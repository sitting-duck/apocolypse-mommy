# scripts/build_bm25.py
# python scripts/build_bm25.py --corpus /abs/path/to/trainer/data/corpus_clean.jsonl --out data/bm25.idx
# eg: 
# $ python ./build_bm25.py --corpus /Users/ashleytharp/Documents/Github/apocolypse-mommy/reranker/data/corpus_clean.jsonl --out ./../data/bm25.idx
# Built BM25 index with 67823 docs → ./../data/bm25.idx
import argparse, os
from retriever_bm25 import build_index

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, help="Path to corpus JSONL")
    ap.add_argument("--out", required=True, help="Path to write BM25 index (e.g., data/bm25.idx)")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    n = build_index(args.corpus, args.out)
    print(f"Built BM25 index with {n} docs → {args.out}")

