from __future__ import annotations

import random
import pandas as pd
from pathlib import Path

LEGIT_DOMAINS = [
    "google.com", "microsoft.com", "github.com", "amazon.com", "apple.com",
    "wikipedia.org", "openai.com", "python.org", "stackoverflow.com", "netflix.com"
]

PHISH_PATTERNS = [
    "secure-{brand}-login-check.com",
    "{brand}-account-verify-alert.net",
    "{brand}-wallet-security-update.org",
    "login-{brand}-confirm-now.com",
    "urgent-{brand}-password-reset.co",
    "{brand}-gift-claim-bonus.info",
]

BRANDS = ["paypal", "amazon", "microsoft", "apple", "netflix", "instagram", "github"]


def random_legit_url() -> str:
    domain = random.choice(LEGIT_DOMAINS)
    path = random.choice(["/", "/about", "/pricing", "/login", "/docs", "/support"])
    scheme = random.choice(["https", "https", "https", "http"])
    return f"{scheme}://www.{domain}{path}"


def random_phish_url() -> str:
    pattern = random.choice(PHISH_PATTERNS)
    brand = random.choice(BRANDS)
    domain = pattern.format(brand=brand)
    path = random.choice([
        "/login", "/verify", "/secure/account", "/confirm-now",
        "/update/billing", "/signin/auth"
    ])
    scheme = random.choice(["http", "http", "https"])
    return f"{scheme}://{domain}{path}"


def main():
    random.seed(42)
    rows = []
    for _ in range(2000):
        rows.append({"url": random_legit_url(), "label": 0})
    for _ in range(2000):
        rows.append({"url": random_phish_url(), "label": 1})

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)

    out = Path("data/raw/phishing_urls.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Saved sample dataset to {out} with shape {df.shape}")


if __name__ == "__main__":
    main()
