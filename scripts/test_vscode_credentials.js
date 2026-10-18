const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const services = ['acedatacloud', 'face', 'fish', 'flux', 'grok', 'happyhorse', 'openai', 'hailuo', 'kling', 'luma', 'midjourney', 'nanobanana', 'producer', 'seedance', 'seedream', 'serp', 'shorturl', 'suno', 'veo', 'wan'];

function load(alias, { input, env = {}, stored, inputError, storeError } = {}) {
  const state = { prompts: [], commands: new Map(), secrets: new Map(), provider: undefined, secretReads: 0, information: [] };
  if (stored) state.secrets.set(`${alias}.apiToken`, stored);
  const vscode = {
    EventEmitter: class { event() {} fire() {} },
    Uri: { parse: value => new URL(value) },
    McpHttpServerDefinition: class {
      constructor(label, uri, headers) { Object.assign(this, { label, uri, headers }); }
    },
    commands: { registerCommand: (id, action) => { state.commands.set(id, action); return {}; } },
    window: {
      showInputBox: async options => { state.prompts.push(options); if (inputError) throw inputError; return input; },
      showInformationMessage: message => state.information.push(message),
    },
    lm: { registerMcpServerDefinitionProvider: (_, provider) => { state.provider = provider; return {}; } },
  };
  const context = {
    subscriptions: [],
    secrets: {
      get: async key => { state.secretReads += 1; return state.secrets.get(key); },
      store: async (key, value) => { if (storeError) throw storeError; state.secrets.set(key, value); },
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


test('all service resolvers reject a different endpoint before reading or prompting for a credential', async t => {
  for (const alias of services) await t.test(alias, async () => {
    const state = load(alias, { stored: 'synthetic-saved-token' });
    for (const target of [undefined, { uri: new URL('https://example.com/mcp') },
      { uri: new URL(state.provider.provideMcpServerDefinitions()[0].uri.href + '?redirect=elsewhere') }]) {
      await assert.rejects(state.provider.resolveMcpServerDefinition(target), /Unexpected MCP server endpoint/);
    }
    assert.equal(state.secretReads, 0);
    assert.equal(state.prompts.length, 0);
    assert.equal(state.secrets.get(`${alias}.apiToken`), 'synthetic-saved-token');
  });
});

test('all service prompts cancel or reject blank input without saving a credential', async t => {
  for (const alias of services) await t.test(alias, async () => {
    for (const input of [undefined, '', '   ']) {
      const state = load(alias, { input });
      await assert.rejects(state.resolve(), /needs an Ace Data Cloud/);
      assert.equal(state.prompts.length, 1);
      assert.equal(state.prompts[0].password, true);
      assert.equal(state.secrets.size, 0);
      assert.equal(state.information.length, 0);
    }
  });
});

test('stored credentials resolve without prompting or adding a second Bearer prefix', async () => {
  for (const alias of ['suno', 'happyhorse', 'openai', 'acedatacloud']) {
    const state = load(alias, { stored: '  synthetic-stored-token  ' });
    const definition = await state.resolve();
    assert.equal(definition.headers.Authorization, 'Bearer synthetic-stored-token');
    assert.equal(state.prompts.length, 0);
  }
});


test('prompt and credential-store failures propagate without reporting a saved key', async () => {
  for (const alias of ['suno', 'seedance', 'happyhorse', 'openai', 'nanobanana']) {
    const promptFailure = load(alias, { inputError: new Error('synthetic input unavailable') });
    await assert.rejects(promptFailure.resolve(), /synthetic input unavailable/);
    assert.equal(promptFailure.secrets.size, 0);
    assert.equal(promptFailure.information.length, 0);
    const storeFailure = load(alias, { input: 'synthetic-test-key', storeError: new Error('synthetic credential store unavailable') });
    await assert.rejects(storeFailure.commands.get(`acedatacloud.${alias}.setApiToken`)(), /synthetic credential store unavailable/);
    assert.equal(storeFailure.secrets.size, 0);
    assert.equal(storeFailure.information.length, 0);
  }
});
