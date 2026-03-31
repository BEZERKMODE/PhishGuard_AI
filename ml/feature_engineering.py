from __future__ import annotations

import re
import pandas as pd
from urllib.parse import urlparse
from backend.app.utils import safe_parse, estimate_entropy, looks_like_ip, SUSPICIOUS_KEYWORDS, TRUSTED_BRANDS, SHORTENERS


FEATURE_COLUMNS = [
    "url_length",
    "host_length",
    "path_length",
    "query_length",
    "num_dots",
    "num_hyphens",
    "num_underscores",
    "num_slashes",
    "num_digits",
    "num_special_chars",
    "has_https",
    "has_ip_address",
    "has_at_symbol",
    "uses_shortener",
    "subdomain_depth",
    "entropy",
    "suspicious_keyword_count",
    "brand_collision_count",
    "https_token_in_path_or_host",
]


def extract_features_from_url(url: str) -> dict:
    parsed, normalized_url = safe_parse(url)
    host = (parsed.netloc or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    full = normalized_url.lower()

    special_chars = re.findall(r"[^a-zA-Z0-9]", normalized_url)
    suspicious_keyword_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in full)
    brand_collision_count = sum(1 for b in TRUSTED_BRANDS if b in full and b not in host)
    uses_shortener = int(any(s in host for s in SHORTENERS))
    subdomain_depth = max(len([p for p in host.split(".") if p]) - 2, 0)

    return {
        "url_length": len(normalized_url),
        "host_length": len(host),
        "path_length": len(path),
        "query_length": len(query),
        "num_dots": normalized_url.count("."),
        "num_hyphens": normalized_url.count("-"),
        "num_underscores": normalized_url.count("_"),
        "num_slashes": normalized_url.count("/"),
        "num_digits": sum(c.isdigit() for c in normalized_url),
        "num_special_chars": len(special_chars),
        "has_https": int(parsed.scheme == "https"),
        "has_ip_address": int(looks_like_ip(host)),
        "has_at_symbol": int("@" in normalized_url),
        "uses_shortener": uses_shortener,
        "subdomain_depth": subdomain_depth,
        "entropy": estimate_entropy(normalized_url),
        "suspicious_keyword_count": suspicious_keyword_count,
        "brand_collision_count": brand_collision_count,
        "https_token_in_path_or_host": int("https" in host.replace("https://", "") or "https" in path),
    }


def build_feature_frame(df: pd.DataFrame, url_column: str = "url") -> pd.DataFrame:
    feature_rows = [extract_features_from_url(url) for url in df[url_column].astype(str)]
    X = pd.DataFrame(feature_rows)
    return X[FEATURE_COLUMNS]
