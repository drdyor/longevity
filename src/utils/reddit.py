"""Reddit data collection utilities using PRAW."""
import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict
import praw
from dotenv import load_dotenv

load_dotenv()


def get_reddit_client() -> praw.Reddit:
    """Initialize and return authenticated Reddit client."""
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )


def fetch_posts(
    subreddit_name: str = "longevity",
    days_back: int = 365,
    max_posts: int = 10000
) -> List[Dict]:
    """
    Fetch posts from a subreddit within the specified time window.
    
    Args:
        subreddit_name: Name of the subreddit (default: "longevity")
        days_back: How many days back to fetch (default: 365)
        max_posts: Maximum number of posts to fetch (default: 10000)
    
    Returns:
        List of dictionaries containing post data
    """
    reddit = get_reddit_client()
    sub = reddit.subreddit(subreddit_name)
    
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    
    rows = []
    count = 0
    
    print(f"Fetching posts from r/{subreddit_name} (last {days_back} days)...")
    
    for post in sub.new(limit=None):
        created = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
        
        if created < cutoff:
            break
        
        rows.append({
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "url": post.url,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": created.isoformat(),
            "author": str(post.author),
        })
        
        count += 1
        if count % 100 == 0:
            print(f"  Fetched {count} posts...")
        
        if count >= max_posts:
            break
    
    print(f"✓ Fetched {len(rows)} posts")
    return rows
