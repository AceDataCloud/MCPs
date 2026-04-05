"""Informational tools for ShortURL API."""

from core.server import mcp


@mcp.tool()
async def shorturl_get_usage_guide() -> str:
    """Get a comprehensive guide for using the ShortURL tools.

    Provides detailed information on how to use the ShortURL tools
    effectively, including parameters, examples, and best practices.

    Returns:
        Complete usage guide for ShortURL tools.
    """
    # Last updated: 2026-04-05
    return """# ShortURL Tools Usage Guide

## Available Tools

### URL Shortening
**shorturl_create** - Shorten a single URL
- url: The long URL to shorten (required, must start with http:// or https://)

**shorturl_batch_create** - Shorten multiple URLs at once
- urls: List of long URLs to shorten (max 10 per batch)

## Example Usage

### Shorten a Single URL
```
shorturl_create(url="https://platform.acedata.cloud/documents/a2303356-6672-4eb8-9778-75f55c998fe9")
```

**Response:**
```json
{
  "success": true,
  "data": {
    "url": "https://surl.id/1uHCs01xa5"
  }
}
```

### Batch Shorten Multiple URLs
```
shorturl_batch_create(urls=[
    "https://example.com/very-long-url-1",
    "https://example.com/very-long-url-2"
])
```

## Response Structure

### Successful Response
- **success**: `true` - indicates the request was successful
- **data.url**: The shortened URL (e.g., `https://surl.id/abc123`)

### Error Response
- **success**: `false` - indicates an error occurred
- **error.code**: Error code (e.g., `api_error`, `bad_request`)
- **error.message**: Human-readable error description
- **trace_id**: Request trace ID for debugging

## Notes
- The service is **free** (0 credits per request)
- Short URLs use the `surl.id` domain
- Short URLs are permanent and redirect to the original URL
- Only valid HTTP/HTTPS URLs can be shortened
- Rate limiting applies to prevent abuse
"""


@mcp.tool()
async def shorturl_get_api_info() -> str:
    """Get information about the ShortURL API service.

    Returns details about the API endpoint, pricing, and service capabilities.

    Returns:
        API information and service details.
    """
    # Last updated: 2026-04-05
    return """# ShortURL API Information

## Service Details

| Property     | Value                                  |
|-------------|----------------------------------------|
| Service     | Short URL (URL Shortener)              |
| Endpoint    | POST /shorturl                         |
| Base URL    | https://api.acedata.cloud              |
| Pricing     | Free (0 credits per request)           |
| Auth        | Bearer token required                  |
| Domain      | Short URLs use surl.id                 |
| Status      | Production                             |

## API Endpoint

```
POST https://api.acedata.cloud/shorturl
```

### Request Headers
| Header        | Value                    | Required |
|---------------|--------------------------|----------|
| accept        | application/json         | Yes      |
| authorization | Bearer {your_token}      | Yes      |
| content-type  | application/json         | Yes      |

### Request Body
| Field   | Type   | Description                    | Required |
|---------|--------|--------------------------------|----------|
| content | string | The long URL to shorten        | Yes      |

### Response
| Field       | Type    | Description                              |
|-------------|---------|------------------------------------------|
| success     | boolean | Whether the request was successful       |
| data.url    | string  | The shortened URL                        |

## Error Codes

| Code                 | Status | Description                              |
|---------------------|--------|------------------------------------------|
| token_mismatched    | 400    | Token does not match the API             |
| api_not_implemented | 400    | API is not implemented                   |
| bad_request         | 400    | Invalid request parameters               |
| no_token            | 400    | No authentication token provided         |
| disabled            | 400    | Application has been disabled            |
| invalid_token       | 401    | Invalid or expired token                 |
| token_expired       | 401    | Authentication token has expired         |
| used_up             | 403    | Insufficient balance                     |
| no_api              | 404    | API not found                            |
| too_many_requests   | 429    | Rate limit exceeded                      |
| api_error           | 500    | Internal server error                    |

## Get Your API Token

1. Visit https://platform.acedata.cloud
2. Sign up or log in
3. Navigate to Short URL API page
4. Click "Acquire" to get your token
"""
