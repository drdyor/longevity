"""LLM utilities for local inference via Ollama."""
import json
from typing import Dict, List, Any
import ollama


def chat_completion(prompt: str, model: str = "llama3:8b") -> str:
    """Send a prompt to the local Ollama model and return the response."""
    try:
        resp = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp["message"]["content"]
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""


def extract_json_from_response(response: str) -> Any:
    """Try to extract and parse JSON from an LLM response."""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        start = response.find("[")
        end = response.rfind("]")
        if start != -1 and end != -1:
            try:
                return json.loads(response[start:end+1])
            except json.JSONDecodeError:
                pass
        start = response.find("{")
        end = response.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(response[start:end+1])
            except json.JSONDecodeError:
                pass
        return {}


def extract_claims_from_post(title: str, selftext: str, model: str = "llama3:8b") -> List[Dict]:
    """Extract longevity-related claims from a Reddit post."""
    text = f"{title}\n\n{selftext}".strip()
    if not text:
        return []
    
    prompt = f"""You are an evidence-focused medical research assistant.

From the text below, extract SPECIFIC longevity-related claims.

Return JSON ONLY in this format (no other text):
[
  {{
    "claim": "specific claim statement",
    "topic": "main topic (e.g., rapamycin, NAD+, metformin, GLP-1, fasting, exercise, etc.)",
    "type": "supplement/drug/lifestyle/device/other",
    "direction": "benefit/harm/neutral",
    "target": "lifespan/healthspan/disease/performance/other"
  }}
]

If no clear longevity claims are present, return: []

TEXT:
{text[:2000]}
"""
    
    response = chat_completion(prompt, model)
    claims = extract_json_from_response(response)
    if not isinstance(claims, list):
        return []
    return claims


def evaluate_claim(claim: str, topic: str, references_text: str, model: str = "llama3:8b") -> Dict:
    """Evaluate a claim against scientific references."""
    prompt = f"""You are a critical longevity researcher.

CLAIM:
"{claim}"

RELATED SCIENTIFIC PAPERS:
{references_text or "No results found."}

Based ONLY on this information, evaluate the claim:

1. Rate the strength of evidence:
   - "strong_support" (multiple RCTs, meta-analyses)
   - "moderate_support" (some studies, limited human data)
   - "weak_support" (animal models only, small studies)
   - "mixed" (conflicting evidence)
   - "no_clear_support" (no relevant evidence found)

2. Explain in 3-5 sentences.

Return JSON ONLY (no other text):
{{
  "evidence_level": "...",
  "explanation": "..."
}}
"""
    
    response = chat_completion(prompt, model)
    result = extract_json_from_response(response)
    if not isinstance(result, dict):
        return {"evidence_level": "unknown", "explanation": "Could not parse evaluation"}
    return result
