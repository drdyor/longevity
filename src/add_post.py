"""
Add and analyze new Reddit posts/URLs

This script allows you to manually add Reddit content for analysis.
Simply paste Reddit post text or URLs, and the system will:
1. Extract claims
2. Verify against PubMed
3. Generate comparison report
"""
import os
import sys
import pandas as pd
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.llm import extract_claims_from_post
from src.utils.pubmed import search_pubmed, format_references, build_search_query
from src.utils.llm import evaluate_claim


def analyze_reddit_post(title: str, text: str, post_url: str = "", post_id: str = None):
    """
    Analyze a single Reddit post and return structured results.
    
    Returns dict with:
    - Original post
    - Extracted claims
    - PubMed evidence for each claim
    - Comparison analysis
    """
    if not post_id:
        post_id = f"manual_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print("=" * 70)
    print("ANALYZING REDDIT POST")
    print("=" * 70)
    print(f"\nTitle: {title}")
    print(f"URL: {post_url or 'N/A'}")
    print("-" * 70)
    
    # Step 1: Extract claims
    print("\n[1/3] Extracting claims with AI (Ollama)...")
    claims = extract_claims_from_post(title, text)
    
    if not claims:
        print("   ⚠️  No specific longevity claims found in this post")
        return None
    
    print(f"   ✓ Found {len(claims)} claims")
    
    # Step 2: Verify each claim against PubMed
    print(f"\n[2/3] Verifying {len(claims)} claims against PubMed...")
    
    results = []
    for i, claim_data in enumerate(claims, 1):
        claim_text = claim_data.get('claim', '')
        topic = claim_data.get('topic', '')
        
        print(f"\n   Claim {i}/{len(claims)}: {claim_text[:60]}...")
        
        # Search PubMed
        query = build_search_query(claim_text, topic)
        papers = search_pubmed(query, max_results=5)
        refs_text = format_references(papers)
        
        print(f"      Found {len(papers)} PubMed papers")
        
        # Evaluate with LLM
        evaluation = evaluate_claim(claim_text, topic, refs_text)
        
        results.append({
            'claim': claim_text,
            'topic': topic,
            'type': claim_data.get('type', ''),
            'direction': claim_data.get('direction', ''),
            'target': claim_data.get('target', ''),
            'evidence_level': evaluation.get('evidence_level', 'unknown'),
            'explanation': evaluation.get('explanation', ''),
            'num_papers': len(papers),
            'papers': papers,
            'post_id': post_id,
            'post_url': post_url
        })
        
        print(f"      Evidence: {evaluation.get('evidence_level', 'unknown')}")
    
    # Step 3: Generate comparison report
    print("\n[3/3] Generating comparison report...")
    
    report_data = {
        'post_title': title,
        'post_url': post_url,
        'post_id': post_id,
        'analysis_date': datetime.now().isoformat(),
        'claims_found': len(claims),
        'results': results
    }
    
    return report_data


