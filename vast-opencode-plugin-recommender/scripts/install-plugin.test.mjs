import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {
  installPlugin,
  resolvePlugin,
  validateInstallMetadata,
} from './install-plugin.mjs';

const builtinPath = path.resolve(
  import.meta.dirname,
  '..',
  'plugin-builtin.json',
);

async function fixture(t) {
  const root = await mkdtemp(path.join(os.tmpdir(), 'opencode-installer-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const home = path.join(root, 'home');
  const projectDir = path.join(root, 'project');
  await mkdir(home);
  await mkdir(projectDir);
  execFileSync('git', ['init', '--quiet'], { cwd: projectDir });
  return { home, projectDir };
}

function options(paths, overrides = {}) {
  return {
    plugin: 'builtin-cc-adapter-v2',
    scope: 'project',
    projectDir: paths.projectDir,
    home: paths.home,
    builtinPath,
    env: {},
    ...overrides,
  };
}

test('previews creation of a new global config without writing it', async (t) => {
  const paths = await fixture(t);
  const result = await installPlugin(options(paths, { scope: 'global' }));

  assert.equal(result.schemaVersion, 1);
  assert.equal(result.status, 'ready');
  assert.equal(result.changed, true);
  assert.equal(result.beforeSha256, 'absent');
  assert.equal(
    result.targetPath,
    path.join(paths.home, '.config', 'opencode', 'opencode.json'),
  );
  await assert.rejects(readFile(result.targetPath), { code: 'ENOENT' });

  const applied = await installPlugin(
    options(paths, {
      scope: 'global',
      apply: true,
      expectSha256: result.beforeSha256,
      opencodeBin: false,
    }),
  );
  assert.equal(applied.status, 'installed');
  assert.deepEqual(JSON.parse(await readFile(result.targetPath, 'utf8')), {
    $schema: 'https://opencode.ai/config.json',
    plugin: ['cc-adapter-v2'],
  });
});

test('applies to an existing project config while preserving unknown fields', async (t) => {
  const paths = await fixture(t);
  const targetPath = path.join(paths.projectDir, 'opencode.json');
  await writeFile(targetPath, '{"theme":"system","plugin":["other"]}\n');
  const preview = await installPlugin(options(paths));
  const result = await installPlugin(
    options(paths, {
      apply: true,
      expectSha256: preview.beforeSha256,
      opencodeBin: false,
    }),
  );

  assert.equal(result.status, 'installed');
  assert.equal(result.changed, true);
  assert.equal(result.validation.status, 'pending-restart');
  assert.deepEqual(JSON.parse(await readFile(targetPath, 'utf8')), {
    theme: 'system',
    plugin: ['other', 'cc-adapter-v2'],
  });
});

test('is idempotent when the exact plugin string is already configured', async (t) => {
  const paths = await fixture(t);
  const targetPath = path.join(paths.projectDir, 'opencode.json');
  const original = '{"plugin":["cc-adapter-v2"]}\n';
  await writeFile(targetPath, original);

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'already-installed');
  assert.equal(result.changed, false);
  assert.equal(await readFile(targetPath, 'utf8'), original);
});

test('refuses JSONC instead of rewriting comments', async (t) => {
  const paths = await fixture(t);
  await writeFile(
    path.join(paths.projectDir, 'opencode.jsonc'),
    '{\n  // keep this comment\n  "plugin": []\n}\n',
  );

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'unsupported-jsonc');
  assert.equal(result.changed, false);
});

test('ignores .opencode/opencode.json as a project config candidate', async (t) => {
  const paths = await fixture(t);
  await writeFile(path.join(paths.projectDir, 'opencode.json'), '{}\n');
  await mkdir(path.join(paths.projectDir, '.opencode'));
  await writeFile(
    path.join(paths.projectDir, '.opencode', 'opencode.json'),
    '{}\n',
  );

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'ready');
  assert.equal(result.targetPath, path.join(paths.projectDir, 'opencode.json'));
});

test('refuses ambiguous root JSON and JSONC config candidates', async (t) => {
  const paths = await fixture(t);
  await writeFile(path.join(paths.projectDir, 'opencode.json'), '{}\n');
  await writeFile(path.join(paths.projectDir, 'opencode.jsonc'), '{}\n');

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'ambiguous-config');
  assert.equal(result.changed, false);
  assert.equal(result.conflicts.length, 1);
});

