const vscode = require("vscode");
const catalog = require("./servers.json");

const PROVIDER_ID = "acedatacloud.bundle";
const COMMAND_PREFIX = "acedatacloud.bundle.";
const API_KEY = "bundle.apiKey";
const PLATFORM_TOKEN = "bundle.platformToken";

function selectedServices() {
  const selected = vscode.workspace
    .getConfiguration("acedatacloud.bundle")
    .get("services", []);
  return catalog.filter((service) => selected.includes(service.id));
}

async function promptCredential(context, key, platform, label) {
  const token = await vscode.window.showInputBox({
    title: label,
    prompt: platform
      ? "Enter a platform token from https://platform.acedata.cloud/console/platform-tokens. Account tools use this token separately from API keys."
      : "Enter an API key from https://platform.acedata.cloud/console/applications. Saved securely in VS Code SecretStorage.",
    password: true,
    ignoreFocusOut: true,
  });
  const value = token?.trim();
  if (!value) return undefined;
  await context.secrets.store(key, value);
  return value;
}

async function readCredential(context, service) {
  if (service.credential === "platform") {
    const saved = await context.secrets.get(PLATFORM_TOKEN);
    return saved?.trim() || process.env.ACEDATACLOUD_PLATFORM_TOKEN?.trim();
  }
  const override = await context.secrets.get(`bundle.service.${service.id}`);
  const shared = await context.secrets.get(API_KEY);
  return override?.trim() || shared?.trim() || process.env.ACEDATACLOUD_API_TOKEN?.trim();
}

function activate(context) {
  const changed = new vscode.EventEmitter();
  const register = (name, handler) =>
    context.subscriptions.push(vscode.commands.registerCommand(COMMAND_PREFIX + name, handler));

  context.subscriptions.push(changed);
  register("selectServices", async () => {
    const selected = new Set(selectedServices().map((service) => service.id));
    const choices = await vscode.window.showQuickPick(
      catalog.map((service) => ({
        label: service.label,
        description: service.credential === "platform" ? "Separate platform token" : service.id,
        picked: selected.has(service.id),
        id: service.id,
      })),
      { canPickMany: true, title: "Choose your Ace Data Cloud MCP services" },
    );
    if (!choices) return;
    await vscode.workspace.getConfiguration("acedatacloud.bundle").update(
      "services", choices.map((choice) => choice.id), vscode.ConfigurationTarget.Global,
    );
  });
  register("setApiKey", () => promptCredential(context, API_KEY, false, "Ace Data Cloud shared API key"));
  register("setPlatformToken", () => promptCredential(context, PLATFORM_TOKEN, true, "Ace Data Cloud account platform token"));
  register("setServiceApiKey", async () => {
    const service = await vscode.window.showQuickPick(
      catalog.filter((item) => item.credential === "api").map((item) => ({ label: item.label, id: item.id })),
      { title: "Choose the service for this API key" },
    );
    if (service) {
      await promptCredential(context, `bundle.service.${service.id}`, false, `${service.label} API key`);
    }
  });
  register("clearCredentials", async () => {
    await Promise.all([
      API_KEY, PLATFORM_TOKEN, ...catalog.map((service) => `bundle.service.${service.id}`),
    ].map((key) => context.secrets.delete(key)));
    vscode.window.showInformationMessage("Ace Data Cloud: saved credentials cleared. Environment variables, if set, still apply.");
  });

  const provider = {
    onDidChangeMcpServerDefinitions: changed.event,
    provideMcpServerDefinitions: () => selectedServices().map((service) =>
      new vscode.McpHttpServerDefinition(`${service.label} · Ace Data Cloud`, vscode.Uri.parse(service.url)),
    ),
    resolveMcpServerDefinition: async (server) => {
      const service = selectedServices().find((item) => item.url === server.uri.toString());
      if (!service) throw new Error("Unknown or disabled Ace Data Cloud MCP endpoint.");
      let token = await readCredential(context, service);
      if (!token) {
        const platform = service.credential === "platform";
        token = await promptCredential(
          context, platform ? PLATFORM_TOKEN : `bundle.service.${service.id}`, platform,
          `${service.label} ${platform ? "platform token" : "API key"}`,
        );
      }
      if (!token) throw new Error(`${service.label} needs a credential before connecting.`);
      return new vscode.McpHttpServerDefinition(server.label, vscode.Uri.parse(service.url), {
        Authorization: `Bearer ${token}`,
      });
    },
  };
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((event) => {
      if (event.affectsConfiguration("acedatacloud.bundle.services")) changed.fire();
    }),
    context.secrets.onDidChange((event) => {
      if (event.key.startsWith("bundle.")) changed.fire();
    }),
    vscode.lm.registerMcpServerDefinitionProvider(PROVIDER_ID, provider),
  );
  return { provider };
}

module.exports = { activate };
