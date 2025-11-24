# src/models.py
from dataclasses import dataclass, asdict
from typing import Dict
import uuid

@dataclass
class TimeSlot:
    day: str            # e.g. 'Monday'
    start_time: str     # 'HH:MM' 24-hour
    end_time: str       # 'HH:MM' 24-hour

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict):
        return TimeSlot(day=d["day"], start_time=d["start_time"], end_time=d["end_time"])


@dataclass
class Entry:
    id: str             # unique id (string)
    subject: str
    teacher: str
    room: str
    timeslot: TimeSlot
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "subject": self.subject,
            "teacher": self.teacher,
            "room": self.room,
            "timeslot": self.timeslot.to_dict(),
            "notes": self.notes,
        }

    @staticmethod
    def from_dict(d: Dict):
        ts = TimeSlot.from_dict(d["timeslot"])
        return Entry(id=d["id"], subject=d["subject"], teacher=d["teacher"], room=d["room"], timeslot=ts, notes=d.get("notes",""))

def generate_id() -> str:
    return uuid.uuid4().hex[:8]
