# src/main.py
import sys
from typing import Optional
from .manager import TimetableManager
from .models import TimeSlot, Entry

def print_header():
    print("Class Time Table - CRUD Manager (CLI)")
   

def print_menu():
    print("\nSelect an option:")
    print("1) List all entries")
    print("2) Add entry")
    print("3) Update entry")
    print("4) Delete entry")
    print("5) Show entry details")
    print("6) Exit")

def input_nonempty(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Please enter a non-empty value.")

def choose_entry_id(manager: TimetableManager) -> Optional[str]:
    entries = manager.list_entries()
    if not entries:
        print("No entries available.")
        return None
    for e in entries:
        print(f"- {e.id} | {e.timeslot.day} {e.timeslot.start_time}-{e.timeslot.end_time} | {e.subject} | {e.teacher} | {e.room}")
    return input_nonempty("Enter entry ID: ")

def cmd_list(manager: TimetableManager):
    entries = manager.list_entries()
    if not entries:
        print("No entries yet.")
        return
    print("\nAll timetable entries:")
    for e in entries:
        print(f"[{e.id}] {e.timeslot.day} {e.timeslot.start_time}-{e.timeslot.end_time} | {e.subject} | {e.teacher} | {e.room}")

def cmd_add(manager: TimetableManager):
    try:
        subject = input_nonempty("Subject: ")
        teacher = input_nonempty("Teacher: ")
        room = input_nonempty("Room: ")
        day = input_nonempty("Day (e.g. Monday): ")
        start_time = input_nonempty("Start time (HH:MM 24-hour): ")
        end_time = input_nonempty("End time (HH:MM 24-hour): ")
        notes = input("Notes (optional): ").strip()
        entry = manager.add_entry(subject=subject, teacher=teacher, room=room, day=day, start_time=start_time, end_time=end_time, notes=notes)
        print(f"Added entry with ID {entry.id}")
    except Exception as ex:
        print("Error:", ex)

def cmd_update(manager: TimetableManager):
    try:
        entry_id = choose_entry_id(manager)
        if not entry_id:
            return
        e = manager.find_by_id(entry_id)
        if not e:
            print("Entry not found.")
            return
        print("Press Enter to keep current value.")
        subject = input(f"Subject [{e.subject}]: ").strip() or None
        teacher = input(f"Teacher [{e.teacher}]: ").strip() or None
        room = input(f"Room [{e.room}]: ").strip() or None
        day = input(f"Day [{e.timeslot.day}]: ").strip() or None
        start_time = input(f"Start time [{e.timeslot.start_time}]: ").strip() or None
        end_time = input(f"End time [{e.timeslot.end_time}]: ").strip() or None
        notes = input(f"Notes [{e.notes}]: ").strip() or None

        updated = manager.update_entry(entry_id, subject=subject, teacher=teacher, room=room, day=day, start_time=start_time, end_time=end_time, notes=notes)
        print(f"Updated entry {updated.id}")
    except Exception as ex:
        print("Error:", ex)

def cmd_delete(manager: TimetableManager):
    try:
        entry_id = choose_entry_id(manager)
        if not entry_id:
            return
        confirm = input(f"Type 'yes' to delete entry {entry_id}: ").strip().lower()
        if confirm == "yes":
            manager.delete_entry(entry_id)
            print("Deleted.")
        else:
            print("Aborted.")
    except Exception as ex:
        print("Error:", ex)

def cmd_show(manager: TimetableManager):
    entry_id = choose_entry_id(manager)
    if not entry_id:
        return
    e = manager.find_by_id(entry_id)
    if not e:
        print("Entry not found.")
        return
    print("\nEntry details:")
    print(f"ID      : {e.id}")
    print(f"Subject : {e.subject}")
    print(f"Teacher : {e.teacher}")
    print(f"Room    : {e.room}")
    print(f"Day     : {e.timeslot.day}")
    print(f"Time    : {e.timeslot.start_time} - {e.timeslot.end_time}")
    print(f"Notes   : {e.notes}")

def main():
    manager = TimetableManager()
    print_header()
    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            cmd_list(manager)
        elif choice == "2":
            cmd_add(manager)
        elif choice == "3":
            cmd_update(manager)
        elif choice == "4":
            cmd_delete(manager)
        elif choice == "5":
            cmd_show(manager)
        elif choice == "6" or choice.lower() in ("q","quit","exit"):
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Unknown choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
