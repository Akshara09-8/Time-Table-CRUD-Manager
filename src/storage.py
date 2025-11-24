# src/storage.py
import json
from pathlib import Path
from typing import List
from .models import Entry

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "timetable.json"

class JsonStorage:
    def __init__(self, path: Path = DATA_FILE):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"entries": []})

    def _read(self) -> dict:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If file corrupted, overwrite with empty structure
            self._write({"entries": []})
            return {"entries": []}

    def _write(self, data: dict) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_entries(self) -> List[Entry]:
        data = self._read()
        entries = [Entry.from_dict(d) for d in data.get("entries", [])]
        return entries

    def save_entries(self, entries: List[Entry]) -> None:
        data = {"entries": [e.to_dict() for e in entries]}
        self._write(data)
