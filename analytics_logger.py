# analytics_logger.py
# Simple JSONL analytics for Honey (Telegram bot)
# - Interaction logging (messages, timing, sizes, categories)
# - Affiliate funnel logging (impressions, clicks, purchases)
# - Lightweight keyword-based categorization

from __future__ import annotations
import os, json, datetime, re, threading
from pathlib import Path
from typing import Optional, Dict, Any, Iterable

# -------- Config --------
ANALYTICS_FILE = Path(os.getenv("ANALYTICS_FILE", "analytics/events.jsonl"))
ANALYTICS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Single global lock for append writes (cheap & simple)
_WRITE_LOCK = threading.Lock()

# -------- Categorization (rule of thumb) --------
# You can extend/modify these lists anytime.
_CATS = {
    "water": [
        r"\bwater\b", r"\bfilter(s|ing)?\b", r"\bpurif(y|ier|ication)\b",
        r"\bstorage\b", r"\bboil(ing)?\b"
    ],
    "food": [
        r"\bfood\b", r"\bmre(s)?\b", r"\bnon[- ]?perishable\b", r"\bcanned\b",
        r"\bcalorie(s)?\b", r"\bstockpile\b"
    ],
    "power": [
        r"\b(power|electricity|grid)\b", r"\bblackout\b", r"\bgenerator\b",
        r"\bsolar\b", r"\bbattery\b", r"\bpower bank\b"
    ],
    "shelter": [
        r"\bshelter\b", r"\btent\b", r"\bblanket\b", r"\bspace blanket\b",
        r"\binsulat(e|ion)\b", r"\bwarmth\b"
    ],
    "medical": [
        r"\bfirst[- ]?aid\b", r"\bbandage\b", r"\btrauma\b", r"\bifak\b",
        r"\bmed(ical|s)?\b", r"\bwound\b"
    ],
    "comms": [
        r"\bradio\b", r"\bnoaa\b", r"\bfrs\b", r"\bham\b", r"\bwalkie\b",
        r"\bcommunication(s)?\b"
    ],
    "evac": [
        r"\bevac(uate|uation)\b", r"\bevacuating\b", r"\broute(s)?\b",
        r"\bbug[- ]?out\b", r"\bgo[- ]?bag\b"
    ],
    "weather": [
        r"\bhurricane\b", r"\btornado\b", r"\bwildfire\b", r"\bflood(ing)?\b",
        r"\bstorm\b", r"\bblizzard\b", r"\bheatwave\b"
    ],
}

_cat_compiled = {k: [re.compile(pat, re.I) for pat in pats] for k, pats in _CATS.items()}

def categorize(text: str) -> str:
    """Return first matching category or 'uncategorized'."""
    if not text:
        return "uncategorized"
    for cat, patterns in _cat_compiled.items():
        if any(p.search(text) for p in patterns):
            return cat
    return "uncategorized"

# -------- Core write --------
def _append_event(event: Dict[str, Any]) -> None:
    event.setdefault("timestamp", datetime.datetime.utcnow().isoformat())
    with _WRITE_LOCK:
        with open(ANALYTICS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

# -------- Public API --------
def log_interaction(
    *,
    user_id: int,
    message: str,
    reply_len: int,
    response_time_ms: int,
    category: Optional[str] = None,
    error: bool = False,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log one completed Q->A interaction.
    """
    cat = category or categorize(message or "")
    event = {
        "type": "interaction",
        "user_id": user_id,
        "message": message,
        "category": cat,
        "response_time_ms": int(response_time_ms),
        "bot_reply_len": int(reply_len),
        "error": bool(error),
    }
    if meta:
        event["meta"] = meta
    _append_event(event)

def log_affiliate_impressions(
    *,
    user_id: int,
    message: Optional[str],
    category: Optional[str],
    items: Iterable[Dict[str, Any]] | int,
) -> None:
    """
    Log affiliate impressions (count or list of items).
    """
    if isinstance(items, int):
        count = items
        details = None
    else:
        details = [{"title": i.get("title"), "url": i.get("url")} for i in items]
        count = len(details)

    event = {
        "type": "affiliate_impressions",
        "user_id": user_id,
        "message": message,
        "category": category or categorize(message or ""),
        "count": int(count),
    }
    if details:
        event["items"] = details
    _append_event(event)

def log_affiliate_click(
    *,
    user_id: int,
    url: str,
    item_title: Optional[str] = None,
    category: Optional[str] = None,
) -> None:
    """
    Log a click on an affiliate link.
    (If you use external short links, call this when your redirect fires.)
    """
    event = {
        "type": "affiliate_click",
        "user_id": user_id,
        "url": url,
        "item_title": item_title,
        "category": category,
    }
    _append_event(event)

def log_affiliate_purchase(
    *,
    user_id: int,
    url: Optional[str] = None,
    item_title: Optional[str] = None,
    revenue_usd: Optional[float] = None,
    category: Optional[str] = None,
    order_id: Optional[str] = None,
) -> None:
    """
    Log a (reported) purchase. You can wire this up when you later ingest
    partner reports (Amazon PA-API / reports CSV).
    """
    event = {
        "type": "affiliate_purchase",
        "user_id": user_id,
        "url": url,
        "item_title": item_title,
        "revenue_usd": revenue_usd,
        "category": category,
        "order_id": order_id,
    }
    _append_event(event)

def log_system(
    *,
    level: str,
    msg: str,
    meta: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log system-level events (startup, webhook set, errors).
    """
    event = {"type": "system", "level": level, "msg": msg}
    if meta:
        event["meta"] = meta
    _append_event(event)

