# retriever_bm25.py
import json, pickle
from pathlib import Path
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi

# Expected corpus: JSONL with {"id": "...", "text": "...", "title": "..."} (title optional)

def _tokenize(s: str) -> List[str]:
    return s.lower().split()  # simple + fast; swap in better tokenization if you like

def build_index(corpus_path: str, index_path: str):
    docs = []
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            text = obj.get("text") or obj.get("body") or ""
            if not text.strip():
                continue
            docs.append({"id": obj.get("id"), "title": obj.get("title", ""), "text": text})
    tokenized = [ _tokenize(d["text"]) for d in docs ]
    bm25 = BM25Okapi(tokenized)
    Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, "wb") as f:
        pickle.dump({"docs": docs, "bm25": bm25}, f)
    return len(docs)

def load_index(index_path: str):
    with open(index_path, "rb") as f:
        blob = pickle.load(f)
    return blob["bm25"], blob["docs"]

def retrieve(query: str, bm25, docs: List[Dict], top_k: int = 50) -> List[Dict]:
    scores = bm25.get_scores(_tokenize(query))
    idx_scores: List[Tuple[int, float]] = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
    return [ {**docs[i], "score": float(s)} for i, s in idx_scores ]

