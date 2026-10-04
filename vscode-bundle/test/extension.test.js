const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const catalog = require("../servers.json");
const manifest = require("../package.json");

function harness({ selected = ["suno", "acedatacloud"], saved = {}, env = {}, input } = {}) {
  const secrets = new Map(Object.entries(saved));
  const commands = new Map();
  const listeners = {};
  const prompts = [];
  let provider;
  class EventEmitter {
    event = () => ({ dispose() {} });
    fire() { this.fired = true; }
    dispose() {}
  }
  class McpHttpServerDefinition {
    constructor(label, uri, headers = {}) {
      Object.assign(this, { label, uri, headers });
    }
  }
  const vscode = {
    EventEmitter, McpHttpServerDefinition,
    Uri: { parse: (url) => ({ toString: () => url }) },
    ConfigurationTarget: { Global: 1 },
    workspace: {
      getConfiguration: () => ({ get: () => selected, update: async (_, values) => { selected = values; } }),
      onDidChangeConfiguration: (fn) => { listeners.configuration = fn; return { dispose() {} }; },
    },
    window: {
      showInputBox: async (options) => { prompts.push(options); return input; },
      showQuickPick: async () => undefined,
      showInformationMessage() {},
    },
    commands: { registerCommand: (id, fn) => { commands.set(id, fn); return { dispose() {} }; } },
    lm: { registerMcpServerDefinitionProvider: (id, value) => {
      assert.equal(id, "acedatacloud.bundle"); provider = value; return { dispose() {} };
    } },
  };
  const context = {
    subscriptions: [],
    secrets: {
      get: async (key) => secrets.get(key),
      store: async (key, value) => secrets.set(key, value),
      delete: async (key) => secrets.delete(key),
      onDidChange: (fn) => { listeners.secrets = fn; return { dispose() {} }; },
    },
  };
  const sandbox = {
    require: (id) => id === "vscode" ? vscode : catalog,
    module: { exports: {} }, process: { env },
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../extension.js"), "utf8"), sandbox);
  sandbox.module.exports.activate(context);
  return { provider, commands, prompts, secrets, vscode };
}

test("catalog, configuration and defaults agree and exclude retired services", () => {
  const setting = manifest.contributes.configuration.properties["acedatacloud.bundle.services"];
  assert.equal(new Set(catalog.map((s) => s.id)).size, catalog.length);
  assert.ok(catalog.length > 0);
  assert.equal(manifest.name, "mcp-toolbox");
  assert.equal(manifest.displayName, "Ace Data Cloud MCP");
  assert.deepEqual(setting.items.enum, catalog.map((s) => s.id));
  assert.ok(setting.default.every((id) => catalog.some((s) => s.id === id)));
  assert.ok(!catalog.some((s) => s.id === "sora"));
  assert.ok(!manifest.contributes.mcpServers);
  for (const service of catalog) {
    const url = new URL(service.url);
    assert.equal(url.protocol, "https:");
    assert.ok(url.hostname === "mcp.acedata.cloud" || url.hostname.endsWith(".mcp.acedata.cloud"));
    assert.equal(url.pathname, "/mcp");
  }
});

test("server discovery exposes only selected services without credentials", () => {
  const { provider } = harness();
  const definitions = provider.provideMcpServerDefinitions();
  assert.equal(definitions.length, 2);
  assert.ok(definitions.every((s) => Object.keys(s.headers).length === 0));
  assert.equal(harness({ selected: [] }).provider.provideMcpServerDefinitions().length, 0);
});

test("API and account credentials never cross service boundaries", async () => {
  const { provider } = harness({ saved: { "bundle.apiKey": "api-secret", "bundle.platformToken": "account-secret" } });
  for (const server of provider.provideMcpServerDefinitions()) {
    const result = await provider.resolveMcpServerDefinition(server);
    assert.equal(result.headers.Authorization, server.uri.toString() === "https://mcp.acedata.cloud/mcp" ? "Bearer account-secret" : "Bearer api-secret");
  }
});

test("per-service key overrides saved shared key and environment", async () => {
  const { provider } = harness({ selected: ["suno"], saved: { "bundle.service.suno": "service", "bundle.apiKey": "shared" }, env: { ACEDATACLOUD_API_TOKEN: "env" } });
  const result = await provider.resolveMcpServerDefinition(provider.provideMcpServerDefinitions()[0]);
  assert.equal(result.headers.Authorization, "Bearer service");
});

test("account server never falls back to an API key", async () => {
  const { provider } = harness({ selected: ["acedatacloud"], saved: { "bundle.apiKey": "api-only" }, env: { ACEDATACLOUD_API_TOKEN: "also-api" } });
  await assert.rejects(() => provider.resolveMcpServerDefinition(provider.provideMcpServerDefinitions()[0]), /needs a credential/);
});

test("unknown endpoints cannot receive a credential", async () => {
  const { provider, vscode } = harness({ saved: { "bundle.apiKey": "secret" } });
  await assert.rejects(() => provider.resolveMcpServerDefinition({ label: "Other", uri: vscode.Uri.parse("https://example.com/mcp") }), /Unknown or disabled/);
});

test("cancelled credential prompt fails without saving or connecting", async () => {
  const { provider, secrets } = harness({ selected: ["suno"] });
  await assert.rejects(() => provider.resolveMcpServerDefinition(provider.provideMcpServerDefinitions()[0]), /needs a credential/);
  assert.equal(secrets.size, 0);
});

test("credential prompt saves to SecretStorage and clear removes all bundle keys", async () => {
  const { provider, secrets, commands, prompts } = harness({ selected: ["suno"], input: "  new-key  " });
  const result = await provider.resolveMcpServerDefinition(provider.provideMcpServerDefinitions()[0]);
  assert.equal(result.headers.Authorization, "Bearer new-key");
  assert.equal(secrets.get("bundle.service.suno"), "new-key");
  assert.equal(prompts[0].password, true);
  await commands.get("acedatacloud.bundle.clearCredentials")();
  assert.equal(secrets.size, 0);
});
