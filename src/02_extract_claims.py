"""
Step 2: Extract claims from Reddit posts

This script processes posts and extracts specific longevity-related claims
using a local LLM via Ollama.
"""
import os
import sys
from datetime import datetime
import pandas as pd
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.llm import extract_claims_from_post


def find_latest_posts_file(data_dir: str = "data/raw") -> str:
    """Find the most recent posts CSV file."""
    import glob
    files = glob.glob(os.path.join(data_dir, "posts_*.csv"))
    if not files:
        raise FileNotFoundError(f"No posts files found in {data_dir}")
    return max(files)  # Most recent by filename


def main():
    """Main claim extraction function."""
    print("=" * 60)
    print("Claim Extraction from Reddit Posts")
    print("=" * 60)
    
    # Configuration
    INPUT_DIR = os.getenv("DATA_DIR", "data/raw")
    OUTPUT_DIR = os.getenv("DATA_DIR", "data/interim")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Load posts
        input_file = find_latest_posts_file(INPUT_DIR)
        print(f"\nLoading posts from: {input_file}")
        df = pd.read_csv(input_file)
        print(f"✓ Loaded {len(df)} posts")
        
        # Extract claims
        print("\nExtracting claims (this may take a while)...")
        print("Note: Make sure Ollama is running with llama3:8b model")
        
        all_claims = []
        for idx, row in df.iterrows():
            if idx % 10 == 0:
                print(f"  Progress: {idx}/{len(df)} posts processed ({len(all_claims)} claims found)")
            
            try:
                claims = extract_claims_from_post(
                    title=row.get("title", ""),
                    selftext=row.get("selftext", "")
                )
                
                # Add post metadata to each claim
                for claim in claims:
                    claim.update({
                        "post_id": row["id"],
                        "created_utc": row["created_utc"],
                        "post_score": row["score"],
                        "post_comments": row["num_comments"],
                    })
                
                all_claims.extend(claims)
                
            except Exception as e:
                print(f"  Warning: Error processing post {row['id']}: {e}")
                continue
        
        print(f"\n✓ Extracted {len(all_claims)} claims from {len(df)} posts")
        
        if not all_claims:
            print("⚠ No claims extracted. Check that Ollama is running.")
            return 1
        
        # Save claims
        claims_df = pd.DataFrame(all_claims)
        output_file = os.path.join(OUTPUT_DIR, f"claims_{timestamp}.parquet")
        claims_df.to_parquet(output_file, index=False)
        
        print(f"✓ Saved to: {output_file}")
        
        # Summary statistics
        print("\nClaim Statistics:")
        print(f"  Total claims: {len(claims_df)}")
        if "topic" in claims_df.columns:
            print(f"  Unique topics: {claims_df['topic'].nunique()}")
            print("\n  Top 10 topics:")
            print(claims_df['topic'].value_counts().head(10).to_string())
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
