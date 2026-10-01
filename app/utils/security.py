SUSPICIOUS_PHRASES = [
    "ignore previous",
    "system prompt",
    "you are now",
]

def is_suspicious(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in SUSPICIOUS_PHRASES)                          
                