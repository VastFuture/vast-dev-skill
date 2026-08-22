#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import {
  access,
  mkdir,
  readFile,
  readdir,
  realpath,
  rename,
  rm,
  stat,
  writeFile,
} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCHEMA_VERSION = 1;
const DEFAULT_SCHEMA = 'https://opencode.ai/config.json';
const BUILTIN_PATH = path.resolve(import.meta.dirname, '..', 'plugin-builtin.json');

function result(status, targetPath = null) {
  return {
    schemaVersion: SCHEMA_VERSION,
    status,
    changed: false,
    targetPath,
    beforeSha256: null,
    warnings: [],
    conflicts: [],
  };
}

function sha256(content) {
  return createHash('sha256').update(content).digest('hex');
}

async function exists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch (error) {
    if (error.code === 'ENOENT') return false;
    throw error;
  }
}

async function readDocument(filePath) {
  const content = await readFile(filePath, 'utf8');
  return { content, document: JSON.parse(content) };
}

function packageName(spec) {
  if (spec.startsWith('@')) {
    const slash = spec.indexOf('/');
    const version = spec.indexOf('@', slash);
    return version === -1 ? spec : spec.slice(0, version);
  }
  const version = spec.indexOf('@');
  return version === -1 ? spec : spec.slice(0, version);
}

function isPackageSpec(spec) {
  return /^(?:@[a-z0-9][a-z0-9._~-]*\/)?[a-z0-9][a-z0-9._~-]*(?:@[a-zA-Z0-9][a-zA-Z0-9._+~-]*)?$/.test(
    spec,
  );
}

function inspectEntries(entries, wanted) {
  const exact = [];
  const conflicts = [];
  for (const entry of entries ?? []) {
    const tuple = Array.isArray(entry);
    const spec = tuple ? entry[0] : entry;
    if (typeof spec !== 'string') continue;
    if (spec === wanted) {
      if (tuple) conflicts.push(`${wanted} already has tuple options`);
      else exact.push(spec);
    } else if (packageName(spec) === packageName(wanted)) {
      conflicts.push(`${wanted} has a conflicting version: ${spec}`);
    }
  }
  return { exact, conflicts };
}

export function validateInstallMetadata(plugins) {
  const errors = [];
  for (const plugin of plugins) {
    const prefix = plugin.id || plugin.name || '<unknown>';
    if (typeof plugin.packageSpec !== 'string' || !isPackageSpec(plugin.packageSpec)) {
      errors.push(`${prefix}: packageSpec must be a bare or scoped npm package`);
    }
    if (plugin.installStrategy !== 'opencode-config') {
      errors.push(`${prefix}: installStrategy must be opencode-config`);
    }
    if (
      !Array.isArray(plugin.supportedScopes) ||
      plugin.supportedScopes.length === 0 ||
      plugin.supportedScopes.some(
        (scope) => scope !== 'global' && scope !== 'project',
      )
    ) {
      errors.push(`${prefix}: supportedScopes must contain global or project`);
    }
  }
  return errors;
}

async function loadPlugins(options) {
  const builtinPath = options.builtinPath ?? BUILTIN_PATH;
  const home = options.home ?? os.homedir();
  const builtin = JSON.parse(await readFile(builtinPath, 'utf8')).plugins ?? [];
  const userPath =
    options.userPath ?? path.join(home, '.claude', 'opencode-plugin-recommend.json');
  const user = (await exists(userPath))
    ? JSON.parse(await readFile(userPath, 'utf8')).plugins ?? []
    : [];
  return { builtin, user };
}

export async function resolvePlugin(query, options = {}) {
  const plugins = await loadPlugins(options);
  const byId = [...plugins.builtin, ...plugins.user].filter(
    (plugin) => plugin.id === query,
  );
  const builtinByName = plugins.builtin.filter((plugin) => plugin.name === query);
  const userByName = plugins.user.filter((plugin) => plugin.name === query);
  const matches = byId.length ? byId : builtinByName.length ? builtinByName : userByName;
  if (matches.length !== 1) {
    throw new Error(matches.length ? 'Ambiguous plugin recommendation' : 'Plugin not found');
  }
  const errors = validateInstallMetadata(matches);
  if (errors.length) throw new Error(errors.join('; '));
  return matches[0];
}

