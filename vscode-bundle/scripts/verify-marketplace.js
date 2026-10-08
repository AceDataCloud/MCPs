const expected = process.argv[2];
const target = process.argv[3] || "mcp-toolbox";
const endpoint = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery";
function isValidatedVersion(extension, version, extensionName = "mcp-toolbox") {
  return extension?.extensionName === extensionName
    && extension.publisher?.publisherName === "acedatacloud"
    && extension.versions?.some((item) => item.version === version && item.flags?.split(", ").includes("validated"));
}

async function verify(version, extensionName) {
  if (!version) throw new Error("Expected Marketplace version is required");
  if (!["mcp-toolbox", "chat-models"].includes(extensionName)) throw new Error("Unsupported Marketplace extension");
  const payload = {
    filters: [{ criteria: [{ filterType: 7, value: `acedatacloud.${extensionName}` }] }],
    flags: 946, // Exclude versions that Marketplace has not validated yet.
  };
  for (let attempt = 0; attempt < 60; attempt += 1) {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json;api-version=3.0-preview.1" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(30000),
    });
    if (!response.ok) throw new Error(`Marketplace query returned ${response.status}`);
    const data = await response.json();
    const extensions = data.results?.[0]?.extensions || [];
    const extension = extensions.find((item) => item.extensionName === extensionName && item.publisher?.publisherName === "acedatacloud");
    if (isValidatedVersion(extension, version, extensionName)) {
      console.log(`Marketplace verified: acedatacloud.${extensionName} ${version}`);
      return;
    }
    if (attempt < 59) await new Promise((resolve) => setTimeout(resolve, 15000));
  }
  throw new Error(`Marketplace version ${version} is not publicly visible`);
}

module.exports = { isValidatedVersion };
if (require.main === module) {
  verify(expected, target).catch((error) => { console.error(error.message); process.exitCode = 1; });
}
