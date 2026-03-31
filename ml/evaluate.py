from __future__ import annotations

import json
from pathlib import Path

METRICS_PATH = Path("models/training_metrics.json")


def main():
    if not METRICS_PATH.exists():
        raise FileNotFoundError("Training metrics not found. Run python ml/train.py first.")
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
