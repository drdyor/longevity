"""PubMed search utilities using NCBI E-utilities."""
import time
import requests
from typing import List, Dict


def search_pubmed(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search PubMed for articles matching the query.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of paper dictionaries with pmid, title, journal, pubdate
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # Search for article IDs
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    
    try:
        search_response = requests.get(
            base_url + "esearch.fcgi",
            params=search_params,
            timeout=10
        )
        search_response.raise_for_status()
        search_data = search_response.json()
        
        ids = search_data.get("esearchresult", {}).get("idlist", [])
        
        if not ids:
            return []
        
        # Fetch article summaries
        summary_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json"
        }
        
        time.sleep(0.35)  # Rate limiting: ~3 requests per second
        
        summary_response = requests.get(
            base_url + "esummary.fcgi",
            params=summary_params,
            timeout=10
        )
        summary_response.raise_for_status()
        summary_data = summary_response.json()
        
        results = []
        for pmid in ids:
            item = summary_data.get("result", {}).get(pmid, {})
            results.append({
                "pmid": pmid,
                "title": item.get("title", ""),
                "journal": item.get("fulljournalname", ""),
                "pubdate": item.get("pubdate", ""),
            })
        
        return results
        
    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return []


def format_references(papers: List[Dict]) -> str:
    """
    Format a list of papers into a readable text summary.
    
    Args:
        papers: List of paper dictionaries
    
    Returns:
        Formatted string of references
    """
    if not papers:
        return "No results found."
    
    lines = []
    for p in papers:
        lines.append(f"- {p['title']} ({p['journal']}, {p['pubdate']}) [PMID: {p['pmid']}]")
    
    return "\n".join(lines)


def build_search_query(claim: str, topic: str) -> str:
    """
    Build an optimized PubMed search query from a claim and topic.
    
    Args:
        claim: The claim text
        topic: The main topic
    
    Returns:
        Formatted search query string
    """
    # Combine topic with longevity-related terms
    base_terms = f"{topic} longevity lifespan healthspan aging"
    
    # Add study quality filters
    filters = "randomized trial OR clinical trial OR meta-analysis OR systematic review"
    
    return f"({base_terms}) AND ({filters})"