test('reports an exact cross-scope duplicate and does not add it again', async (t) => {
  const paths = await fixture(t);
  const globalDir = path.join(paths.home, '.config', 'opencode');
  await mkdir(globalDir, { recursive: true });
  await writeFile(
    path.join(globalDir, 'opencode.json'),
    '{"plugin":["cc-adapter-v2"]}\n',
  );

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'already-installed-other-scope');
  assert.equal(result.changed, false);
  assert.match(result.warnings.join('\n'), /global/i);
});

test('stops when another scope uses JSONC that cannot be inspected safely', async (t) => {
  const paths = await fixture(t);
  const globalDir = path.join(paths.home, '.config', 'opencode');
  await mkdir(globalDir, { recursive: true });
  await writeFile(
    path.join(globalDir, 'opencode.jsonc'),
    '{ // plugin may already exist\n "plugin": ["cc-adapter-v2"]\n}\n',
  );

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'conflict');
  assert.match(result.conflicts.join('\n'), /JSONC configuration/);
});

test('stops on a tuple option conflict', async (t) => {
  const paths = await fixture(t);
  await writeFile(
    path.join(paths.projectDir, 'opencode.json'),
    '{"plugin":[["cc-adapter-v2",{"commands":false}]]}\n',
  );

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'conflict');
  assert.equal(result.changed, false);
  assert.match(result.conflicts.join('\n'), /tuple options/i);
});

test('stops on a different version of the same npm package', async (t) => {
  const paths = await fixture(t);
  await writeFile(
    path.join(paths.projectDir, 'opencode.json'),
    '{"plugin":["cc-adapter-v2@1.0.0"]}\n',
  );

  const result = await installPlugin(options(paths));

  assert.equal(result.status, 'conflict');
  assert.match(result.conflicts.join('\n'), /version/i);
});

test('rejects apply when the preview digest is stale', async (t) => {
  const paths = await fixture(t);
  const targetPath = path.join(paths.projectDir, 'opencode.json');
  await writeFile(targetPath, '{"theme":"one"}\n');
  const preview = await installPlugin(options(paths));
  const replacement = '{"theme":"two"}\n';
  await writeFile(targetPath, replacement);

  const result = await installPlugin(
    options(paths, {
      apply: true,
      expectSha256: preview.beforeSha256,
      opencodeBin: false,
    }),
  );

  assert.equal(result.status, 'stale-plan');
  assert.equal(result.changed, false);
  assert.equal(await readFile(targetPath, 'utf8'), replacement);
});

test('requires the preview digest in apply mode', async (t) => {
  const paths = await fixture(t);
  const result = await installPlugin(options(paths, { apply: true }));

  assert.equal(result.status, 'expect-sha256-required');
  assert.equal(result.changed, false);
});

test('rolls back when runtime validation fails without exposing output', async (t) => {
  const paths = await fixture(t);
  const targetPath = path.join(paths.projectDir, 'opencode.json');
  const original = '{"theme":"safe"}\n';
  await writeFile(targetPath, original);
  const fakeBin = path.join(paths.projectDir, 'fake-opencode.mjs');
  await writeFile(
    fakeBin,
    '#!/usr/bin/env node\nprocess.stdout.write(JSON.stringify({plugin:[],secret:"DO_NOT_EXPOSE"}));\n',
    { mode: 0o755 },
  );
  const preview = await installPlugin(options(paths));

  const result = await installPlugin(
    options(paths, {
      apply: true,
      expectSha256: preview.beforeSha256,
      opencodeBin: fakeBin,
    }),
  );

  assert.equal(result.status, 'validation-failed');
  assert.equal(result.changed, false);
  assert.equal(result.rolledBack, true);
  assert.doesNotMatch(JSON.stringify(result), /DO_NOT_EXPOSE/);
  assert.equal(await readFile(targetPath, 'utf8'), original);
});

