const expected = process.argv[2];
if (!expected) throw new Error("Expected Marketplace version is required");
const endpoint = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery";
const payload = {
  filters: [{ criteria: [{ filterType: 7, value: "acedatacloud.mcp-toolbox" }] }],
  flags: 914,
};
(async () => {
  for (let attempt = 0; attempt < 20; attempt += 1) {
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
    if (extension?.versions?.some((item) => item.version === expected)) {
      console.log(`Marketplace verified: acedatacloud.mcp-toolbox ${expected}`);
      return;
    }
    if (attempt < 19) await new Promise((resolve) => setTimeout(resolve, 15000));
  }
  throw new Error(`Marketplace version ${expected} is not publicly visible`);
})().catch((error) => { console.error(error.message); process.exitCode = 1; });
