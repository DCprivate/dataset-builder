import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Iterable, Any


def load_sources(json_path: str) -> list[dict]:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"Sources file not found: {json_path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Sources file must contain a JSON list")

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Source at index {i} must be an object")

        if "kind" not in item or "value" not in item:
            raise ValueError(f"Source at index {i} must contain 'kind' and 'value'")

        if not isinstance(item["kind"], str) or not isinstance(item["value"], str):
            raise ValueError(f"'kind' and 'value' must be strings at index {i}")

    return data


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_jsonl(records: Iterable[Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for record in records:
            if is_dataclass(record):
                record = asdict(record)
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")

    return path


def read_jsonl(input_path: str | Path) -> list[dict]:
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"JSONL file not found: {input_path}")

    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    return records