test('runtime validation uses pure mode and verifies the exact plugin', async (t) => {
  const paths = await fixture(t);
  const fakeBin = path.join(paths.projectDir, 'fake-opencode.mjs');
  await writeFile(
    fakeBin,
    '#!/usr/bin/env node\nif (process.env.OPENCODE_PURE !== "1") process.exit(1); process.stdout.write(JSON.stringify({plugin:["cc-adapter-v2"]}));\n',
    { mode: 0o755 },
  );
  const preview = await installPlugin(options(paths));

  const result = await installPlugin(
    options(paths, {
      apply: true,
      expectSha256: preview.beforeSha256,
      opencodeBin: fakeBin,
    }),
  );

  assert.equal(result.status, 'installed');
  assert.equal(result.validation.status, 'passed');
});

test('blocks similarly named files in plugin directories without reading secrets', async (t) => {
  const paths = await fixture(t);
  const pluginDir = path.join(paths.projectDir, '.opencode', 'plugins');
  await mkdir(pluginDir, { recursive: true });
  await writeFile(path.join(pluginDir, 'cc-adapter-v2.js'), 'export default {}');

  const result = await installPlugin(
    options(paths, { env: { OPENCODE_CONFIG_CONTENT: 'DO_NOT_EXPOSE' } }),
  );

  assert.match(result.warnings.join('\n'), /OPENCODE_CONFIG_CONTENT/);
  assert.equal(result.status, 'conflict');
  assert.match(result.conflicts.join('\n'), /plugin directory/i);
  assert.doesNotMatch(JSON.stringify(result), /DO_NOT_EXPOSE/);
});

test('redacts OPENCODE_CONFIG_DIR and detects scoped package filenames', async (t) => {
  const paths = await fixture(t);
  const customDir = path.join(paths.home, 'SECRET_CONFIG_DIR_VALUE');
  await mkdir(path.join(customDir, 'plugins'), { recursive: true });
  await writeFile(path.join(customDir, 'plugins', 'plugin.js'), 'export default {}');
  const userPath = path.join(paths.home, '.claude', 'opencode-plugin-recommend.json');
  await mkdir(path.dirname(userPath), { recursive: true });
  await writeFile(
    userPath,
    JSON.stringify({
      plugins: [{
        id: 'scoped',
        name: 'scoped',
        packageSpec: '@scope/plugin',
        installStrategy: 'opencode-config',
        supportedScopes: ['project'],
      }],
    }),
  );

  const result = await installPlugin(options(paths, {
    plugin: 'scoped',
    userPath,
    env: { OPENCODE_CONFIG_DIR: customDir },
  }));

  assert.equal(result.status, 'conflict');
  assert.match(result.conflicts.join('\n'), /OPENCODE_CONFIG_DIR\/plugins/);
  assert.doesNotMatch(JSON.stringify(result), /SECRET_CONFIG_DIR_VALUE/);
});

test('all auto-installable built-ins have valid installer metadata', async () => {
  const document = JSON.parse(await readFile(builtinPath, 'utf8'));
  const installable = document.plugins.filter((plugin) => plugin.installStrategy);
  assert.deepEqual(validateInstallMetadata(installable), []);
  assert.equal(
    document.plugins.some((plugin) =>
      plugin.installCommand.includes('npm install -g'),
    ),
    false,
  );
});

test('ralph-loop remains manual while the published npm package is stale', async (t) => {
  const paths = await fixture(t);
  await assert.rejects(
    resolvePlugin('ralph-loop', options(paths)),
    /packageSpec|installStrategy|supportedScopes/,
  );
});

test('cc-adapter-v2 resolves by fixed ID and by name with its canonical URL', async (t) => {
  const paths = await fixture(t);
  const base = options(paths);
  const byId = await resolvePlugin('builtin-cc-adapter-v2', base);
  const byName = await resolvePlugin('cc-adapter-v2', base);

  assert.equal(byId.packageSpec, 'cc-adapter-v2');
  assert.equal(byName.id, byId.id);
  assert.equal(byId.url, 'https://github.com/VastFuture/opencode-cc-adapter');
});

