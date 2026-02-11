# src/retriever.py

import json
import requests
import msgpack
from typing import List, Dict

from config import ENDEE_BASE_URL, INDEX_NAME, TOP_K

METADATA_FILE = "vector_metadata.json"


def load_metadata() -> Dict:
    """Load local vector metadata."""
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def search_endee(query_vector: List[float], k: int = TOP_K) -> List[Dict]:
    """
    Search Endee index using the correct API and msgpack response.
    """
    url = f"{ENDEE_BASE_URL}/api/v1/index/{INDEX_NAME}/search"

    payload = {
        "vector": query_vector,
        "k": k,
        "include_vectors": False
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    # Decode msgpack response
    decoded = msgpack.unpackb(response.content, raw=False)

    results = []
    for item in decoded:
        # Expected format: [score, vector_id, ...]
        if isinstance(item, list) and len(item) >= 2:
            results.append({
                "id": item[1],
                "score": item[0]
            })

    return results


def retrieve_documents(query_vector: List[float], k: int = TOP_K) -> List[Dict]:
    """
    Retrieve documents by combining Endee search results
    with local metadata.
    """
    metadata = load_metadata()
    search_results = search_endee(query_vector, k)

    documents = []
    for res in search_results:
        vec_id = res["id"]
        if vec_id in metadata:
            documents.append({
                "content": metadata[vec_id]["content"],
                "source": metadata[vec_id]["source"],
                "score": res["score"]
            })

    return documents
