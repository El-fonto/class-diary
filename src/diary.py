import os
import json
import uuid
import datetime
from datetime import date, time


class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = str(uuid.uuid4())
        self.lesson_count = 1


class Session:
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
        print(f"Student: {self.student.name}")

        i = 1
        for timestamp, entry in self.entries:
            formatted_timestamp = timestamp.strftime("%H:%M:%S")
            print(f"🕑️{formatted_timestamp} #{i}: {entry}")
            i += 1


class Diary:
    def __init__(self, path) -> None:
        self.path = path
        self.session_data = {}

    def get_or_create_student(self, name: str) -> Student:
        filename = f"{name}_profile.json"

        # traverses the directory looking for a folder with student's name
        for file in os.listdir(self.path):
            student_path = os.path.join(file, name)

            # there's a folder
            if os.path.exists(student_path):
                student_profile = os.path.join(student_path, filename)

                # there's a file
                if os.path.isfile(student_profile):
                    with open(filename, "r") as f:
                        loaded_profile = json.load(f)

                    name = loaded_profile.get("name", "Unknown")
                    id = loaded_profile.get("id", "Unknown")
                    lesson_count = loaded_profile.get("lesson_count", 1)
                    print(f"{name} was found! ID:{id}")
                    print(f"Lesson #{lesson_count}")
                    student = Student(name)
                    student.id = id
                    student.lesson_count = lesson_count
                    return student

        # no dir, no file, no profile -> create one
        student_path = os.path.join(self.path, name)
        if not os.path.exists(student_path):
            os.mkdir(student_path)

        student_profile = os.path.join(student_path, filename)

        print(f"No existing profile found at {student_path}")
        print(f"Creating a new profile for: {name}")

        new_student = Student(name)
        self.session_data["name"] = new_student.name
        self.session_data["id"] = new_student.id
        self.session_data["lesson_count"] = new_student.lesson_count

        with open(filename, "w") as f:
            json.dump(self.session_data, f, indent=2, sort_keys=True)

        print(f"Profile for: {new_student.name} created at {student_profile}")
        print(
            f"{new_student.name}, ID:{new_student.id}, lesson #{new_student.lesson_count}"
        )

        return new_student

    """
    def save_to_file(self, dest_path, session):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

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
