# affiliate_catalog.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class Item:
    title: str
    url: str
    tags: List[str]         # simple keywords to match user text
    notes: str = ""         # optional blurb

CATALOG: List[Item] = [
    Item(
        title="Gardeners Basics Survival Vegetable Seeds Kit (35 varieties, 16k+ Non-GMO Heirloom)",
        url="https://amzn.to/4nOGOUw",
        tags=["seed","garden","gardening","food","grow","homestead"],
        notes="Long-term food security; store cool/dry."
    ),
    Item(
        title="Raynic NOAA/Solar/Crank Emergency Weather Radio (5000mAh, flashlight, charger)",
        url="https://amzn.to/4714QVe",
        tags=["radio","noaa","crank","weather","blackout","storm","hurricane","tornado","power","outage","emergency"],
        notes="Weather alerts + phone charging during outages."
    ),
    Item(
        title='RHINO RESCUE 6" Israeli-Style Emergency Bandage (5 pack)',
        url="https://amzn.to/3IIbl7t",
        tags=["bandage","trauma","first aid","ifak","wound","bleeding","tourniquet","medical"],
        notes="Compression bandage for serious bleeding."
    ),
    Item(
        title="Straw Water Filter (5 pack) – personal emergency water purifier",
        url="https://amzn.to/3J3wkS4",
        tags=["water","filter","purifier","drink","hydration","camping","hiking","boil","contamination"],
        notes="Compact filtration for on-the-go water."
    ),
    Item(
        title="13-in-1 Survival Multitool Hammer",
        url="https://amzn.to/42Gwh5w",
        tags=["multitool","tool","hammer","pliers","knife","camping","repair","kit"],
        notes="Handy do-everything tool for kits."
    ),
    Item(
        title='Emergency Fire Blanket 40"x40"',
        url="https://amzn.to/4mZ4ww3",
        tags=["fire","blanket","kitchen","grease","electrical","safety"],
        notes="Smothers small kitchen/electrical fires fast."
    ),
]

def find_matches(user_text: str, max_items: int = 3) -> List[Item]:
    """Very simple matcher: score by keyword overlaps; return top few."""
    txt = user_text.lower()
    scores: Dict[int, int] = {}
    for i, item in enumerate(CATALOG):
        hit = sum(1 for t in item.tags if t in txt)
        if hit:
            scores[i] = hit
    ranked_idx = sorted(scores, key=lambda k: scores[k], reverse=True)
    return [CATALOG[i] for i in ranked_idx[:max_items]]

def preset_for_scenario(scenario: str) -> List[Item]:
    sc = scenario.lower()
    if any(k in sc for k in ["blackout","power","outage"]):
        return [CATALOG[1], CATALOG[3], CATALOG[5]]  # radio, water filter, fire blanket
    if any(k in sc for k in ["first aid","trauma","bleeding","ifak"]):
        return [CATALOG[2], CATALOG[4]]
    if any(k in sc for k in ["garden","food","seed"]):
        return [CATALOG[0]]
    # fallback: nothing
    return []