async function assertGitRoot(projectDir) {
  if (!projectDir) throw new Error('--project-dir is required for project scope');
  const command = spawnSync('git', ['rev-parse', '--show-toplevel'], {
    cwd: projectDir,
    encoding: 'utf8',
  });
  if (command.status !== 0) throw new Error('Project directory is not a Git worktree');
  const [actual, requested] = await Promise.all([
    realpath(command.stdout.trim()),
    realpath(projectDir),
  ]);
  if (actual !== requested) throw new Error('Project directory must be the Git root');
  return requested;
}

async function discoverTarget(scope, home, projectDir) {
  const base =
    scope === 'global' ? path.join(home, '.config', 'opencode') : projectDir;
  const candidates =
    scope === 'global'
      ? [path.join(base, 'opencode.json'), path.join(base, 'opencode.jsonc')]
      : [
          path.join(base, 'opencode.json'),
          path.join(base, 'opencode.jsonc'),
        ];
  const present = [];
  for (const candidate of candidates) {
    if (await exists(candidate)) present.push(candidate);
  }
  if (present.length > 1) return { status: 'ambiguous-config', present };
  if (present[0]?.endsWith('.jsonc')) return { status: 'unsupported-jsonc', present };
  return {
    status: 'ok',
    targetPath: present[0] ?? path.join(base, 'opencode.json'),
  };
}

async function inspectConfig(filePath, wanted) {
  if (!(await exists(filePath))) return { exact: [], conflicts: [] };
  const { document } = await readDocument(filePath);
  if (document.plugin !== undefined && !Array.isArray(document.plugin)) {
    return { exact: [], conflicts: ['plugin must be an array'] };
  }
  return inspectEntries(document.plugin, wanted);
}

async function inspectOtherConfigs(options, targetPath, wanted) {
  const paths = new Map();
  const globalBase = path.join(options.home, '.config', 'opencode');
  const globalPaths = [
    path.join(globalBase, 'opencode.json'),
    path.join(globalBase, 'opencode.jsonc'),
  ];
  const projectPaths = options.projectDir
    ? [
        path.join(options.projectDir, 'opencode.json'),
        path.join(options.projectDir, 'opencode.jsonc'),
      ]
    : [];
  for (const globalPath of globalPaths) paths.set(globalPath, 'global config');
  for (const projectPath of projectPaths) paths.set(projectPath, 'project config');
  if (options.env.OPENCODE_CONFIG) {
    paths.set(path.resolve(options.env.OPENCODE_CONFIG), 'OPENCODE_CONFIG');
  }
  const warnings = [];
  const conflicts = [];
  let duplicate = false;
  for (const [filePath, label] of paths) {
    if (filePath === targetPath || !(await exists(filePath))) continue;
    if (filePath.endsWith('.jsonc')) {
      conflicts.push(`${label}: JSONC configuration cannot be inspected safely`);
      continue;
    }
    const inspected = await inspectConfig(filePath, wanted);
    if (inspected.exact.length) {
      duplicate = true;
      warnings.push(`Plugin is already present in ${label}`);
    }
    conflicts.push(...inspected.conflicts.map((message) => `${label}: ${message}`));
  }
  return { duplicate, warnings, conflicts };
}

async function inspectPluginDirectories(options, wanted) {
  const directories = [{
    path: path.join(options.home, '.config', 'opencode', 'plugins'),
    label: 'global plugin directory',
  }];
  if (options.projectDir) {
    directories.push({
      path: path.join(options.projectDir, '.opencode', 'plugins'),
      label: 'project plugin directory',
    });
  }
  if (options.env.OPENCODE_CONFIG_DIR) {
    directories.push(
      {
        path: path.join(options.env.OPENCODE_CONFIG_DIR, 'plugin'),
        label: 'OPENCODE_CONFIG_DIR/plugin',
      },
      {
        path: path.join(options.env.OPENCODE_CONFIG_DIR, 'plugins'),
        label: 'OPENCODE_CONFIG_DIR/plugins',
      },
    );
  }
  const localName = packageName(wanted).split('/').at(-1);
  const conflicts = [];
  for (const directory of directories) {
    if (!(await exists(directory.path))) continue;
    const info = await stat(directory.path);
    if (!info.isDirectory()) continue;
    const names = await readdir(directory.path);
    if (names.some((name) => name.includes(localName))) {
      conflicts.push(`A similarly named file exists in ${directory.label}`);
    }
  }
  return conflicts;
}

