from mcp.server.fastmcp import FastMCP  # import official python SDK
import feedparser
import logging
import sys
import ssl
import certifi

# SET CERTIFICATES BEFORE ANYTHING ELSE
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
mcp = FastMCP("RSSFeedSearch")

@mcp.tool()
def fetch_google_blog_feed(query: str, max_results: int=5) -> list:
    """
    Fetch RSS feed entries from Google Blog Search based on a query.
    args:
        query: str, the search query - title or description
        max_results: int, maximum number of results to return
    returns: list of blog feed entries matching query
    """
    feed = feedparser.parse("https://blog.google/rss/")
    logging.info(f"Feed bozo flag: {feed.bozo}")
    logging.info(f"Number of entries: {len(feed.entries)}")
        
    results = []
    query_lower = query.lower()
    for entry in feed.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")

        if query_lower in title.lower() or query_lower in description.lower():
            results.append({
                "title": title,
                "link": entry.get("link", ""),
                "description": description
            })
        if len(results) >= max_results:
            break
    
    return results or [{"message": "no matching entries found."}]

@mcp.tool()
def fetch_youtube_feed(query: str, max_results: int=5) -> list:
    """
    Fetch RSS feed entries from a YouTube channel based on a query.
    args:
        query: str, the search query - title or description
        max_results: int, maximum number of results to return
    returns: list of video feed entries matching query
    """
    feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw")
    logging.info(f"Feed bozo flag: {feed.bozo}")
    
    results = []
    for entry in feed.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")

        if query.lower() in title.lower() or query.lower() in description.lower():
            results.append({
                "title": title,
                "link": entry.get("link", ""),
                "description": description
            })
        if len(results) >= max_results:
            break
    
    return results or [{"message": "no matching entries found."}]    
    
if __name__ == "__main__":
    mcp.run()  # stdio transport