def generate_comparison_report(analysis_data):
    """Generate a detailed Markdown comparison report."""
    
    report = f"""# Reddit vs Science Comparison Report

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Original Reddit Post

**Title:** {analysis_data['post_title']}

**URL:** {analysis_data.get('post_url', 'N/A')}

**Claims Identified:** {analysis_data['claims_found']}

---

## Methodology

This analysis follows a rigorous 3-step verification process:

### Step 1: Claim Extraction
- **Method:** AI-powered extraction using Llama 3 (8B parameters)
- **Process:** Identifies specific, falsifiable claims about longevity interventions
- **Output:** Structured claims with topic categorization

### Step 2: Literature Search
- **Database:** PubMed (NCBI E-utilities API)
- **Query:** Targeted search for clinical trials, RCTs, meta-analyses
- **Limit:** Top 5 most relevant papers per claim
- **Rate:** 3 requests/second (respecting NCBI guidelines)

### Step 3: Evidence Evaluation
- **Method:** AI-powered synthesis (Llama 3)
- **Criteria:**
  - ✅ **Strong support**: Multiple RCTs, meta-analyses, human data
  - 🟡 **Moderate support**: Some studies, limited human data
  - 🟠 **Weak support**: Animal models only, small studies
  - ⚪ **Mixed**: Conflicting evidence
  - ❌ **No clear support**: No relevant evidence found

---

## Detailed Analysis

"""
    
    # Add each claim analysis
    for i, result in enumerate(analysis_data['results'], 1):
        evidence_emoji = {
            'strong_support': '✅',
            'moderate_support': '🟡',
            'weak_support': '🟠',
            'mixed': '⚪',
            'no_clear_support': '❌',
            'unknown': '❓'
        }
        emoji = evidence_emoji.get(result['evidence_level'], '❓')
        
        report += f"""### Claim {i}: {result['claim']}

**Topic:** {result['topic']}  
**Type:** {result['type']}  
**Direction:** {result['direction']}  
**Target:** {result['target']}

#### Evidence Rating: {emoji} {result['evidence_level'].upper().replace('_', ' ')}

**Scientific Explanation:**
{result['explanation']}

**Supporting Literature ({result['num_papers']} papers found):**
"""
        
        if result['papers']:
            for paper in result['papers']:
                report += f"\n- **[{paper['title']}](https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/)**  \n"
                report += f"  {paper['journal']}, {paper['pubdate']} (PMID: {paper['pmid']})\n"
        else:
            report += "\nNo relevant papers found in PubMed.\n"
        
        report += "\n---\n\n"
    
    # Summary
    report += """## Summary & Reliability Assessment

### Evidence Quality Distribution:
"""
    
    evidence_counts = {}
    for result in analysis_data['results']:
        level = result['evidence_level']
        evidence_counts[level] = evidence_counts.get(level, 0) + 1
    
    for level, count in evidence_counts.items():
        emoji = {'strong_support': '✅', 'moderate_support': '🟡', 'weak_support': '🟠', 
                 'mixed': '⚪', 'no_clear_support': '❌', 'unknown': '❓'}.get(level, '❓')
        report += f"- {emoji} **{level.replace('_', ' ').title()}:** {count} claim(s)\n"
    
    report += f"""

### Key Findings:

**Total Claims Analyzed:** {len(analysis_data['results'])}  
**Claims with Scientific Support:** {sum(1 for r in analysis_data['results'] if r['evidence_level'] in ['strong_support', 'moderate_support'])}  
**Claims Lacking Evidence:** {sum(1 for r in analysis_data['results'] if r['evidence_level'] == 'no_clear_support')}

---

## Transparency & Reproducibility

**Data Sources:**
- Reddit post (original source)
- PubMed Central (peer-reviewed literature)
- All PMIDs cited above are verifiable

**AI Models Used:**
- Claim extraction: Llama 3 (8B, open-source)
- Evidence synthesis: Llama 3 (8B, open-source)
- All prompts designed to minimize hallucination

**Limitations:**
- AI may miss nuanced claims
- PubMed search limited to top 5 results per claim
- Evidence evaluation is AI-assisted, not peer-reviewed
- No manual expert review performed

**Confidence Level:**
This report provides a systematic, transparent analysis but should be considered preliminary. 
For critical health decisions, consult the original papers and medical professionals.

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**System Version:** Reddit Longevity Evidence Agent v1.0  
**Contact:** [Your details here]

"""
    
    return report


def main():
    """Interactive mode to add new posts."""
    print("=" * 70)
    print("REDDIT POST ANALYZER - Add New Content")
    print("=" * 70)
    print("\nThis tool analyzes Reddit posts and compares claims to PubMed evidence.")
    print("\nOptions:")
    print("1. Paste Reddit post text")
    print("2. Enter Reddit URL (future feature)")
    print("3. Load from file")
    
    # For now, demo with command line args
    if len(sys.argv) < 3:
        print("\nUsage:")
        print('  python src/add_post.py "Post Title" "Post Text" [optional_url]')
        print("\nExample:")
        print('  python src/add_post.py "Rapamycin results" "I\'ve been taking 6mg weekly..."')
        return 1
    
    title = sys.argv[1]
    text = sys.argv[2]
    url = sys.argv[3] if len(sys.argv) > 3 else ""
    
    # Analyze
    analysis = analyze_reddit_post(title, text, url)
    
    if not analysis:
        return 1
    
    # Generate report
    report = generate_comparison_report(analysis)
    
    # Save report
    output_dir = "data/reports"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"analysis_{timestamp}.md")
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete!")
    print(f"✓ Report saved to: {report_file}")
    
    # Also append to main evidence database
    df_new = pd.DataFrame(analysis['results'])
    
    # Check if main database exists
    main_db = "data/processed/claims_evidence_main.csv"
    if os.path.exists(main_db):
        df_existing = pd.read_csv(main_db)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    df_combined.to_csv(main_db, index=False)
    print(f"✓ Added to main database: {main_db}")
    
    print(f"\n📄 View your report:")
    print(f"   cat {report_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