async function atomicWrite(filePath, content) {
  await mkdir(path.dirname(filePath), { recursive: true });
  const temporary = path.join(
    path.dirname(filePath),
    `.${path.basename(filePath)}.${process.pid}.${Date.now()}.tmp`,
  );
  await writeFile(temporary, content, { mode: 0o600 });
  try {
    await rename(temporary, filePath);
  } catch (error) {
    await rm(temporary, { force: true });
    throw error;
  }
}

function validateWrittenConfig(content, wanted) {
  const document = JSON.parse(content);
  if (!Array.isArray(document.plugin)) throw new Error('plugin must be an array');
  const inspected = inspectEntries(document.plugin, wanted);
  if (inspected.exact.length !== 1 || inspected.conflicts.length) {
    throw new Error('Written plugin entry is not unique');
  }
}

function runtimeValidate(binary, cwd, env, wanted) {
  if (binary === false) return { status: 'pending-restart' };
  const executable = binary ?? 'opencode';
  const command = spawnSync(executable, ['debug', 'config'], {
    cwd,
    encoding: 'utf8',
    env: { ...env, OPENCODE_PURE: '1' },
  });
  if (command.error?.code === 'ENOENT') return { status: 'pending-restart' };
  if (command.status !== 0 || command.error) return { status: 'failed' };
  try {
    const document = JSON.parse(command.stdout);
    const entries = inspectEntries(document.plugin, wanted);
    return entries.exact.length === 1 && entries.conflicts.length === 0
      ? { status: 'passed' }
      : { status: 'failed' };
  } catch {
    return { status: 'failed' };
  }
}

