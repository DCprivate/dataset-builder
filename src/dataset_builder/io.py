from __future__ import annotations

from pathlib import Path
from typing import Iterable

import orjson
import pandas as pd


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_jsonl(records: Iterable[dict], path: str | Path) -> None:
    with open(path, "wb") as f:
        for record in records:
            f.write(orjson.dumps(record))
            f.write(b"\n")


def write_parquet(records: list[dict], path: str | Path) -> str:
    df = pd.DataFrame(records)
    try:
        df.to_parquet(path, index=False)
        return "parquet"
    except ImportError:
        csv_path = Path(path).with_suffix(".csv")
        df.to_csv(csv_path, index=False)
        return str(csv_path)
