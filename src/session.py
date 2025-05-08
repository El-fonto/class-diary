import os
import json
import datetime
from datetime import date


class Student:
    def __init__(self, name: str | None, lesson_count: int = 0) -> None:
        self.name = name
        self.lesson_count = lesson_count


class Session:
    def __init__(self, student: Student, session_date: date | None = None) -> None:
        self.student = student
        self.session_date = session_date or date.today()
        self.entries = []
        self.timestamps = []

    def add_entry(self, entry: str) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.timestamps.append(timestamp)
        self.entries.append(entry)

    def save_to_file(self, data_dir="data_diary"):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        session_data = {
            "student": self.student.name,
            "session_date": self.session_date.isoformat(),
            "entries": self.entries,
            "timestamps": self.timestamps,
        }

        filename = f"{self.session_date.isoformat()}_{self.student.name}.json"
        filepath = os.path.join(data_dir, filename)

        with open(filename, "w") as f:
            json.dump(session_data, f, indent=4)

        return filepath
