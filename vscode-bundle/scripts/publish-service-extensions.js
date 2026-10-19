// Fixed service allowlist. Run from the trusted VSCodeMCP publisher workflow.
const fs = require('node:fs');
const path = require('node:path');

const SERVICES = Object.freeze({
  suno: { directory: 'suno/vscode', extension: 'mcp-suno', mirror: 'AceDataCloud/SunoMCP' },
  seedance: { directory: 'seedance/vscode', extension: 'mcp-seedance', mirror: 'AceDataCloud/SeedanceMCP' },
  happyhorse: { directory: 'happyhorse/vscode', extension: 'mcp-happyhorse', mirror: 'AceDataCloud/HappyHorseMCP' },
  'gpt-image': { directory: 'openai/vscode', extension: 'mcp-gpt-image', mirror: 'AceDataCloud/OpenAIMCP' },
  nanobanana: { directory: 'nanobanana/vscode', extension: 'mcp-nanobanana', mirror: 'AceDataCloud/NanoBananaMCP' },
});

function selectServices(service) {
  if (service === 'all') return Object.keys(SERVICES);
  if (!Object.hasOwn(SERVICES, service)) throw new Error('Unknown service');
  return [service];
}

function serviceMatrix(service) {
  return selectServices(service).map(name => ({ service: name, mirror: SERVICES[name].mirror }));
}

function packageFiles(directory) {
  const files = new Map();
  function walk(current, prefix = '') {
    for (const item of fs.readdirSync(current, { withFileTypes: true })) {
      const relative = path.posix.join(prefix, item.name);
      if (item.isSymbolicLink()) throw new Error('Package source cannot contain symlinks');
      if (item.isDirectory()) walk(path.join(current, item.name), relative);
      else if (item.isFile()) files.set(relative, fs.readFileSync(path.join(current, item.name)));
    }
  }
  walk(directory);
  return files;
}

function verifyMirror(service, source, mirror) {
  selectServices(service);
  const entry = SERVICES[service];
  if (!entry) throw new Error('Verify one service mirror');
  const expected = packageFiles(path.join(source, entry.directory));
  const actual = packageFiles(path.join(mirror, 'vscode'));
  if (!expected.size || expected.size !== actual.size
      || [...expected].some(([name, value]) => !actual.has(name) || !value.equals(actual.get(name)))) {
    throw new Error('Service mirror has not synced the exact VS Code package; publish is blocked');
  }
  console.log(`Exact package mirror verified: ${entry.mirror}`);
}

function nextVersion(versions, now) {
  const prefix = `${now.getUTCFullYear()}.${now.getUTCMonth() + 1}${String(now.getUTCDate()).padStart(2, '0')}.`;
  const builds = versions.filter(v => v.startsWith(prefix)).map(v => v.slice(prefix.length));
  if (builds.some(v => !/^\d+$/.test(v))) throw new Error('Invalid existing CalVer');
  return prefix + (builds.length ? Math.max(...builds.map(Number)) + 1 : 0);
}

async function gallery(extension, fetchImpl = fetch, { includeUnvalidated = false } = {}) {
  const response = await fetchImpl('https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json;api-version=7.2-preview.1' },
    // IncludeVersions (1), IncludeVersionProperties (16), IncludeAssetUri (128).
    // Allocation must include pending uploads; verification excludes them (32).
    body: JSON.stringify({ filters: [{ criteria: [{ filterType: 7, value: `acedatacloud.${extension}` }] }], flags: 145 | (includeUnvalidated ? 0 : 32) }),
    signal: AbortSignal.timeout(30000),
  });
  if (!response.ok) throw new Error(`Gallery query failed: ${response.status}`);
  const body = await response.json();
  const results = body.results?.[0]?.extensions;
  if (!Array.isArray(results)) throw new Error('Malformed Gallery response');
  const match = results.find(x => x.publisher?.publisherName === 'acedatacloud' && x.extensionName === extension);
  return match;
}

async function prepare(service, source, { now = new Date(), fetchImpl = fetch } = {}) {
  selectServices(service); // Reject unknown input before reading files.
  if (service === 'all') throw new Error('Prepare one service per matrix job');
  const entry = SERVICES[service];
  const directory = path.join(source, entry.directory);
  const file = path.join(directory, 'package.json');
  const pkg = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (pkg.publisher !== 'acedatacloud' || pkg.name !== entry.extension) throw new Error('Unexpected publisher/package identity');
  if (!pkg.contributes?.mcpServerDefinitionProviders?.length || !fs.existsSync(path.join(directory, pkg.main))) throw new Error('Missing stable MCP runtime');
  const existing = await gallery(entry.extension, fetchImpl, { includeUnvalidated: true });
  const version = nextVersion((existing?.versions || []).map(x => x.version), now);
  fs.writeFileSync(file, JSON.stringify({ ...pkg, version }, null, 2) + '\n');
  return { directory, version, extension: entry.extension };
}

async function verify(service, expected) {
  selectServices(service);
  const entry = SERVICES[service];
  if (!entry) throw new Error('Verify one service');
  for (let attempt = 0; attempt < 40; attempt += 1) {
    const extension = await gallery(entry.extension);
    const flags = new Set(String(extension?.flags || '').split(/,\s*/));
    const version = extension?.versions?.find(x => x.version === expected);
    if (flags.has('public') && version && String(version.flags || '').split(/,\s*/).includes('validated')) {
      console.log(`Public Marketplace version verified: acedatacloud.${entry.extension}@${expected}`);
      return;
    }
    if (attempt < 39) await new Promise(resolve => setTimeout(resolve, 15000));
  }
  throw new Error('Expected public/validated version not visible');
}

module.exports = { SERVICES, selectServices, serviceMatrix, nextVersion, gallery, prepare, verifyMirror };
if (require.main === module) {
  const [command, service, argument] = process.argv.slice(2);
  (async () => {
    if (command === 'matrix') console.log(JSON.stringify(serviceMatrix(service)));
    else if (command === 'verify-mirror') verifyMirror(service, argument, process.argv[5]);
    else if (command === 'prepare') {
      const result = await prepare(service, argument);
      for (const [key, value] of Object.entries(result)) {
        if (/[\r\n]/.test(value)) throw new Error('Invalid output value');
        fs.appendFileSync(process.env.GITHUB_OUTPUT, `${key}=${value}\n`);
      }
    } else if (command === 'verify') await verify(service, argument);
    else throw new Error('Unknown command');
  })().catch(error => { console.error(error.message); process.exitCode = 1; });
}
