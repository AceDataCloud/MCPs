"""Prompt templates for SERP MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def serp_search_guide() -> str:
    """Guide for choosing the right SERP tool for search tasks."""
    return """# Google SERP Search Guide

When the user wants to search for information, choose the appropriate tool based on their needs:

## Regular Web Search
**Tool:** `serp_google_search`
**Use when:**
- User wants general information
- Looking for websites, articles, or documentation
- Research on any topic

**Example:** "What is machine learning?"
→ Call `serp_google_search` with query="machine learning"

## Image Search
**Tool:** `serp_google_images`
**Use when:**
- User wants pictures or photos
- Looking for visual content
- "Show me images of..."

**Example:** "Show me pictures of the Eiffel Tower"
→ Call `serp_google_images` with query="Eiffel Tower"

## News Search
**Tool:** `serp_google_news`
**Use when:**
- User wants current events
- Looking for recent news articles
- "What's happening with...", "Latest news about..."

**Example:** "What's the latest news about AI?"
→ Call `serp_google_news` with query="AI", time_range="qdr:d"

## Video Search
**Tool:** `serp_google_videos`
**Use when:**
- User wants video content
- Looking for tutorials, reviews, entertainment
- "Find videos about...", "How to... video"

**Example:** "Find videos about cooking pasta"
→ Call `serp_google_videos` with query="cooking pasta tutorial"

## Local Places Search
**Tool:** `serp_google_places`
**Use when:**
- User wants local businesses
- Looking for restaurants, shops, services
- "Find ... near me", "Best ... in [city]"

**Example:** "Find Italian restaurants in New York"
→ Call `serp_google_places` with query="Italian restaurants New York"

## Map Search
**Tool:** `serp_google_maps`
**Use when:**
- User wants location information
- Looking for addresses, directions
- Geographic searches

**Example:** "Where is Central Park?"
→ Call `serp_google_maps` with query="Central Park New York"

## Important Notes:
1. Always use specific, well-formed queries
2. Use country/language parameters for localized results
3. Use time_range for recent/trending topics
4. Consider pagination for comprehensive research
"""


@mcp.prompt()
def serp_workflow_examples() -> str:
    """Common workflow examples for SERP search tasks."""
    return """# SERP Search Workflow Examples

## Workflow 1: Research a Topic
1. User: "Tell me about quantum computing"
2. Call `serp_google_search(query="quantum computing overview")`
3. Present the knowledge graph and top results
4. If user wants more: search for specific subtopics

## Workflow 2: Current Events Research
1. User: "What's happening with climate change?"
2. Call `serp_google_news(query="climate change", time_range="qdr:w")`
3. Present recent news articles
4. Follow up with specific event searches if needed

## Workflow 3: Visual Content Search
1. User: "Show me modern architecture buildings"
2. Call `serp_google_images(query="modern architecture buildings")`
3. Present image results with URLs
4. User can request more specific styles

## Workflow 4: Local Business Search
1. User: "Find a good sushi restaurant in San Francisco"
2. Call `serp_google_places(query="best sushi restaurant San Francisco")`
3. Present place results with ratings
4. Follow up with specific restaurant searches

## Workflow 5: Learning/Tutorial Search
1. User: "How do I learn Python programming?"
2. Call `serp_google_search(query="learn Python programming beginner")`
3. Also call `serp_google_videos(query="Python programming tutorial beginner")`
4. Present both web resources and video tutorials

## Workflow 6: International Search
1. User: "Find news about Japan in Japanese"
2. Call `serp_google_news(query="Japan news", country="jp", language="ja")`
3. Present localized results

## Tips:
- Combine multiple search types for comprehensive results
- Use time filters for time-sensitive queries
- Localize searches when regional relevance matters
- Paginate for thorough research
"""


@mcp.prompt()
def serp_query_tips() -> str:
    """Tips for writing effective search queries."""
    return """# SERP Query Writing Tips

## Effective Query Writing

### Be Specific
Instead of broad queries, use specific terms:
- ❌ "cars"
- ✅ "electric vehicle comparison 2024"

### Use Keywords
Focus on important keywords:
- ❌ "I want to know how to make bread at home"
- ✅ "homemade bread recipe"

### Include Context
Add relevant context for better results:
- ❌ "best practices"
- ✅ "software development best practices 2024"

### Use Quotes for Exact Matches
When searching for exact phrases:
- "machine learning" algorithms (exact phrase + keyword)

## Query Patterns by Intent

### Informational Queries
- "What is [topic]"
- "[topic] explained"
- "[topic] guide"

### Comparison Queries
- "[A] vs [B]"
- "[A] compared to [B]"
- "best [category] [year]"

### How-To Queries
- "how to [action]"
- "[action] tutorial"
- "[action] step by step"

### News Queries
- "[topic] news"
- "latest [topic]"
- "[topic] [year]"

### Local Queries
- "[business type] near [location]"
- "best [category] in [city]"
- "[service] [neighborhood]"

## Combining with Parameters

### For Recent Information
Query: "AI developments"
+ time_range: "qdr:w" (past week)

### For Localized Results
Query: "weather forecast"
+ country: "uk"
+ language: "en"

### For Comprehensive Research
Query: "renewable energy"
+ number: 20 (more results)
+ Multiple search types (search, news, videos)

## Common Pitfalls to Avoid
1. Overly long queries (keep it concise)
2. Stop words only ("the", "a", "is")
3. Typos (affects result quality)
4. Missing context (too ambiguous)
"""