export async function installPlugin(input) {
  const options = {
    env: process.env,
    home: os.homedir(),
    ...input,
  };
  if (options.scope !== 'global' && options.scope !== 'project') {
    throw new Error('--scope must be global or project');
  }
  if (options.scope === 'project') {
    options.projectDir = await assertGitRoot(options.projectDir);
  }
  const plugin = await resolvePlugin(options.plugin, options);
  if (!plugin.supportedScopes.includes(options.scope)) {
    throw new Error(`Plugin does not support ${options.scope} scope`);
  }

  const discovered = await discoverTarget(
    options.scope,
    options.home,
    options.projectDir,
  );
  const fallbackPath = discovered.present?.[0] ?? null;
  const output = result(discovered.status, discovered.targetPath ?? fallbackPath);
  if (discovered.status !== 'ok') {
    if (discovered.status === 'ambiguous-config') {
      output.conflicts.push('Multiple OpenCode configuration files exist in the target scope');
    }
    return output;
  }

  const targetExists = await exists(discovered.targetPath);
  let original = null;
  let document = { $schema: DEFAULT_SCHEMA };
  if (targetExists) {
    try {
      const parsed = await readDocument(discovered.targetPath);
      original = parsed.content;
      document = parsed.document;
    } catch {
      output.status = 'invalid-json';
      output.conflicts.push('Target configuration is not valid JSON');
      return output;
    }
  }
  output.beforeSha256 = targetExists ? sha256(original) : 'absent';
  if (document.plugin !== undefined && !Array.isArray(document.plugin)) {
    output.status = 'conflict';
    output.conflicts.push('plugin must be an array');
    return output;
  }

  const targetEntries = inspectEntries(document.plugin, plugin.packageSpec);
  if (targetEntries.conflicts.length) {
    output.status = 'conflict';
    output.conflicts.push(...targetEntries.conflicts);
    return output;
  }
  if (targetEntries.exact.length) {
    output.status = 'already-installed';
    return output;
  }

  const other = await inspectOtherConfigs(options, discovered.targetPath, plugin.packageSpec);
  output.warnings.push(...other.warnings);
  output.conflicts.push(...other.conflicts);
  output.conflicts.push(
    ...(await inspectPluginDirectories(options, plugin.packageSpec)),
  );
  if (Object.hasOwn(options.env, 'OPENCODE_CONFIG_CONTENT')) {
    output.warnings.push('OPENCODE_CONFIG_CONTENT is set and was not read');
  }
  output.warnings.push('Remote and managed runtime configuration cannot be inspected');
  if (output.conflicts.length) {
    output.status = 'conflict';
    return output;
  }
  if (other.duplicate) {
    output.status = 'already-installed-other-scope';
    return output;
  }

  output.status = 'ready';
  output.changed = true;
  output.expectedChange = { pluginAppend: plugin.packageSpec };
  const expectedConfig = {
    ...document,
    plugin: [...(document.plugin ?? []), plugin.packageSpec],
  };
  if (!options.apply) return output;
  if (!options.expectSha256) {
    output.status = 'expect-sha256-required';
    output.changed = false;
    delete output.expectedChange;
    return output;
  }

  const currentExists = await exists(discovered.targetPath);
  const current = currentExists ? await readFile(discovered.targetPath, 'utf8') : null;
  const currentDigest = currentExists ? sha256(current) : 'absent';
  if (currentDigest !== options.expectSha256) {
    output.status = 'stale-plan';
    output.changed = false;
    delete output.expectedChange;
    return output;
  }

  const written = `${JSON.stringify(expectedConfig, null, 2)}\n`;
  const writtenDigest = sha256(written);
  await atomicWrite(discovered.targetPath, written);
  try {
    validateWrittenConfig(await readFile(discovered.targetPath, 'utf8'), plugin.packageSpec);
  } catch {
    const rollback = await rollbackIfUnchanged(
      discovered.targetPath,
      original,
      writtenDigest,
    );
    output.status = 'validation-failed';
    output.changed = false;
    output.rolledBack = rollback;
    if (!rollback) {
      output.warnings.push('Configuration changed concurrently; automatic rollback was skipped');
    }
    delete output.expectedChange;
    return output;
  }

  const validation = runtimeValidate(
    options.opencodeBin,
    options.scope === 'project' ? options.projectDir : options.home,
    { ...process.env, ...options.env, HOME: options.home },
    plugin.packageSpec,
  );
  if (validation.status === 'failed') {
    output.rolledBack = await rollbackIfUnchanged(
      discovered.targetPath,
      original,
      writtenDigest,
    );
    if (!output.rolledBack) {
      output.warnings.push('Configuration changed concurrently; automatic rollback was skipped');
    }
    output.status = 'validation-failed';
    output.changed = false;
    output.validation = validation;
    delete output.expectedChange;
    return output;
  }

  output.status = 'installed';
  output.validation = validation;
  delete output.expectedChange;
  return output;
}

async function restore(filePath, original) {
  if (original === null) await rm(filePath, { force: true });
  else await atomicWrite(filePath, original);
}

async function rollbackIfUnchanged(filePath, original, writtenDigest) {
  if (!(await exists(filePath))) return false;
  const current = await readFile(filePath, 'utf8');
  if (sha256(current) !== writtenDigest) return false;
  await restore(filePath, original);
  return true;
}

function parseArguments(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--apply') options.apply = true;
    else if (argument === '--plugin') options.plugin = argv[++index];
    else if (argument === '--scope') options.scope = argv[++index];
    else if (argument === '--project-dir') options.projectDir = argv[++index];
    else if (argument === '--expect-sha256') options.expectSha256 = argv[++index];
    else throw new Error(`Unknown argument: ${argument}`);
  }
  if (!options.plugin) throw new Error('--plugin is required');
  return options;
}

async function main() {
  try {
    const output = await installPlugin(parseArguments(process.argv.slice(2)));
    process.stdout.write(`${JSON.stringify(output)}\n`);
    if (!['ready', 'installed', 'already-installed'].includes(output.status)) {
      process.exitCode = 1;
    }
  } catch (error) {
    process.stdout.write(
      `${JSON.stringify({
        ...result('error'),
        error: error instanceof Error ? error.message : 'Unknown error',
      })}\n`,
    );
    process.exitCode = 1;
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  await main();
}
