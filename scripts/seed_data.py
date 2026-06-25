import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.database import init_db
from app.models import EventIn
from app.services.ingestion import ingest_event


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> None:
    init_db()
    sample_dir = ROOT / "data" / "sample"
    count = 0

    for file_path in sample_dir.glob("*.jsonl"):
        for payload in load_jsonl(file_path):
            event = EventIn(**payload)
            ingest_event(event)
            count += 1

    print(f"Seeded {count} events into local data lake.")


if __name__ == "__main__":
    main()
