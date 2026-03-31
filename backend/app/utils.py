import re
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "banking", "confirm",
    "password", "signin", "authenticate", "wallet", "invoice", "suspended",
    "urgent", "gift", "claim", "pay", "refund", "security"
]

TRUSTED_BRANDS = [
    "google", "microsoft", "paypal", "apple", "amazon", "netflix",
    "instagram", "facebook", "whatsapp", "bank", "github"
]

SHORTENERS = [
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "is.gd", "ow.ly", "buff.ly"
]


def safe_parse(url: str):
    if not re.match(r"^https?://", url):
        url = "http://" + url
    return urlparse(url), url


def estimate_entropy(text: str) -> float:
    if not text:
        return 0.0
    from math import log2
    probs = [text.count(c) / len(text) for c in set(text)]
    return -sum(p * log2(p) for p in probs if p > 0)


def looks_like_ip(host: str) -> bool:
    return bool(re.match(r"^(\d{1,3}\.){3}\d{1,3}$", host or ""))


def extract_reason_flags(url: str, features: dict) -> list[str]:
    reasons = []
    lower_url = url.lower()

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in lower_url:
            reasons.append(f"Contains suspicious keyword: {keyword}")
            if len(reasons) >= 3:
                break

    if features.get("url_length", 0) > 75:
        reasons.append("Long URL length")
    if features.get("num_hyphens", 0) >= 3:
        reasons.append("Too many hyphens")
    if features.get("num_dots", 0) >= 4:
        reasons.append("Too many dots / subdomains")
    if features.get("has_ip_address", 0) == 1:
        reasons.append("Uses IP address instead of domain")
    if features.get("uses_shortener", 0) == 1:
        reasons.append("Uses URL shortener")
    if features.get("has_at_symbol", 0) == 1:
        reasons.append("Contains @ symbol")
    if features.get("https_token_in_path_or_host", 0) == 1:
        reasons.append("Contains misleading 'https' token in URL")
    if features.get("brand_collision_count", 0) >= 1:
        reasons.append("Potential brand impersonation pattern")

    return reasons[:5] or ["No strong suspicious indicators found"]
