# src/vector_store.py

import requests
import json
from typing import List, Dict
from config import ENDEE_BASE_URL, INDEX_NAME

# Endee endpoints
CREATE_INDEX_URL = f"{ENDEE_BASE_URL}/api/v1/index/create"
INSERT_VECTOR_URL = f"{ENDEE_BASE_URL}/api/v1/index/{INDEX_NAME}/vector/insert"

# Local metadata file (since Endee does not store metadata)
METADATA_FILE = "vector_metadata.json"


def create_index(dim: int = 384, space_type: str = "cosine"):
    """
    Create a vector index in Endee.
    """
    payload = {
        "index_name": INDEX_NAME,
        "dim": dim,
        "space_type": space_type
    }

    response = requests.post(CREATE_INDEX_URL, json=payload)

    # Index may already exist
    if response.status_code not in (200, 201):
        if "already exists" in response.text.lower():
            print(f"Index '{INDEX_NAME}' already exists.")
            return
        raise RuntimeError(
            f"Failed to create index: {response.status_code} {response.text}"
        )

    print(f"Index '{INDEX_NAME}' created successfully.")


def store_vectors(embeddings: List[List[float]], documents: List[Dict]):
    """
    Store vectors in Endee and save metadata locally.
    """
    if len(embeddings) != len(documents):
        raise ValueError("Embeddings and documents count mismatch")

    metadata_map = {}

    for i, (vector, doc) in enumerate(zip(embeddings, documents), start=1):
        vector_id = f"doc_{i:04d}"

        payload = [
            {
                "id": vector_id,
                "vector": vector
            }
        ]

        response = requests.post(INSERT_VECTOR_URL, json=payload)

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Failed to insert vector {vector_id}: "
                f"{response.status_code} {response.text}"
            )

        # Store metadata locally
        metadata_map[vector_id] = {
            "content": doc["content"],
            "source": doc["source"]
        }

    # Save metadata locally
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata_map, f, indent=2)

    print(f"✓ Stored {len(metadata_map)} vectors")
    print(f"✓ Metadata saved to {METADATA_FILE}")
