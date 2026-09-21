const fs = require('fs');
const path = require('path');

// Load puppeteer from the globally installed @mermaid-js/mermaid-cli
const puppeteerPath = path.join(
  '/home/fenghaolin/.nvm/versions/node/v25.7.0/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer'
);
const puppeteer = require(puppeteerPath);

async function runQualityGate() {
  const dataPath = path.join(__dirname, 'assets/skills-data.json');
  const skills = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

  console.log(`Starting headless quality gate for ${skills.length} Mermaid diagrams...`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Load mermaid script in page
  await page.setContent(`
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
      </head>
      <body>
      </body>
    </html>
  `);

  await page.waitForFunction('typeof window.mermaid !== "undefined"');

  const failures = [];

  for (let i = 0; i < skills.length; i++) {
    const s = skills[i];
    const code = s.mermaid;

    const result = await page.evaluate(async (mmdCode) => {
      try {
        const parseResult = await window.mermaid.parse(mmdCode);
        return { success: true };
      } catch (err) {
        return { success: false, error: err.message || err.str || String(err) };
      }
    }, code);

    if (!result.success) {
      failures.push({
        id: s.id,
        name: s.displayTitle || s.name,
        error: result.error,
        code: code
      });
      console.log(`[FAIL] ${s.id}: ${result.error.split('\n')[0]}`);
    }
  }

  await browser.close();

  console.log('\n================ QUALITY GATE VERDICT ================');
  console.log(`Total Tested: ${skills.length}`);
  console.log(`Passed: ${skills.length - failures.length}`);
  console.log(`Failed: ${failures.length}`);

  if (failures.length > 0) {
    fs.writeFileSync(
      path.join(__dirname, 'mermaid_failures.json'),
      JSON.stringify(failures, null, 2),
      'utf8'
    );
    console.log(`Saved ${failures.length} failures to tutorial-site/mermaid_failures.json`);
    process.exit(1);
  } else {
    console.log('ALL 171 MERMAID DIAGRAMS 100% VALIDATED BY MERMAID PARSER!');
    process.exit(0);
  }
}

runQualityGate().catch((err) => {
  console.error('Gate error:', err);
  process.exit(1);
});
