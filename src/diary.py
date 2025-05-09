# import os
# import json
# import uuid
import datetime
from datetime import date, time


class Student:
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id


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


"""
class Diary:
    def __init__(self, path) -> None:
        self.path = path

    def get_or_create_student(self, student_name):
        pass

    def save_to_file(self, data_dir):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        session_data = {
            "student": .student.name,
            "session_date": self.session_date.isoformat(),
            "entries": self.entries,
            "timestamps": self.timestamps,
        }

        filename = f"{self.session_date.isoformat()}_{self.student.name}.json"
        filepath = os.path.join(data_dir, filename)

        with open(filename, "w") as f:
            json.dump(session_data, f, indent=4)

        return filepath
"""
