const expected = process.argv[2];
const endpoint = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery";
const payload = {
  filters: [{ criteria: [{ filterType: 7, value: "acedatacloud.mcp-toolbox" }] }],
  flags: 946, // Exclude versions that Marketplace has not validated yet.
};
function isValidatedVersion(extension, version) {
  return extension?.extensionName === "mcp-toolbox"
    && extension.publisher?.publisherName === "acedatacloud"
    && extension.versions?.some((item) => item.version === version && item.flags?.split(", ").includes("validated"));
}

async function verify(version) {
  if (!version) throw new Error("Expected Marketplace version is required");
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
    const extension = extensions.find((item) => item.extensionName === "mcp-toolbox" && item.publisher?.publisherName === "acedatacloud");
    if (isValidatedVersion(extension, version)) {
      console.log(`Marketplace verified: acedatacloud.mcp-toolbox ${version}`);
      return;
    }
    if (attempt < 59) await new Promise((resolve) => setTimeout(resolve, 15000));
  }
  throw new Error(`Marketplace version ${version} is not publicly visible`);
}

module.exports = { isValidatedVersion };
if (require.main === module) {
  verify(expected).catch((error) => { console.error(error.message); process.exitCode = 1; });
}
