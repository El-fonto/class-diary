import os
import json
import uuid
import datetime
from datetime import date
# from pyfiglet import Figlet


class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = str(uuid.uuid4())
        self.lesson_count = 1


class SessionNotes:
    def __init__(
        self, student: Student, lesson_title: str, session_date: date | None = None
    ) -> None:
        self.student = student
        self.lesson_title = lesson_title
        self.session_date = session_date or date.today()
        self.entries: list[tuple[datetime.datetime, str]] = []

    def add_entry(self, entry: str) -> None:
        timestamp = datetime.datetime.now()
        self.entries.append((timestamp, entry))

    def display_summary(self):
        if not self.entries:
            print("No entries this session")
            return

        print("\nClass Summary:")
        print(f"Date: {self.session_date} - Student: {self.student.name}")
        print(
            f"Lesson #: {self.student.lesson_count} - {self.lesson_title} with #{len(self.entries)} notes:"
        )

        i = 1
        for timestamp, entry in self.entries:
            formatted_timestamp = timestamp.strftime("%H:%M:%S")
            print(f"🕑️{formatted_timestamp} #[{i}]: {entry}")
            i += 1


class Diary:
    def __init__(self, path) -> None:
        self.path = path
        self.data = {}
        self.open()

    def open(self):
        today = date.today().strftime("%A %d %B %Y")
        # f = Figlet(font="slant")
        # print(f.renderText("Class Diary"))
        print(f"Today's date: {today}")

    def close(self):
        self.update_profile()
        self.data["notes"].display_summary()
        self.save_to_file()

    def add_notes(self, lesson_title: str) -> SessionNotes:
        notes = SessionNotes(self.data["student"], lesson_title)
        self.data["notes"] = notes

        return self.data["notes"]

    def get_or_create_profile(self, name: str) -> Student:
        student_path = os.path.join(self.path, name)
        filename = f"00_{name}_profile.json"
        student_profile = os.path.join(student_path, filename)

        # there's a folder
        if os.path.exists(student_path) and os.path.isfile(student_profile):
            with open(student_profile, "r") as f:
                loaded_profile = json.load(f)

            new_student = Student(loaded_profile.get("student_name", name))
            new_student.id = loaded_profile.get("id", "Unknown")
            new_student.lesson_count = loaded_profile.get("lesson_count")
            existing_notes = loaded_profile.get("lesson_notes")

            self.data = {
                "student": new_student,
                "student_profile": student_profile,
                "student_path": student_path,
                "to_export": {
                    "id": new_student.id,
                    "student_name": new_student.name,
                    "lesson_count": new_student.lesson_count,
                    "lesson_notes": [
                        existing_notes,
                    ],
                },
            }

            return new_student

        # no profile -> create one
        print("No existing profile found. Creating one...")
        os.makedirs(student_path, exist_ok=True)

        new_student = Student(name)

        self.data = {
            "student": new_student,
            "student_profile": student_profile,
            "student_path": student_path,
            "to_export": {
                "id": new_student.id,
                "student_name": new_student.name,
                "lesson_count": new_student.lesson_count,
            },
        }

        with open(student_profile, "w") as f:
            json.dump(self.data["to_export"], f, indent=2, sort_keys=True)

        print(f"{new_student.name}'s profile created -> {student_profile}\n")

        return new_student

    def update_profile(self):
        student_profile = self.data["student_profile"]
        self.data["to_export"]["lesson_count"] += 1

        title = self.data["notes"].lesson_title
        formatted_date = str(self.data["notes"].session_date.strftime("%A %d %B %Y"))

        export_notes = [f"{formatted_date}-{title}"]

        i = 1
        for timestamp, entry in self.data["notes"].entries:
            formatted_timestamp = str(timestamp.strftime("%H:%M:%S"))
            export_notes.append(f"{formatted_timestamp} #[{i}]: {entry}")
            i += 1

        if "lesson_notes" in self.data["to_export"]:
            self.data["to_export"]["lesson_notes"].append(export_notes)
        else:
            self.data["to_export"]["lesson_notes"] = export_notes

        with open(student_profile, "w") as f:
            json.dump(self.data["to_export"], f, indent=2)

    def save_to_file(self):
        student_name = self.data["student"].name
        session_date = self.data["notes"].session_date.isoformat()

        note_file = f"{session_date}_{student_name}.json"
        filename = os.path.join(self.data["student_path"], note_file)

        with open(filename, "w") as f:
            json.dump(self.data["to_export"], f, indent=2)
