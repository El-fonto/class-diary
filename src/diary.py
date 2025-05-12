import os
import json
import uuid
import datetime
from datetime import date


class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = str(uuid.uuid4())
        self.lesson_count = 1


class SessionNotes:
    def __init__(self, student: Student, session_date: date | None = None) -> None:
        self.student = student
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
        print(f"Date: {self.session_date}")
        print(f"Lesson #: {self.student.lesson_count}")
        print(f"Student: {self.student.name}")

        i = 1
        for timestamp, entry in self.entries:
            formatted_timestamp = timestamp.strftime("%H:%M:%S")
            print(f"🕑️{formatted_timestamp} #[{i}]: {entry}")
            i += 1


class Diary:
    def __init__(self, path) -> None:
        self.path = path
        self.internal_data = {}
        self.export_data = {}

        #!TODO:
        ## encapsulate get_or_create_student and add_notes in one

    def close(self):
        self.update_profile()
        self.internal_data["notes"].display_summary()
        self.save_to_file()

    def get_or_create_student(self, name: str) -> Student:
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

            # store strings to write files later
            self.export_data = {
                "id": new_student.id,
                "student_name": new_student.name,
                "lesson_count": new_student.lesson_count,
            }

            # store path and Student to use later
            self.internal_data = {
                "student": new_student,
                "student_profile": student_profile,
                "student_path": student_path,
            }

            return new_student

        # no profile -> create one
        print("No existing profile found. Creating one...")
        os.makedirs(student_path, exist_ok=True)

        new_student = Student(name)
        # store strings to write files later
        self.export_data = {
            "id": new_student.id,
            "student_name": new_student.name,
            "lesson_count": new_student.lesson_count,
        }

        # store path and Student to use later
        self.internal_data = {
            "student": new_student,
            "student_profile": student_profile,
            "student_path": student_path,
        }

        with open(student_profile, "w") as f:
            json.dump(self.export_data, f, indent=2, sort_keys=True)

        print(f"\n{new_student.name}'s profile created -> {student_profile}\n")

        return new_student

    def add_notes(self) -> SessionNotes:
        notes = SessionNotes(self.internal_data["student"])
        self.internal_data["notes"] = notes

        return self.internal_data["notes"]

    def update_profile(self):
        student_profile = self.internal_data["student_profile"]
        self.export_data["lesson_count"] += 1

        export_notes = []

        i = 1
        for timestamp, entry in self.internal_data["notes"].entries:
            formatted_timestamp = str(timestamp.strftime("%H:%M:%S"))
            export_notes.append(f"{formatted_timestamp} #[{i}]: {entry}")
            i += 1

        self.export_data["notes"] = export_notes

        #!TODO:
        ## encapsulate update and save_to_file into one

        with open(student_profile, "w") as f:
            json.dump(self.export_data, f, indent=2)

    def save_to_file(self):
        student_name = self.internal_data["student"].name
        session_date = self.internal_data["notes"].session_date.isoformat()

        note_file = f"{session_date}_{student_name}.json"
        filename = os.path.join(self.internal_data["student_path"], note_file)

        with open(filename, "w") as f:
            json.dump(self.export_data, f, indent=4)
