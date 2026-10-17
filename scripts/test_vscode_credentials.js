const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const services = ['acedatacloud', 'face', 'fish', 'flux', 'grok', 'happyhorse', 'openai', 'hailuo', 'kling', 'luma', 'midjourney', 'nanobanana', 'producer', 'seedance', 'seedream', 'serp', 'shorturl', 'suno', 'veo', 'wan'];

function load(alias, { input, env = {}, stored } = {}) {
  const state = { prompts: [], commands: new Map(), secrets: new Map(), provider: undefined };
  if (stored) state.secrets.set(`${alias}.apiToken`, stored);
  const vscode = {
    EventEmitter: class { event() {} fire() {} },
    Uri: { parse: value => new URL(value) },
    McpHttpServerDefinition: class {
      constructor(label, uri, headers) { Object.assign(this, { label, uri, headers }); }
    },
    commands: { registerCommand: (id, action) => { state.commands.set(id, action); return {}; } },
    window: {
      showInputBox: async options => { state.prompts.push(options); return input; },
      showInformationMessage: () => {},
    },
    lm: { registerMcpServerDefinitionProvider: (_, provider) => { state.provider = provider; return {}; } },
  };
  const context = {
    subscriptions: [],
    secrets: {
      get: async key => state.secrets.get(key),
      store: async (key, value) => state.secrets.set(key, value),
      delete: async key => state.secrets.delete(key),
      onDidChange: () => ({}),
    },
  };
  const sandbox = { module: { exports: {} }, process: { env }, require: name => {
    assert.equal(name, 'vscode'); return vscode;
  } };
  vm.runInNewContext(fs.readFileSync(path.join(root, alias, 'vscode/extension.js'), 'utf8'), sandbox);
  sandbox.module.exports.activate(context);
  state.resolve = () => state.provider.resolveMcpServerDefinition(state.provider.provideMcpServerDefinitions()[0]);
  return state;
}

test('generated credential prompts use the matching credential page and current attribution', async t => {
  for (const alias of services) await t.test(alias, async () => {
    const account = alias === 'acedatacloud';
    const state = load(alias, { input: account ? '  platform-test-token  ' : '  test-api-key  ' });
    const definition = await state.resolve();
    const prompt = state.prompts[0];
    const url = new URL(prompt.prompt.match(/https:\/\/\S+/)[0].replace(/\.$/, ''));
    assert.equal(url.origin, 'https://platform.acedata.cloud');
    assert.equal(url.pathname, account ? '/console/platform-tokens' : '/console/applications');
    assert.equal(url.searchParams.get('utm_source'), 'vscode');
    assert.equal(url.searchParams.get('utm_medium'), 'referral');
    assert.equal(url.searchParams.get('utm_campaign'), 'evergreen');
    assert.equal(url.searchParams.get('utm_content'), `${alias}_mcp_extension_${account ? 'platform_token' : 'api_key'}`);
    assert.equal(prompt.password, true);
    assert.equal(definition.headers.Authorization, account ? 'Bearer platform-test-token' : 'Bearer test-api-key');
    assert.equal(state.secrets.get(`${alias}.apiToken`), account ? 'platform-test-token' : 'test-api-key');
    assert.equal(definition.uri.search, '');
  });
});

test('account cancellation explains the platform-token command without persisting a value', async () => {
  const state = load('acedatacloud');
  await assert.rejects(state.resolve(), /Set Ace Data Cloud Platform Token/);
  assert.equal(state.secrets.size, 0);
});

test('configured credentials keep precedence and do not prompt', async () => {
  for (const alias of ['acedatacloud', 'suno']) {
    const variable = alias === 'acedatacloud' ? 'ACEDATACLOUD_PLATFORM_TOKEN' : 'ACEDATACLOUD_API_TOKEN';
    const state = load(alias, { env: { [variable]: '  env-test-token  ' }, stored: 'stored-test-token' });
    const definition = await state.resolve();
    assert.equal(definition.headers.Authorization, 'Bearer env-test-token');
    assert.equal(state.prompts.length, 0);
  }
});

test('existing clear command still removes the per-service credential', async () => {
  const state = load('acedatacloud', { stored: 'platform-test-token' });
  await state.commands.get('acedatacloud.acedatacloud.clearApiToken')();
  assert.equal(state.secrets.size, 0);
});

test('account command labels match its prompted credential', () => {
  const pkg = JSON.parse(fs.readFileSync(path.join(root, 'acedatacloud/vscode/package.json'), 'utf8'));
  assert.equal(pkg.contributes.commands[0].command, 'acedatacloud.acedatacloud.setApiToken');
  assert.match(pkg.contributes.commands[0].title, /Set Ace Data Cloud Platform Token$/);
  assert.match(pkg.contributes.commands[1].title, /Clear Ace Data Cloud Platform Token$/);
});
