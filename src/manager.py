# src/manager.py
from typing import List, Optional
from datetime import datetime
from .models import Entry, TimeSlot, generate_id
from .storage import JsonStorage

class TimetableManager:
    DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    def __init__(self, storage: Optional[JsonStorage] = None):
        self.storage = storage or JsonStorage()
        self.entries: List[Entry] = self.storage.load_entries()

    # ---------- Persistence ----------
    def save(self) -> None:
        self.storage.save_entries(self.entries)

    # ---------- CRUD operations ----------
    def list_entries(self) -> List[Entry]:
        return list(self.entries)

    def find_by_id(self, entry_id: str) -> Optional[Entry]:
        for e in self.entries:
            if e.id == entry_id:
                return e
        return None

    def add_entry(self, subject: str, teacher: str, room: str, day: str, start_time: str, end_time: str, notes: str="") -> Entry:
        day = day.capitalize()
        self._validate_day(day)
        self._validate_time_format(start_time)
        self._validate_time_format(end_time)
        self._validate_time_order(start_time, end_time)
        new_ts = TimeSlot(day=day, start_time=start_time, end_time=end_time)

        # check conflict
        if self._conflicts_with_existing(new_ts, teacher=teacher, room=room):
            raise ValueError("Time conflict detected: same teacher or room already has a class in this time.")

        new_entry = Entry(id=generate_id(), subject=subject.strip(), teacher=teacher.strip(), room=room.strip(), timeslot=new_ts, notes=notes.strip())
        self.entries.append(new_entry)
        self.save()
        return new_entry

    def update_entry(self, entry_id: str, subject: Optional[str]=None, teacher: Optional[str]=None, room: Optional[str]=None, day: Optional[str]=None, start_time: Optional[str]=None, end_time: Optional[str]=None, notes: Optional[str]=None) -> Entry:
        entry = self.find_by_id(entry_id)
        if not entry:
            raise ValueError("Entry not found")

        # Prepare tentative values
        new_day = day.capitalize() if day else entry.timeslot.day
        self._validate_day(new_day)

        new_start = start_time if start_time else entry.timeslot.start_time
        new_end = end_time if end_time else entry.timeslot.end_time
        self._validate_time_format(new_start)
        self._validate_time_format(new_end)
        self._validate_time_order(new_start, new_end)

        new_teacher = teacher.strip() if teacher else entry.teacher
        new_room = room.strip() if room else entry.room

        new_ts = TimeSlot(day=new_day, start_time=new_start, end_time=new_end)

        # check conflict excluding this entry itself
        if self._conflicts_with_existing(new_ts, teacher=new_teacher, room=new_room, exclude_id=entry.id):
            raise ValueError("Time conflict detected with another entry.")

        # apply updates
        if subject is not None:
            entry.subject = subject.strip()
        entry.teacher = new_teacher
        entry.room = new_room
        entry.timeslot = new_ts
        if notes is not None:
            entry.notes = notes.strip()

        self.save()
        return entry

    def delete_entry(self, entry_id: str) -> None:
        before = len(self.entries)
        self.entries = [e for e in self.entries if e.id != entry_id]
        after = len(self.entries)
        if before == after:
            raise ValueError("Entry ID not found")
        self.save()

    # ---------- Helpers ----------
    def _validate_day(self, day: str) -> None:
        if day.capitalize() not in self.DAYS:
            raise ValueError(f"Invalid day '{day}'. Expected one of: {', '.join(self.DAYS)}")

    def _validate_time_format(self, t: str) -> None:
        try:
            datetime.strptime(t, "%H:%M")
        except Exception:
            raise ValueError(f"Invalid time format '{t}'. Expected HH:MM in 24-hour format.")

    def _validate_time_order(self, start: str, end: str) -> None:
        s = datetime.strptime(start, "%H:%M")
        e = datetime.strptime(end, "%H:%M")
        if not s < e:
            raise ValueError("Start time must be before end time.")

    def _overlap(self, a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
        a_s = datetime.strptime(a_start, "%H:%M")
        a_e = datetime.strptime(a_end, "%H:%M")
        b_s = datetime.strptime(b_start, "%H:%M")
        b_e = datetime.strptime(b_end, "%H:%M")
        # overlap if intervals intersect
        return not (a_e <= b_s or b_e <= a_s)

    def _conflicts_with_existing(self, timeslot: TimeSlot, teacher: str, room: str, exclude_id: Optional[str]=None) -> bool:
        for e in self.entries:
            if exclude_id and e.id == exclude_id:
                continue
            if e.timeslot.day != timeslot.day:
                continue
            if self._overlap(e.timeslot.start_time, e.timeslot.end_time, timeslot.start_time, timeslot.end_time):
                # conflict if same teacher or same room
                if e.teacher.lower() == teacher.lower() or e.room.lower() == room.lower():
                    return True
        return False
