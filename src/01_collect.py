"""
Step 1: Collect posts from r/longevity

This script fetches the last year of posts from r/longevity using the Reddit API
and saves them to a CSV file.
"""
import os
import sys
from datetime import datetime
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.reddit import fetch_posts


def main():
    """Main collection function."""
    print("=" * 60)
    print("Reddit Data Collection - r/longevity")
    print("=" * 60)
    
    # Configuration
    SUBREDDIT = "longevity"
    DAYS_BACK = 365
    MAX_POSTS = 10000
    
    # Output configuration
    DATA_DIR = os.getenv("DATA_DIR", "data/raw")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(DATA_DIR, f"posts_{timestamp}.csv")
    
    # Fetch posts
    try:
        posts = fetch_posts(
            subreddit_name=SUBREDDIT,
            days_back=DAYS_BACK,
            max_posts=MAX_POSTS
        )
        
        if not posts:
            print("⚠ No posts fetched. Check your Reddit API credentials.")
            return 1
        
        # Save to CSV
        df = pd.DataFrame(posts)
        df.to_csv(output_file, index=False)
        
        print(f"\n✓ Saved {len(df)} posts to: {output_file}")
        print(f"  Date range: {df['created_utc'].min()} to {df['created_utc'].max()}")
        print(f"  Total score: {df['score'].sum():,}")
        print(f"  Total comments: {df['num_comments'].sum():,}")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
