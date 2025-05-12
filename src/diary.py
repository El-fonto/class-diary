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

    def get_or_create_student(self, name: str) -> Student:
        student_path = os.path.join(self.path, name)
        filename = f"{name}_profile.json"
        student_profile = os.path.join(student_path, filename)

        # there's a folder
        if os.path.exists(student_path) and os.path.isfile(student_profile):
            with open(student_profile, "r") as f:
                loaded_profile = json.load(f)

            new_student = Student(loaded_profile.get("student_name", name))
            new_student.id = loaded_profile.get("id", "Unknown")
            new_student.lesson_count = loaded_profile.get("lesson_count")

            # store in internal dict to use later
            self.export_data = {
                "student_name": new_student.name,
                "id": new_student.id,
                "lesson_count": new_student.lesson_count,
            }

            self.internal_data = {
                "student": new_student,
                "student_profile": student_profile,
            }

            return new_student

        # no profile -> create one
        print("No existing profile found. Creating one...")
        os.makedirs(student_path, exist_ok=True)

        new_student = Student(name)
        self.export_data = {
            "student_name": new_student.name,
            "id": new_student.id,
            "lesson_count": new_student.lesson_count,
        }

        self.internal_data = {
            "student": new_student,
            "student_profile": student_profile,
        }

        with open(student_profile, "w") as f:
            json.dump(self.export_data, f, indent=2, sort_keys=True)

        print(f"\n{new_student.name}'s profile created -> {student_profile}\n")

        return new_student

    def add_notes(self) -> SessionNotes:
        notes = SessionNotes(self.internal_data["student"])

        self.internal_data["date"] = notes.session_date
        return notes

    def update_profile(self):
        filename = f"{self.export_data["student_name"]}_profile.json"
        profile_path = os.path.join(
            self.path, self.export_data["student_name"], filename
        )
        self.export_data["lesson_count"] += 1

        #!TODO:
        ## add session entries to session_data and add this to the profile with a good syntax in the json

        with open(profile_path, "w") as f:
            json.dump(self.export_data, f, indent=2, sort_keys=True)

    def save_to_file(self):
        student_name = self.internal_data["student"].name
        session_date = self.internal_data["date"].isoformat()

        filename = f"{session_date}_{student_name}.json"

        """
        # if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.session_data["student"] = 
        session_data = {
            "student": .name,
            "session_date": self.session_date.isoformat(),
            "entries": self.entries,
            "timestamps": self.timestamps,
        }

        filename = f"{self.session_date.isoformat()}_{self.name}.json"
        filepath = os.path.join(dest_path, filename)

        with open(filename, "w") as f:
            json.dump(session_data, f, indent=4)

        return filepath
"""
