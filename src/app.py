"""
Interactive Streamlit Dashboard for r/longevity Evidence Analysis

This app provides an interactive interface to explore claims extracted from
r/longevity and their evidence ratings.
"""
import os
import sys
import glob
import pandas as pd
import streamlit as st

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@st.cache_data
def load_latest_evidence():
    """Load the most recent evidence file."""
    processed_dir = "data/processed"
    
    # Try parquet first
    parquet_files = glob.glob(os.path.join(processed_dir, "claims_evidence_*.parquet"))
    if parquet_files:
        latest_file = max(parquet_files)
        return pd.read_parquet(latest_file)
    
    # Fall back to CSV
    csv_files = glob.glob(os.path.join(processed_dir, "claims_evidence_*.csv"))
    if csv_files:
        latest_file = max(csv_files)
        return pd.read_csv(latest_file)
    
    return None


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="r/longevity Evidence Tracker",
        page_icon="🧬",
        layout="wide"
    )
    
    st.title("🧬 r/longevity Evidence Tracker")
    st.markdown("*Analyzing longevity claims from Reddit against scientific evidence*")
    
    # Load data
    df = load_latest_evidence()
    
    if df is None:
        st.error("No evidence data found. Please run the pipeline first:")
        st.code("""
python src/01_collect.py
python src/02_extract_claims.py
python src/03_evidence_check.py
        """)
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Topic filter
    topics = ["All"] + sorted(df["topic"].unique().tolist())
    selected_topic = st.sidebar.selectbox("Topic", topics)
    
    # Evidence level filter
    evidence_levels = ["All"] + sorted(df["evidence_level"].unique().tolist())
    selected_evidence = st.sidebar.selectbox("Evidence Level", evidence_levels)
    
    # Direction filter
    if "direction" in df.columns:
        directions = ["All"] + sorted(df["direction"].unique().tolist())
        selected_direction = st.sidebar.selectbox("Direction", directions)
    else:
        selected_direction = "All"
    
    # Type filter
    if "type" in df.columns:
        types = ["All"] + sorted(df["type"].unique().tolist())
        selected_type = st.sidebar.selectbox("Type", types)
    else:
        selected_type = "All"
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_topic != "All":
        filtered_df = filtered_df[filtered_df["topic"] == selected_topic]
    
    if selected_evidence != "All":
        filtered_df = filtered_df[filtered_df["evidence_level"] == selected_evidence]
    
    if selected_direction != "All" and "direction" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["direction"] == selected_direction]
    
    if selected_type != "All" and "type" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["type"] == selected_type]
    
    # Sort by score
    if "post_score" in filtered_df.columns:
        filtered_df = filtered_df.sort_values("post_score", ascending=False)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Claims", len(filtered_df))
    
    with col2:
        if "topic" in filtered_df.columns:
            st.metric("Unique Topics", filtered_df["topic"].nunique())
    
    with col3:
        strong_evidence = len(filtered_df[filtered_df["evidence_level"] == "strong_support"])
        st.metric("Strong Evidence", strong_evidence)
    
    with col4:
        if "post_score" in filtered_df.columns:
            st.metric("Total Reddit Score", f"{filtered_df['post_score'].sum():,}")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Claims List", "📊 Analytics", "📥 Export"])
    
    with tab1:
        st.subheader("Claims")
        
        # Search box
        search = st.text_input("🔍 Search claims", "")
        if search:
            filtered_df = filtered_df[
                filtered_df["claim"].str.contains(search, case=False, na=False) |
                filtered_df["explanation"].str.contains(search, case=False, na=False)
            ]
        
        # Display claims
        for idx, row in filtered_df.head(50).iterrows():
            with st.expander(f"**{row['claim'][:100]}...**" if len(row['claim']) > 100 else f"**{row['claim']}**"):
                col_a, col_b = st.columns([2, 1])
                
                with col_a:
                    st.markdown(f"**Topic:** {row.get('topic', 'N/A')}")
                    st.markdown(f"**Type:** {row.get('type', 'N/A')}")
                    st.markdown(f"**Direction:** {row.get('direction', 'N/A')}")
                    
                    # Evidence
                    evidence_emoji = {
                        "strong_support": "✅",
                        "moderate_support": "🟡",
                        "weak_support": "🟠",
                        "mixed": "⚪",
                        "no_clear_support": "❌",
                        "unknown": "❓",
                        "error": "⚠️"
                    }
                    emoji = evidence_emoji.get(row.get("evidence_level", "unknown"), "❓")
                    st.markdown(f"**Evidence:** {emoji} {row.get('evidence_level', 'N/A')}")
                    
                    st.markdown("**Explanation:**")
                    st.info(row.get("explanation", "No explanation available"))
                
                with col_b:
                    st.markdown(f"**Reddit Score:** ⬆️ {row.get('post_score', 0)}")
                    st.markdown(f"**Comments:** 💬 {row.get('post_comments', 0)}")
                    st.markdown(f"**Papers Found:** 📄 {row.get('num_papers_found', 0)}")
                    
                    if row.get("pmid_list"):
                        pmids = row["pmid_list"].split(",")
                        st.markdown("**PubMed IDs:**")
                        for pmid in pmids[:3]:
                            st.markdown(f"[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")
        
        if len(filtered_df) > 50:
            st.info(f"Showing 50 of {len(filtered_df)} claims. Adjust filters to narrow results.")
    
    with tab2:
        st.subheader("Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Evidence Distribution")
            evidence_counts = filtered_df["evidence_level"].value_counts()
            st.bar_chart(evidence_counts)
        
        with col2:
            st.markdown("### Top Topics")
            if "topic" in filtered_df.columns:
                topic_counts = filtered_df["topic"].value_counts().head(10)
                st.bar_chart(topic_counts)
        
        # Hype vs Evidence Analysis
        st.markdown("### 🔥 Hype vs Evidence Gap")
        st.markdown("*Claims with high Reddit scores but weak evidence*")
        
        if "post_score" in filtered_df.columns:
            weak_evidence = filtered_df[
                filtered_df["evidence_level"].isin(["weak_support", "no_clear_support"])
            ].sort_values("post_score", ascending=False).head(10)
            
            if not weak_evidence.empty:
                for _, row in weak_evidence.iterrows():
                    st.warning(
                        f"**{row['claim'][:80]}...** (Score: {row['post_score']}) "
                        f"- Evidence: {row['evidence_level']}"
                    )
            else:
                st.info("No high-hype, low-evidence claims found.")
    
    with tab3:
        st.subheader("Export Data")
        
        # CSV download
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="longevity_claims_filtered.csv",
            mime="text/csv"
        )
        
        # Markdown report
        st.markdown("### Generate Markdown Report")
        if st.button("Generate Report"):
            markdown = f"""# r/longevity Evidence Report

Generated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}

## Summary
- Total claims analyzed: {len(filtered_df)}
- Unique topics: {filtered_df['topic'].nunique() if 'topic' in filtered_df.columns else 'N/A'}
- Strong evidence claims: {len(filtered_df[filtered_df['evidence_level'] == 'strong_support'])}

## Evidence Distribution
{filtered_df['evidence_level'].value_counts().to_markdown()}

## Top 10 Claims by Reddit Score
"""
            for idx, row in filtered_df.head(10).iterrows():
                markdown += f"\n### {row['claim']}\n"
                markdown += f"- **Topic:** {row.get('topic', 'N/A')}\n"
                markdown += f"- **Evidence:** {row.get('evidence_level', 'N/A')}\n"
                markdown += f"- **Reddit Score:** {row.get('post_score', 0)}\n"
                markdown += f"- **Explanation:** {row.get('explanation', 'N/A')}\n"
            
            st.download_button(
                label="📥 Download Report",
                data=markdown,
                file_name="longevity_report.md",
                mime="text/markdown"
            )


if __name__ == "__main__":
    main()
