"""
Step 3: Check claims against PubMed evidence

This script searches PubMed for each claim and uses an LLM to evaluate
the strength of evidence.
"""
import os
import sys
from datetime import datetime
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.pubmed import search_pubmed, format_references, build_search_query
from src.utils.llm import evaluate_claim


def find_latest_claims_file(data_dir: str = "data/interim") -> str:
    """Find the most recent claims parquet file."""
    import glob
    files = glob.glob(os.path.join(data_dir, "claims_*.parquet"))
    if not files:
        raise FileNotFoundError(f"No claims files found in {data_dir}")
    return max(files)  # Most recent by filename


def main():
    """Main evidence checking function."""
    print("=" * 60)
    print("Evidence Check - PubMed Verification")
    print("=" * 60)
    
    # Configuration
    INPUT_DIR = os.getenv("DATA_DIR", "data/interim")
    OUTPUT_DIR = os.getenv("DATA_DIR", "data/processed")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Load claims
        input_file = find_latest_claims_file(INPUT_DIR)
        print(f"\nLoading claims from: {input_file}")
        claims_df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_parquet(input_file)
        print(f"✓ Loaded {len(claims_df)} claims")
        
        # Check evidence for each claim
        print("\nChecking evidence (this will take a while)...")
        print("Note: Respecting PubMed rate limits (~3 req/sec)")
        
        results = []
        
        for idx, row in claims_df.iterrows():
            if idx % 10 == 0:
                pct = (idx / len(claims_df)) * 100
                print(f"  Progress: {idx}/{len(claims_df)} ({pct:.1f}%)")
            
            try:
                # Build search query
                query = build_search_query(
                    claim=row.get("claim", ""),
                    topic=row.get("topic", "")
                )
                
                # Search PubMed
                papers = search_pubmed(query, max_results=5)
                references_text = format_references(papers)
                
                # Evaluate with LLM
                evaluation = evaluate_claim(
                    claim=row.get("claim", ""),
                    topic=row.get("topic", ""),
                    references_text=references_text
                )
                
                # Combine all data
                result = {
                    **row.to_dict(),
                    "evidence_level": evaluation.get("evidence_level", "unknown"),
                    "explanation": evaluation.get("explanation", ""),
                    "num_papers_found": len(papers),
                    "pmid_list": ",".join([p["pmid"] for p in papers]),
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"  Warning: Error processing claim {idx}: {e}")
                # Add row with error marker
                results.append({
                    **row.to_dict(),
                    "evidence_level": "error",
                    "explanation": str(e),
                    "num_papers_found": 0,
                    "pmid_list": "",
                })
                continue
        
        print(f"\n✓ Checked {len(results)} claims")
        
        # Save results
        results_df = pd.DataFrame(results)
        output_file = os.path.join(OUTPUT_DIR, f"claims_evidence_{timestamp}.parquet")
        results_df.to_parquet(output_file, index=False)
        
        # Also save as CSV for easy viewing
        csv_file = os.path.join(OUTPUT_DIR, f"claims_evidence_{timestamp}.csv")
        results_df.to_csv(csv_file, index=False)
        
        print(f"✓ Saved to: {output_file}")
        print(f"✓ CSV saved to: {csv_file}")
        
        # Summary statistics
        print("\nEvidence Summary:")
        print(f"  Total claims analyzed: {len(results_df)}")
        if "evidence_level" in results_df.columns:
            print("\n  Evidence levels:")
            print(results_df["evidence_level"].value_counts().to_string())
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
