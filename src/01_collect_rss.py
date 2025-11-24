"""
Reddit data collection using RSS feeds (NO API credentials needed!)

This approach is inspired by Manus and uses Reddit's public RSS feeds,
which require NO authentication and have NO rate limits.
"""
import feedparser
import pandas as pd
from datetime import datetime
import time
import os


def fetch_posts_via_rss(subreddit: str = "longevity", keywords: list = None, max_posts: int = 100):
    """
    Fetch posts from Reddit using RSS feeds (NO API needed!)
    
    Args:
        subreddit: Name of subreddit
        keywords: Optional list of keywords to filter posts
        max_posts: Maximum posts to return (RSS gives ~25 per request)
    
    Returns:
        List of post dictionaries
    """
    # Reddit RSS URL - no authentication needed!
    url = f"https://www.reddit.com/r/{subreddit}.rss"
    
    print(f"Fetching from: {url}")
    print("(No API credentials needed - using public RSS feed)")
    
    try:
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print(f"⚠️ No posts found in feed")
            return []
        
        posts = []
        for entry in feed.entries:
            # Extract data from RSS entry
            post_id = entry.id.split('/')[-1] if hasattr(entry, 'id') else f"rss_{len(posts)}"
            
            # Filter by keywords if provided
            if keywords:
                text = (entry.title + ' ' + entry.get('summary', '')).lower()
                if not any(kw.lower() in text for kw in keywords):
                    continue
            
            posts.append({
                "id": post_id,
                "title": entry.title,
                "selftext": entry.get('summary', ''),
                "url": entry.link,
                "score": 0,  # RSS doesn't include scores
                "num_comments": 0,  # RSS doesn't include comment count
                "created_utc": entry.get('published', datetime.now().isoformat()),
                "author": entry.get('author', 'unknown')
            })
            
            if len(posts) >= max_posts:
                break
        
        return posts
        
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []


def fetch_multiple_subreddits(subreddits: list, keywords: list = None):
    """Fetch from multiple subreddits."""
    all_posts = []
    
    for sub in subreddits:
        print(f"\nFetching r/{sub}...")
        posts = fetch_posts_via_rss(sub, keywords)
        all_posts.extend(posts)
        print(f"  Found {len(posts)} posts")
        time.sleep(2)  # Be polite
    
    return all_posts


# Example keywords for longevity topics
LONGEVITY_KEYWORDS = [
    'rapamycin', 'NAD+', 'NMN', 'metformin', 'GLP-1', 'semaglutide',
    'peptide', 'MOTS-C', 'BPC-157', 'fasting', 'autophagy', 'senolytic',
    'mitochondria', 'resveratrol', 'spermidine', 'berberine'
]


if __name__ == "__main__":
    # Example: Fetch from multiple longevity-related subreddits
    subreddits = ['longevity', 'Biohacking', 'Peptides', 'Nootropics']
    
    print("=" * 60)
    print("Reddit RSS Collection (Manus Method - No API Needed!)")
    print("=" * 60)
    
    all_posts = fetch_multiple_subreddits(subreddits, LONGEVITY_KEYWORDS)
    
    if all_posts:
        # Save to CSV
        df = pd.DataFrame(all_posts)
        output_dir = "data/raw"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_file = os.path.join(output_dir, f"posts_rss_{timestamp}.csv")
        df.to_csv(output_file, index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"✓ Collected {len(all_posts)} posts from {len(subreddits)} subreddits")
        print(f"✓ Saved to: {output_file}")
        print(f"✓ NO API credentials needed!")
    else:
        print("\n⚠️ No posts collected")
