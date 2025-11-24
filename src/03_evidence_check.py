"""
Step 3: Check claims against PubMed evidence
"""
import os
import sys
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.pubmed import search_pubmed, format_references, build_search_query
from src.utils.llm import evaluate_claim

def find_latest_claims_file(data_dir: str = "data/interim") -> str:
    """Find the most recent claims parquet file."""
    import glob
    files = glob.glob(os.path.join(data_dir, "claims_*.parquet"))
    if not files:
        raise FileNotFoundError(f"No claims files found in {data_dir}")
    return max(files)

def main():
    """Main evidence checking function."""
    print("=" * 60)
    print("Evidence Check - PubMed Verification")
    print("=" * 60)
    
    OUTPUT_DIR = "data/processed"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    try:
        input_file = find_latest_claims_file("data/interim")
        print(f"\nLoading claims from: {input_file}")
        claims_df = pd.read_parquet(input_file)
        print(f"✓ Loaded {len(claims_df)} claims")
        
        print("\nChecking evidence (PubMed + LLM evaluation)...")
        print("Respecting PubMed rate limits (~3 req/sec)\n")
        
        results = []
        
        for idx, row in claims_df.iterrows():
            pct = ((idx + 1) / len(claims_df)) * 100
            print(f"  [{idx+1}/{len(claims_df)}] ({pct:.1f}%) {row.get('claim', '')[:50]}...")
            
            try:
                query = build_search_query(
                    claim=row.get("claim", ""),
                    topic=row.get("topic", "")
                )
                
                papers = search_pubmed(query, max_results=5)
                references_text = format_references(papers)
                
                evaluation = evaluate_claim(
                    claim=row.get("claim", ""),
                    topic=row.get("topic", ""),
                    references_text=references_text
                )
                
                result = {
                    **row.to_dict(),
                    "evidence_level": evaluation.get("evidence_level", "unknown"),
                    "explanation": evaluation.get("explanation", ""),
                    "num_papers_found": len(papers),
                    "pmid_list": ",".join([p["pmid"] for p in papers]),
                }
                
                results.append(result)
                print(f"       Evidence: {evaluation.get('evidence_level', 'unknown')}")
                
            except Exception as e:
                print(f"       Warning: Error - {e}")
                results.append({
                    **row.to_dict(),
                    "evidence_level": "error",
                    "explanation": str(e),
                    "num_papers_found": 0,
                    "pmid_list": "",
                })
                continue
        
        print(f"\n✓ Checked {len(results)} claims")
        
        results_df = pd.DataFrame(results)
        output_file = os.path.join(OUTPUT_DIR, f"claims_evidence_{timestamp}.parquet")
        results_df.to_parquet(output_file, index=False)
        
        csv_file = os.path.join(OUTPUT_DIR, f"claims_evidence_{timestamp}.csv")
        results_df.to_csv(csv_file, index=False)
        
        print(f"✓ Saved to: {output_file}")
        print(f"✓ CSV saved to: {csv_file}")
        
        print("\nEvidence Summary:")
        print(f"  Total claims analyzed: {len(results_df)}")
        if "evidence_level" in results_df.columns:
            print("\n  Evidence levels:")
            print(results_df["evidence_level"].value_counts().to_string())
        
        print("\n✅ Pipeline complete! Ready for dashboard.")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
