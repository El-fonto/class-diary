import os
import json
from datetime import date
from pyfiglet import Figlet
from session import Student, Session

DATA_DIARY = "../diary_data"
DATA_PROFILE = "./diary_data/profiles"

#!TODO: update and get should be methods of Student
# The hello message should be encapsulated as hello
# Sessions should create a new folder per student, each folder should contain: profile + class_entries
# Next up, would be getting the Calendar working


def update_student_profile(student_name, data_dir=DATA_DIARY) -> int:
    profile_path = os.path.join(data_dir, f"{student_name}_profile.json")

    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            student_data = json.load(f)
            lesson_count = student_data.get("lesson_count", 0) + 1
    else:
        lesson_count = 1

    student_data = {
        "name": student_name,
        "lesson_count": lesson_count,
    }

    with open(profile_path, "w") as f:
        json.dump(student_data, f, indent=2)

    return lesson_count


def get_student_profile(student_name, data_dir=DATA_DIARY) -> Student:
    profile_path = os.path.join(data_dir, f"{student_name}_profile.json")

    if os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            student_data = json.load(f)
            return Student(student_data["name"], student_data["lesson_count"])
    else:
        return Student(student_name, 0)


def main():
    today = date.today()
    f = Figlet(font="slant")
    print(f.renderText("Class Diary"))
    print(f"Today's date: {today}")

    student_name = input("Who's taking the class: ").title()
    student = get_student_profile(student_name)

    print(f"Starting session with {student_name}, lesson #{student.lesson_count + 1}")

    session = Session(student, today)

    # main loop that should
    while True:
        entry = input("=====> data: (or 'done'): ").strip()
        if entry.lower() == "done":
            break
        session.add_entry(entry)
        print(f"\n   Saved entry at {session.timestamps[-1]}")

    session_file = session.save_to_file(data_dir=DATA_DIARY)

    lesson_number = update_student_profile(student_name, DATA_DIARY)

    print("\nClass Summary:")
    print(f"Date: {session.session_date}")
    print(f"Student: {session.student.name}")
    print(f"Lesson # {lesson_number}")

    for i, (timestamp, entry) in enumerate(zip(session.timestamps, session.entries), 1):
        print(f"🕑️{timestamp} #{i}: {entry}")
    print(f"\nSession saved at {session_file}")


if __name__ == "__main__":
    main()
