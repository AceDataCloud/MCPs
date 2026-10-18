const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { SERVICES, selectServices, serviceMatrix, nextVersion, gallery, prepare, verifyMirror } = require('../scripts/publish-service-extensions');

test('publisher only accepts five fixed independent packages', () => {
  assert.equal(selectServices('all').length, 5);
  assert.equal(SERVICES['gpt-image'].directory, 'openai/vscode');
  assert.equal(SERVICES.happyhorse.extension, 'mcp-happyhorse');
  assert.deepEqual(serviceMatrix('gpt-image'), [{ service: 'gpt-image', mirror: 'AceDataCloud/OpenAIMCP' }]);
  for (const invalid of ['../openai', 'sora', 'https://elsewhere', 'all; echo x']) assert.throws(() => selectServices(invalid));
});

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'vscode-service-publish-'));
  const directory = path.join(root, 'source', 'happyhorse', 'vscode');
  fs.mkdirSync(directory, { recursive: true });
  const pkg = { publisher: 'acedatacloud', name: 'mcp-happyhorse', version: '0.3.0', main: './extension.js', contributes: { mcpServerDefinitionProviders: [{ id: 'acedatacloud.happyhorse' }] } };
  fs.writeFileSync(path.join(directory, 'package.json'), JSON.stringify(pkg));
  fs.writeFileSync(path.join(directory, 'extension.js'), 'module.exports = {};\n');
  return { root, source: path.join(root, 'source'), directory, pkg };
}

test('allocation includes pending uploaded versions, while public verification queries exclude them', async () => {
  const f = fixture();
  try {
    let flags;
    const result = await prepare('happyhorse', f.source, {
      now: new Date('2026-10-19T00:01:00Z'),
      fetchImpl: async (_, options) => {
        flags = JSON.parse(options.body).flags;
        return { ok: true, json: async () => ({ results: [{ extensions: [{ publisher: { publisherName: 'acedatacloud' }, extensionName: 'mcp-happyhorse', versions: [
          { version: '2026.1019.0', flags: 'validated' }, { version: '2026.1019.1', flags: 'none' },
        ] }] }] }) };
      },
    });
    assert.equal(flags & 32, 0);
    assert.equal(result.version, '2026.1019.2');
    await gallery('mcp-happyhorse', async (_, options) => {
      assert.equal(JSON.parse(options.body).flags & 32, 32);
      return { ok: true, json: async () => ({ results: [{ extensions: [] }] }) };
    });
  } finally { fs.rmSync(f.root, { recursive: true }); }
});

test('failed version lookup leaves the source version unchanged', async () => {
  const f = fixture();
  try {
    const before = fs.readFileSync(path.join(f.directory, 'package.json'), 'utf8');
    await assert.rejects(prepare('happyhorse', f.source, { fetchImpl: async () => ({ ok: false, status: 429 }) }), /429/);
    assert.equal(fs.readFileSync(path.join(f.directory, 'package.json'), 'utf8'), before);
  } finally { fs.rmSync(f.root, { recursive: true }); }
});

test('mirror gate accepts exact package bytes and rejects stale or extra package files', () => {
  const f = fixture();
  try {
    const mirror = path.join(f.root, 'mirror');
    fs.cpSync(f.directory, path.join(mirror, 'vscode'), { recursive: true });
    verifyMirror('happyhorse', f.source, mirror);
    fs.writeFileSync(path.join(mirror, 'vscode', 'extension.js'), 'old runtime');
    assert.throws(() => verifyMirror('happyhorse', f.source, mirror), /has not synced/);
    fs.cpSync(f.directory, path.join(mirror, 'vscode'), { recursive: true });
    fs.writeFileSync(path.join(mirror, 'vscode', 'unexpected.js'), 'extra');
    assert.throws(() => verifyMirror('happyhorse', f.source, mirror), /has not synced/);
    fs.writeFileSync(path.join(f.directory, 'empty.txt'), '');
    fs.cpSync(f.directory, path.join(mirror, 'vscode'), { recursive: true });
    fs.unlinkSync(path.join(mirror, 'vscode', 'empty.txt'));
    assert.throws(() => verifyMirror('happyhorse', f.source, mirror), /has not synced/);
  } finally { fs.rmSync(f.root, { recursive: true }); }
});

test('CalVer increments existing builds and uses UTC', () => {
  const now = new Date('2026-10-18T00:01:00Z');
  assert.equal(nextVersion([], now), '2026.1018.0');
  assert.equal(nextVersion(['2026.1018.0', '2026.1018.2', '2026.1017.9'], now), '2026.1018.3');
  assert.throws(() => nextVersion(['2026.1018.invalid'], now));
});

test('Gallery failure never masquerades as an unpublished package', async () => {
  await assert.rejects(gallery('mcp-happyhorse', async () => ({ ok: false, status: 503 })), /503/);
  await assert.rejects(gallery('mcp-happyhorse', async () => ({ ok: true, json: async () => ({}) })), /Malformed/);
  assert.equal(await gallery('mcp-happyhorse', async () => ({ ok: true, json: async () => ({ results: [{ extensions: [] }] }) })), undefined);
});

test('Gallery filters out another publisher or extension', async () => {
  const selected = { publisher: { publisherName: 'acedatacloud' }, extensionName: 'mcp-happyhorse', versions: [] };
  const result = await gallery('mcp-happyhorse', async () => ({ ok: true, json: async () => ({ results: [{ extensions: [
    { publisher: { publisherName: 'other' }, extensionName: 'mcp-happyhorse' }, selected,
  ] }] }) }));
  assert.equal(result, selected);
});
