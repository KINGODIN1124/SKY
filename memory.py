# modules/memory.py
import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Disable tqdm progress bars for clean output
os.environ["TQDM_DISABLE"] = "1"

MEMORY_FILE = "sky_memory.json"
import logging
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
INDEX_FILE = "sky_index.faiss"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def reset_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

def build_embeddings(history):
    """
    Build FAISS index for embeddings.
    """
    texts = [msg['content'] for msg in history if msg['role'] == 'user']
    if not texts:
        return None
    embeddings = EMBEDDING_MODEL.encode(texts, show_progress_bar=False)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, INDEX_FILE)
    return index

def retrieve_relevant_memory(query, history, top_k=5):
    """
    Retrieve top-k relevant memories using embeddings.
    """
    try:
        if not os.path.exists(INDEX_FILE):
            build_embeddings(history)
        if not os.path.exists(INDEX_FILE):
            return []  # No index built yet
        index = faiss.read_index(INDEX_FILE)
        query_emb = EMBEDDING_MODEL.encode([query])
        distances, indices = index.search(np.array(query_emb), top_k)
        relevant = []
        user_msgs = [msg for msg in history if msg['role'] == 'user']
        for idx in indices[0]:
            if idx < len(user_msgs):
                relevant.append(user_msgs[idx])
        return relevant
    except Exception as e:
        # Silently handle errors to avoid console spam
        return []
