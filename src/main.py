from pathlib import Path
from datetime import date
from diary import Diary, Session


# from pyfiglet import Figlet

profile_path = Path("../content/profiles/")
#!TODO:
# get and update are methods of Diary
# The hello message should be encapsulated as hello
# Diary should create a new folder per student, each folder should contain: profile + class_entries
# Next up, would be getting the Calendar working


def main():
    today = date.today()
    # f = Figlet(font="slant")
    # print(f.renderText("Class Diary"))
    print(f"Today's date: {today}")

    name = input("Who's taking the class: ").title()
    lesson = input("Which lesson: ").title()
    diary = Diary(profile_path)

    student = diary.get_or_create_student(name)

    print(f"Starting session with: {student.name}")
    print(f"With a lesson about: {lesson}")

    session = Session(student, today)

    while True:
        entry = input("=====> data: (or 'done'): ").strip()
        if entry.lower() == "done":
            break
        session.add_entry(entry)
        print(f"Saved entry at {session.entries[-1][0]}")

    session.display_summary()


if __name__ == "__main__":
    main()
