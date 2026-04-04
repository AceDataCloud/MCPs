"""Informational tools for SERP API."""

from core.server import mcp


@mcp.tool()
async def serp_list_search_types() -> str:
    """List all available Google search types.

    Shows all available search types and their use cases.
    Use this to understand which search type to use for your query.

    Returns:
        Table of all search types with descriptions.
    """
    return """Available Google Search Types:

| Type      | Description                                    | Use Case                           |
|-----------|------------------------------------------------|------------------------------------|
| search    | Regular web search (default)                   | General queries, finding websites  |
| images    | Image search                                   | Finding pictures, photos, graphics |
| news      | News articles                                  | Current events, recent news        |
| maps      | Map/location results                           | Finding locations on maps          |
| places    | Local businesses and places                    | Restaurants, shops, services       |
| videos    | Video results                                  | YouTube, video content             |

Example Usage:
- "What is AI?" → type: search
- "Pictures of cats" → type: images
- "Latest tech news" → type: news
- "Coffee shops near me" → type: places
- "How to cook pasta video" → type: videos
"""


@mcp.tool()
async def serp_list_countries() -> str:
    """List commonly used country codes for Google search.

    Shows common country codes that can be used to localize search results.

    Returns:
        Table of country codes and their countries.
    """
    return """Common Country Codes for Google Search:

| Code | Country           | Code | Country           |
|------|-------------------|------|-------------------|
| us   | United States     | jp   | Japan             |
| uk   | United Kingdom    | kr   | South Korea       |
| cn   | China             | in   | India             |
| de   | Germany           | br   | Brazil            |
| fr   | France            | mx   | Mexico            |
| es   | Spain             | it   | Italy             |
| ca   | Canada            | au   | Australia         |
| ru   | Russia            | nl   | Netherlands       |
| sg   | Singapore         | hk   | Hong Kong         |
| tw   | Taiwan            | th   | Thailand          |

Usage: Pass the country code to the `country` parameter.
Example: serp_google_search(query="news", country="uk")
"""


@mcp.tool()
async def serp_list_languages() -> str:
    """List commonly used language codes for Google search.

    Shows common language codes that can be used to get results in specific languages.

    Returns:
        Table of language codes and their languages.
    """
    return """Common Language Codes for Google Search:

| Code    | Language              | Code    | Language              |
|---------|----------------------|---------|----------------------|
| en      | English              | ja      | Japanese             |
| zh-cn   | Chinese (Simplified) | ko      | Korean               |
| zh-tw   | Chinese (Traditional)| hi      | Hindi                |
| es      | Spanish              | pt      | Portuguese           |
| fr      | French               | ru      | Russian              |
| de      | German               | ar      | Arabic               |
| it      | Italian              | th      | Thai                 |
| nl      | Dutch                | vi      | Vietnamese           |
| pl      | Polish               | tr      | Turkish              |

Usage: Pass the language code to the `language` parameter.
Example: serp_google_search(query="news", language="zh-cn")
"""


@mcp.tool()
async def serp_list_time_ranges() -> str:
    """List available time range filters for Google search.

    Shows all time range options that can be used to filter results by date.

    Returns:
        Table of time range codes and their meanings.
    """
    return """Time Range Filters for Google Search:

| Code    | Time Range   | Description                    |
|---------|--------------|--------------------------------|
| qdr:h   | Past Hour    | Results from the last hour     |
| qdr:d   | Past Day     | Results from the last 24 hours |
| qdr:w   | Past Week    | Results from the last 7 days   |
| qdr:m   | Past Month   | Results from the last 30 days  |
| (none)  | Any Time     | No time restriction (default)  |

Usage: Pass the time range code to the `time_range` parameter.
Example: serp_google_search(query="AI news", time_range="qdr:d")

Note: Time range is most useful for:
- News searches (recent events)
- Trending topics
- Time-sensitive information
"""


@mcp.tool()
async def serp_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Google SERP tools.

    Provides detailed information on how to use the SERP search tools
    effectively, including parameters, examples, and best practices.

    Returns:
        Complete usage guide for SERP tools.
    """
    return """# Google SERP Tools Usage Guide

## Available Tools

### Main Search Tool
**serp_google_search** - Flexible search with all options
- query: Search query (required)
- search_type: search, images, news, maps, places, videos
- country: Country code (us, uk, cn, etc.)
- language: Language code (en, zh-cn, etc.)
- time_range: Time filter (qdr:h, qdr:d, qdr:w, qdr:m)
- number: Results per page (default: 10)
- page: Page number (default: 1)

### Specialized Tools (Shortcuts)
- **serp_google_images** - Image search
- **serp_google_news** - News search
- **serp_google_videos** - Video search
- **serp_google_places** - Local places/businesses
- **serp_google_maps** - Map locations

## Example Usage

### Basic Web Search
```
serp_google_search(query="artificial intelligence")
```

### News Search with Time Filter
```
serp_google_news(query="tech news", time_range="qdr:d")
```

### Localized Search
```
serp_google_search(
    query="best restaurants",
    country="uk",
    language="en"
)
```

### Image Search
```
serp_google_images(query="sunset photography")
```

### Paginated Results
```
serp_google_search(query="python tutorials", number=20, page=2)
```

## Response Contents

### Regular Search (type: search)
- **knowledge_graph**: Entity information (company, person, etc.)
- **answer_box**: Direct answers
- **organic**: Regular search results
- **people_also_ask**: Related questions
- **related_searches**: Related queries

### Image Search (type: images)
- **images**: Image results with URLs and thumbnails

### News Search (type: news)
- **news**: News articles with source and date

### Video Search (type: videos)
- **videos**: Video results with duration and source

### Places Search (type: places)
- **places**: Local business/place information

## Best Practices

1. **Be specific**: More specific queries yield better results
2. **Use localization**: Set country/language for relevant results
3. **Time filtering**: Use for news and current events
4. **Pagination**: Use number/page for browsing many results
5. **Choose right type**: Use specialized types for specific content

## Credits Note
- Standard searches (10 results): 1 credit
- Extended results (>10): May cost additional credits
"""
