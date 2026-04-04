"""Prompt templates for ShortURL MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def shorturl_guide() -> str:
    """Guide for choosing the right ShortURL tool for URL shortening tasks."""
    return """# ShortURL Guide

When the user wants to shorten a URL or create short links, use the appropriate tool:

## Single URL Shortening
**Tool:** `shorturl_create`
**Use when:**
- User wants to shorten a single URL
- User shares a long link and wants it shortened
- User needs a clean link for sharing

**Example:** "Shorten this URL: https://example.com/very-long-path"
→ Call `shorturl_create` with url="https://example.com/very-long-path"

## Batch URL Shortening
**Tool:** `shorturl_batch_create`
**Use when:**
- User has multiple URLs to shorten
- User wants to shorten a list of links
- Bulk URL shortening tasks

**Example:** "Shorten these URLs: url1, url2, url3"
→ Call `shorturl_batch_create` with urls=["url1", "url2", "url3"]

## API Information
**Tool:** `shorturl_get_api_info`
**Use when:**
- User asks about the ShortURL API details
- User wants to know about pricing or limits
- User needs error code reference

## Usage Guide
**Tool:** `shorturl_get_usage_guide`
**Use when:**
- User wants to understand how to use the tools
- User needs examples or best practices

## Important Notes:
1. Only valid HTTP/HTTPS URLs can be shortened
2. The service is free (0 credits per request)
3. Short URLs use the `surl.id` domain and are permanent
4. Rate limiting applies - don't make excessive requests
5. Bearer token authentication is required
"""


@mcp.prompt()
def shorturl_workflow_examples() -> str:
    """Common workflow examples for ShortURL tasks."""
    return """# ShortURL Workflow Examples

## Workflow 1: Shorten a Single Link
1. User: "Make this link shorter: https://platform.acedata.cloud/documents/a2303356-6672-4eb8-9778-75f55c998fe9"
2. Call `shorturl_create(url="https://platform.acedata.cloud/documents/a2303356-6672-4eb8-9778-75f55c998fe9")`
3. Return the short URL: https://surl.id/abc123

## Workflow 2: Prepare Links for Social Media
1. User: "I need to share these links on Twitter, make them shorter"
2. Collect all URLs from the user
3. Call `shorturl_batch_create(urls=[...])` with all URLs
4. Present the mapping of original → short URLs

## Workflow 3: Create Clean Documentation Links
1. User: "I'm writing a document and need clean links for these references"
2. Gather all reference URLs
3. Shorten each one using `shorturl_batch_create`
4. Present formatted results for easy copy-paste

## Workflow 4: Marketing Campaign Links
1. User: "Create short links for my campaign landing pages"
2. Collect all campaign URLs
3. Use `shorturl_batch_create` for efficiency
4. Present results in a table format

## Tips:
- Use batch shortening for 2+ URLs to be efficient
- Verify URLs are valid before shortening
- Short URLs are permanent - they won't expire
- The service is free, no credit consumption
"""


@mcp.prompt()
def shorturl_best_practices() -> str:
    """Best practices for URL shortening."""
    return """# URL Shortening Best Practices

## When to Shorten URLs
- **Social media posts** - Character limits make short URLs essential
- **Email campaigns** - Clean URLs look more professional
- **Print materials** - Short URLs are easier to type manually
- **Chat messages** - Long URLs can break in messaging apps
- **QR codes** - Shorter URLs generate simpler QR codes
- **Documentation** - Clean links in technical docs

## URL Guidelines

### Valid URLs
- Must start with `http://` or `https://`
- Must be a complete, valid URL
- Can contain query parameters and fragments

### Examples
- ✅ `https://example.com/path?param=value`
- ✅ `http://example.com/page#section`
- ✅ `https://example.com/very/long/nested/path/to/resource`
- ❌ `example.com` (missing scheme)
- ❌ `ftp://example.com` (not HTTP/HTTPS)
- ❌ `` (empty string)

## Batch Processing Tips
- Maximum 10 URLs per batch call
- For more than 10 URLs, split into multiple batches
- Auth errors will stop the batch - fix authentication first
- Each URL in the batch is processed independently

## Error Handling
- If you get a 401 error, check your API token
- If you get a 429 error, wait before retrying
- If you get a 500 error, the upstream service may be temporarily unavailable
"""
