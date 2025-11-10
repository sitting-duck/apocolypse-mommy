# reranker_ce.py
"""
Cross-Encoder reranker wrapper.

Usage (programmatic):
    from reranker_ce import RerankerCE
    rr = RerankerCE("/abs/path/to/your/checkpoint", batch_size=64, device=None)
    reranked = rr.score("boil water safely", candidates)  # candidates: List[{"text": "...", "title": "...", "id": "..."}]
    # Each dict gets 'rerank_score' added and the list is sorted desc by that score.

Notes:
- Works with Sentence-Transformers CrossEncoder checkpoints (e.g., your fine-tuned model).
- Device: None = auto (CPU on macOS typically), or 'cuda' if you installed a CUDA torch build.
- We defensively trim very long strings by characters (tokenizer will still truncate by tokens).
"""

from __future__ import annotations
from typing import List, Dict, Optional
from sentence_transformers import CrossEncoder

_DEFAULT_MAX_CHARS_PER_SIDE = 4000  # guard against extremely long passages (tokenizer will still truncate)

class RerankerCE:
    def __init__(
        self,
        model_path: str,
        batch_size: int = 64,
        device: Optional[str] = None,
        max_chars_per_side: int = _DEFAULT_MAX_CHARS_PER_SIDE,
        normalize: bool = False,
    ):
        """
        :param model_path: Path to the CrossEncoder checkpoint directory (contains config.json, model.safetensors, etc.)
        :param batch_size: Batch size for inference.
        :param device: 'cuda', 'cpu', or None for auto.
        :param max_chars_per_side: Hard cap on characters for query/doc string before tokenization.
        :param normalize: If True, min-max normalize scores to [0,1] (useful for logging/UX; ranking is unchanged).
        """
        self.model = CrossEncoder(model_path, device=device)
        self.batch_size = int(batch_size)
        self.max_chars = int(max_chars_per_side) if max_chars_per_side and max_chars_per_side > 0 else None
        self.normalize = bool(normalize)

    def _trim(self, s: str) -> str:
        if not isinstance(s, str):
            s = "" if s is None else str(s)
        if self.max_chars and len(s) > self.max_chars:
            return s[: self.max_chars]
        return s

    def score(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """
        Adds 'rerank_score' to each candidate and returns a new list sorted by that score (desc).
        Each candidate must have a 'text' field; 'title' and 'id' are optional.

        :param query: User query/question string.
        :param candidates: List of dicts with at least {'text': str, ...}
        :return: Sorted list (desc) with 'rerank_score' added.
        """
        if not candidates:
            return []

        q = self._trim(query or "")
        pairs = [(q, self._trim(c.get("text", ""))) for c in candidates]

        # Sentence-Transformers CrossEncoder.predict returns a numpy array of floats
        scores = self.model.predict(pairs, batch_size=self.batch_size, show_progress_bar=False)

        if self.normalize and len(scores) > 0:
            smin, smax = float(scores.min()), float(scores.max())
            if smax > smin:
                scores = (scores - smin) / (smax - smin)
            else:
                # all same: map to 0.5
                scores = scores * 0 + 0.5

        out: List[Dict] = []
        for c, s in zip(candidates, scores):
            c2 = dict(c)
            c2["rerank_score"] = float(s)
            out.append(c2)

        out.sort(key=lambda d: d["rerank_score"], reverse=True)
        return out

    def topk(self, query: str, candidates: List[Dict], k: int = 5) -> List[Dict]:
        """Convenience: return only the top-k after scoring."""
        return self.score(query, candidates)[: int(k)]

