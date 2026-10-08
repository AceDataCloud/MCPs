const test = require("node:test");
const assert = require("node:assert/strict");
const { isValidatedVersion } = require("../scripts/verify-marketplace.js");

function entry(flags, version = "2026.1004.24201") {
  return { extensionName: "mcp-toolbox", publisher: { publisherName: "acedatacloud" }, versions: [{ version, flags }] };
}

test("upload acceptance without validation is not a completed release", () => {
  assert.equal(isValidatedVersion(entry("none"), "2026.1004.24201"), false);
  assert.equal(isValidatedVersion(entry("validationFailed"), "2026.1004.24201"), false);
  assert.equal(isValidatedVersion(entry("validated", "older"), "2026.1004.24201"), false);
});

test("only the expected validated publisher and version confirms release", () => {
  assert.equal(isValidatedVersion(entry("validated"), "2026.1004.24201"), true);
  const other = entry("validated");
  other.publisher.publisherName = "other";
  assert.equal(isValidatedVersion(other, "2026.1004.24201"), false);
});

test("chat model publication requires its own validated Marketplace entry", () => {
  const model = { extensionName: "chat-models", publisher: { publisherName: "acedatacloud" }, versions: [{ version: "0.1.0", flags: "validated" }] };
  assert.equal(isValidatedVersion(model, "0.1.0", "chat-models"), true);
  assert.equal(isValidatedVersion(model, "0.1.0", "mcp-toolbox"), false);
  assert.equal(isValidatedVersion(model, "0.1.1", "chat-models"), false);
});
