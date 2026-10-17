const test = require('node:test');
const assert = require('node:assert/strict');
const { SERVICES, selectServices, nextVersion, gallery } = require('../scripts/publish-service-extensions');

test('publisher only accepts five fixed independent packages', () => {
  assert.equal(selectServices('all').length, 5);
  assert.equal(SERVICES['gpt-image'].directory, 'openai/vscode');
  assert.equal(SERVICES.happyhorse.extension, 'mcp-happyhorse');
  for (const invalid of ['../openai', 'sora', 'https://elsewhere', 'all; echo x']) assert.throws(() => selectServices(invalid));
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