test('resolves an installable user recommendation without using installCommand', async (t) => {
  const paths = await fixture(t);
  const userPath = path.join(paths.home, '.claude', 'opencode-plugin-recommend.json');
  await mkdir(path.dirname(userPath), { recursive: true });
  await writeFile(
    userPath,
    JSON.stringify({
      plugins: [
        {
          id: 'user-safe-plugin',
          name: 'safe-plugin',
          packageSpec: 'safe-plugin',
          installStrategy: 'opencode-config',
          supportedScopes: ['project'],
          installCommand: 'exit 99',
        },
      ],
    }),
  );

  const result = await installPlugin(
    options(paths, { plugin: 'safe-plugin', userPath }),
  );

  assert.equal(result.status, 'ready');
  assert.deepEqual(result.expectedChange, { pluginAppend: 'safe-plugin' });
});

test('CLI preview emits only the minimal change and never leaks existing secrets', async (t) => {
  const paths = await fixture(t);
  await writeFile(
    path.join(paths.projectDir, 'opencode.json'),
    '{"apiKey":"LITERAL_API_KEY","nested":{"secret":"LITERAL_SECRET"}}\n',
  );
  const stdout = execFileSync(
    process.execPath,
    [
      path.resolve(import.meta.dirname, 'install-plugin.mjs'),
      '--plugin',
      'cc-adapter-v2',
      '--scope',
      'project',
      '--project-dir',
      paths.projectDir,
    ],
    { encoding: 'utf8', env: { ...process.env, HOME: paths.home } },
  );
  const envelope = JSON.parse(stdout);

  assert.equal(envelope.schemaVersion, 1);
  assert.equal(envelope.status, 'ready');
  assert.equal(envelope.changed, true);
  assert.match(envelope.beforeSha256, /^[a-f0-9]{64}$/);
  assert.deepEqual(envelope.conflicts, []);
  assert.deepEqual(envelope.expectedChange, { pluginAppend: 'cc-adapter-v2' });
  assert.equal('expectedConfig' in envelope, false);
  assert.doesNotMatch(stdout, /LITERAL_API_KEY|LITERAL_SECRET/);
});

test('rejects unsafe package specs', () => {
  const invalid = [
    '../plugin',
    './plugin',
    '/tmp/plugin',
    'https://example.com/plugin',
    'git+https://example.com/plugin.git',
    'github:user/repo',
    'name with space',
  ];
  for (const packageSpec of invalid) {
    assert.notDeepEqual(
      validateInstallMetadata([
        {
          id: packageSpec,
          packageSpec,
          installStrategy: 'opencode-config',
          supportedScopes: ['project'],
        },
      ]),
      [],
      packageSpec,
    );
  }
  assert.deepEqual(
    validateInstallMetadata([
      {
        id: 'valid',
        packageSpec: '@scope/plugin@next',
        installStrategy: 'opencode-config',
        supportedScopes: ['project'],
      },
    ]),
    [],
  );
});

test('built-in name wins over a user recommendation with the same name', async (t) => {
  const paths = await fixture(t);
  const userPath = path.join(paths.home, '.claude', 'opencode-plugin-recommend.json');
  await mkdir(path.dirname(userPath), { recursive: true });
  await writeFile(
    userPath,
    JSON.stringify({
      plugins: [
        {
          id: 'user-shadow',
          name: 'cc-adapter-v2',
          packageSpec: 'malicious-shadow',
          installStrategy: 'opencode-config',
          supportedScopes: ['project'],
        },
      ],
    }),
  );

  const plugin = await resolvePlugin('cc-adapter-v2', options(paths));
  assert.equal(plugin.id, 'builtin-cc-adapter-v2');
});

test('runtime validation rejects invalid JSON and rolls back', async (t) => {
  const paths = await fixture(t);
  const targetPath = path.join(paths.projectDir, 'opencode.json');
  const original = '{"theme":"safe"}\n';
  await writeFile(targetPath, original);
  const fakeBin = path.join(paths.projectDir, 'fake-opencode.mjs');
  await writeFile(fakeBin, '#!/usr/bin/env node\nprocess.stdout.write("not json");\n', {
    mode: 0o755,
  });
  const preview = await installPlugin(options(paths));
  const result = await installPlugin(
    options(paths, {
      apply: true,
      expectSha256: preview.beforeSha256,
      opencodeBin: fakeBin,
    }),
  );

  assert.equal(result.status, 'validation-failed');
  assert.equal(result.rolledBack, true);
  assert.equal(await readFile(targetPath, 'utf8'), original);
});
