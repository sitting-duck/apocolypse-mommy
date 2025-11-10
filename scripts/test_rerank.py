# scripts/test_rerank.py
from pathlib import Path
import sys

# add repo root to sys.path so we can import retriever_bm25 / reranker_ce
sys.path.append(str(Path(__file__).resolve().parents[1]))

import os
from retriever_bm25 import load_index, retrieve
from reranker_ce import RerankerCE

BM25_INDEX_PATH = os.environ.get("BM25_INDEX_PATH", "data/bm25.idx")
RERANKER_PATH   = os.environ.get("RERANKER_PATH", "/Users/ashleytharp/Documents/Github/apocolypse-mommy/reranker/checkpoints/modelA_miniLM_e2_bm25neg")
BM25_TOPK       = int(os.environ.get("BM25_TOPK", "50"))
RERANK_TOPN     = int(os.environ.get("RERANK_TOPN", "5"))

def main():
    print("Python:", sys.executable)
    print("CWD:", Path.cwd())
    print("BM25_INDEX_PATH:", BM25_INDEX_PATH)
    print("RERANKER_PATH:", RERANKER_PATH)

    bm25, docs = load_index(BM25_INDEX_PATH)
    print("Docs loaded:", len(docs))

    rr = RerankerCE(RERANKER_PATH, device=None)
    q = input("Enter a test query (e.g., 'boil water'): ").strip()
    if not q:
        print("No query, exiting.")
        return

    candidates = retrieve(q, bm25, docs, top_k=BM25_TOPK)
    print("Candidates retrieved:", len(candidates))
    reranked = rr.score(q, candidates)
    topn = reranked[:RERANK_TOPN]

    print("\nTop results:")
    for i, d in enumerate(topn, 1):
        title = d.get("title") or ""
        snippet = (d.get("text") or "")[:400].replace("\n", " ")
        print(f"\n[{i}] score={d.get('rerank_score'):.4f} title={title}\n{snippet}\n---")

if __name__ == "__main__":
    main()

