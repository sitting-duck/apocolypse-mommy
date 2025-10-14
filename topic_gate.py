# topic_gate.py — off-topic detector + nudges + /topics content

from __future__ import annotations

# Keywords that indicate the user is talking about preparedness
PREP_KEYWORDS = {
    # hazards & scenarios
    "blackout","power","outage","storm","hurricane","tornado","earthquake","wildfire",
    "evacuate","evacuation","shelter","blizzard","heatwave","flood","disaster","emergency",
    # essentials & gear
    "water","food","lighting","lantern","battery","batteries","radio","first aid","bandage",
    "trauma","ifak","generator","charger","power bank","filter","purifier","noaa","flashlight",
    # planning
    "go bag","gobag","bug out","72-hour","checklist","kit","preparedness","survival","responder"
}

def is_off_topic(text: str) -> bool:
    """
    Heuristic: very short/nonsense or no overlap with prep keywords.
    """
    if not text or text.strip() == "":
        return True
    t = text.lower().strip()
    only_letters = sum(c.isalpha() for c in t)
    if len(t) <= 3 and only_letters <= 3:
        return True
    for kw in PREP_KEYWORDS:
        if kw in t:
            return False
    return True

def nudge_text() -> str:
    return (
        "I’m here to help with emergency **preparedness**.\n\n"
        "Try something like:\n"
        "• *3-day power outage for a family of 4—what do we need?*\n"
        "• *What should go in a basic go-bag?*\n"
        "• *How much water should I store for two adults and a dog?*\n\n"
        "You can also send */topics* to see examples, or */buy radio* for quick links."
    )

TOPIC_EXAMPLES = [
    ("Blackout (72 hours)", "3-day power outage, two adults + one child, budget $150"),
    ("Go-bag (24–72h)", "What goes in a basic go-bag for two adults?"),
    ("Water planning", "How much water should I store for 3 people and a dog?"),
    ("First aid basics", "What should I keep for bleeding control at home?"),
    ("Storm prep", "Storm incoming this weekend—what should I do today?"),
    ("Communications", "How do I get NOAA weather alerts without internet?"),
]

def format_topics_list() -> str:
    lines = ["*Common scenarios I can help with:*"]
    for title, example in TOPIC_EXAMPLES:
        lines.append(f"• *{title}*: _{example}_")
    lines.append("\nTip: try */buy radio* or */buy first aid* for quick links.")
    return "\n".join(lines)

