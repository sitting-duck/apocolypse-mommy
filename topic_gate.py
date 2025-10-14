# topic_gate.py — preparedness + fieldcraft + hunting + martial arts (safety-first)
from __future__ import annotations
import re

# ------------------------------------------------------------
# Tokenization helpers
# ------------------------------------------------------------
# Safe word extractor: start with a letter, then letters / apostrophes / hyphens.
# Hyphen is placed at the end of the class to avoid "bad character range" errors.
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z’'-]+")  # allows straight/curly apostrophes and hyphens

def _normalize(text: str) -> str:
    """Lowercase and keep simple word-like tokens."""
    return " ".join(_WORD_RE.findall((text or "").lower()))

def _contains_phrase(text: str, phrases: list[str]) -> bool:
    t = (text or "").lower()
    return any(p in t for p in phrases)

def _has_any(text: str, terms: list[str]) -> bool:
    t = (text or "").lower()
    return any(term in t for term in terms)

# ------------------------------------------------------------
# Scope configuration
# ------------------------------------------------------------
# Core preparedness + fieldcraft signals (single tokens)
CORE_TOKENS = {
    # hazards & scenarios
    "blackout","power","outage","storm","hurricane","tornado","earthquake","wildfire",
    "evacuate","evacuation","shelter","blizzard","heatwave","flood","disaster","emergency",
    # essentials & gear
    "water","food","lighting","lantern","battery","batteries","radio","first","aid","bandage",
    "trauma","ifak","generator","charger","power","bank","filter","purifier","noaa","flashlight",
    # comms/off-grid & info
    "comms","communication","communications","ham","gmrs","frs","mesh","satellite","satphone",
    "offline","offgrid","off-grid","internet","grid","grid-down","griddown",
    "map","maps","paper","print","book","books","handbook","manual",
    # fieldcraft / ranger-handbook style topics (high level)
    "navigation","land","nav","compass","bearing","pace","count","sheltercraft","campcraft",
    "firecraft","knots","cordage","foraging","edible","plants","tracking","signaling","signalling",
    # planning & meta
    "gobag","go","bag","bug","out","72-hour","checklist","kit","preparedness","survival","responder",
}

# Explicit phrases that are clearly preparedness-adjacent
ACCEPT_PHRASES = [
    # off-grid / no-internet
    "no internet","without internet","offline only","off grid","off-grid","grid down","grid-down",
    # info & reference
    "paper maps","print resources","reference library","book list","field manual",
    # hunting (safety/legal framing encouraged)
    "hunting safety","hunter education","ethical hunting","wild game processing basics",
    # martial arts (fitness/awareness framing)
    "martial arts conditioning","martial arts for fitness","de-escalation","situational awareness",
]

# Sensitive areas that require safety/legal framing
SENSITIVE_TOPICS = [
    # weapons / martial arts broad terms
    "weapon","weapons","firearm","firearms","gun","guns","knife","knives","martial arts","mma","combat",
    "strike","choke","armbar","takedown","grappling",
    # hunting when not clearly ethical/legal
    "hunting","bow","archery","rifle","shotgun","trap","snare",
]

# Qualifiers that legitimize sensitive topics (safety-first, legal)
SAFETY_QUALIFIERS = [
    "safety","safe","legal","lawful","ethics","ethical","rules","storage","handling",
    "training","certified","education","awareness","de-escalation","avoid","prevent","nonviolent",
]

# Explicitly disallowed (hard block) — harmful/illegal instructions
HARD_BLOCK = [
    "how to make a bomb","build a bomb","improvised explosive","manufacture explosive",
    "bypass background check","ghost gun","silencer plan","poaching","how to hurt",
    "fatal strike","vital points to kill","homemade weapon","booby trap","landmine",
]

# Risky operational terms — redirect unless clearly safety/legal
RISKY_TERMS = [
    "warfare","attack","ambush","assault","improvised","jamming","signal jammer","tracking device",
    "surveillance device","poison","lure animal illegally","snare without permit",
]

# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
def is_prep_related(text: str) -> bool:
    """
    Accept if:
      - explicit ACCEPT_PHRASES appear, OR
      - any token overlaps CORE_TOKENS, OR
      - the text mentions a SENSITIVE_TOPIC together with a SAFETY_QUALIFIER
    """
    if not text or not text.strip():
        return False
    t = _normalize(text)

    if _contains_phrase(t, ACCEPT_PHRASES):
        return True

    tokens = set(t.split())
    if tokens & CORE_TOKENS:
        return True

    if _has_any(t, SENSITIVE_TOPICS) and _has_any(t, SAFETY_QUALIFIERS):
        return True

    return False

def needs_safety_redirect(text: str) -> bool:
    """
    Redirect when:
      - hard-blocked phrases appear, OR
      - risky operational terms appear WITHOUT safety/legal qualifiers, OR
      - sensitive topics appear WITHOUT safety/legal qualifiers
    """
    t = _normalize(text)
    if _contains_phrase(t, HARD_BLOCK):
        return True

    risky = _has_any(t, RISKY_TERMS)
    sensitive = _has_any(t, SENSITIVE_TOPICS)
    qualified = _has_any(t, SAFETY_QUALIFIERS)

    if (risky or sensitive) and not qualified:
        return True

    return False

def nudge_text() -> str:
    return (
        "I’m here to help with **preparedness & fieldcraft** (lawful, safety-first).\n\n"
        "Try:\n"
        "• *3-day power outage for a family of 4 — what do we need?*\n"
        "• *No internet/off-grid — how do I keep info & comms?*\n"
        "• *Hunting safety & ethical basics for emergencies?*\n"
        "• *Martial arts for fitness & de-escalation?*\n\n"
        "See */topics* for more, or */buy radio* for quick links."
    )

TOPIC_EXAMPLES = [
    ("Blackout (72 hours)", "3-day power outage, two adults + one child, budget $150"),
    ("No-internet / Off-grid", "No internet at home — how do I keep info and communications?"),
    ("Fieldcraft basics", "Paper maps, compass, and land nav pacing — where to start?"),
    ("Hunting (legal & ethical)", "What are the safety basics and legal steps for new hunters?"),
    ("Martial arts (fitness & awareness)", "Best conditioning & de-escalation drills for beginners?"),
    ("First aid", "What should I keep for bleeding control at home?"),
    ("Comms", "How do I get NOAA weather alerts without internet?"),
]

def format_topics_list() -> str:
    lines = ["*Common scenarios I can help with (safety-first, legal only):*"]
    for title, example in TOPIC_EXAMPLES:
        lines.append(f"• *{title}*: _{example}_")
    lines.append("\nTip: try */buy radio* or */buy first aid* for quick links.")
    return "\n".join(lines)

def safety_redirect_text() -> str:
    return (
        "I can’t help with instructions that enable harm or illegal activity.\n\n"
        "If your goal is **staying safe and legal**, I can cover:\n"
        "• De-escalation, awareness, and fitness from martial arts\n"
        "• Firearm/weapon **safety**, storage, and certified training resources (no tactics)\n"
        "• Hunting **safety**, licensing, seasons, and ethical practices\n"
        "• Off-grid readiness: comms, power, first aid, water, and printed references\n\n"
        "Try rephrasing with a **safety/legal** focus (e.g., “hunting **safety & ethics**”)."
    )

