"""
Step 2: Extract claims from Reddit posts
"""
import os
import sys
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.llm import extract_claims_from_post

def find_latest_posts_file(data_dir: str = "data/raw") -> str:
    """Find the most recent posts CSV file."""
    import glob
    files = glob.glob(os.path.join(data_dir, "posts_*.csv"))
    if not files:
        raise FileNotFoundError(f"No posts files found in {data_dir}")
    return max(files)

def main():
    """Main claim extraction function."""
    print("=" * 60)
    print("Claim Extraction from Reddit Posts")
    print("=" * 60)
    
    OUTPUT_DIR = "data/interim"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    try:
        input_file = find_latest_posts_file("data/raw")
        print(f"\nLoading posts from: {input_file}")
        df = pd.read_csv(input_file)
        print(f"✓ Loaded {len(df)} posts")
        
        print("\nExtracting claims with Ollama (llama3:8b)...")
        print("This will take a few minutes...\n")
        
        all_claims = []
        for idx, row in df.iterrows():
            print(f"  [{idx+1}/{len(df)}] Processing: {row['title'][:60]}...")
            
            try:
                claims = extract_claims_from_post(
                    title=row.get("title", ""),
                    selftext=row.get("selftext", "")
                )
                
                for claim in claims:
                    claim.update({
                        "post_id": row["id"],
                        "created_utc": row["created_utc"],
                        "post_score": row["score"],
                        "post_comments": row["num_comments"],
                    })
                
                all_claims.extend(claims)
                print(f"      Found {len(claims)} claims")
                
            except Exception as e:
                print(f"      Warning: Error - {e}")
                continue
        
        print(f"\n✓ Extracted {len(all_claims)} total claims from {len(df)} posts")
        
        if not all_claims:
            print("⚠ No claims extracted.")
            return 1
        
        claims_df = pd.DataFrame(all_claims)
        output_file = os.path.join(OUTPUT_DIR, f"claims_{timestamp}.parquet")
        claims_df.to_parquet(output_file, index=False)
        
        print(f"✓ Saved to: {output_file}")
        
        print("\nClaim Statistics:")
        print(f"  Total claims: {len(claims_df)}")
        if "topic" in claims_df.columns:
            print(f"  Unique topics: {claims_df['topic'].nunique()}")
            print("\n  Top topics:")
            print(claims_df['topic'].value_counts().head(10).to_string())
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
