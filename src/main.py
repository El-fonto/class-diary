# import os
from datetime import date
from diary import Student, Session

# from pyfiglet import Figlet

# PROFILES_PATH = "./content/profiles"
# STUDENT_PATH = os.path.join(PROFILES_PATH, f"{student.name}")

#!TODO: update and get should be methods of Student
# The hello message should be encapsulated as hello
# Sessions should create a new folder per student, each folder should contain: profile + class_entries
# Next up, would be getting the Calendar working


def main():
    today = date.today()
    # f = Figlet(font="slant")
    # print(f.renderText("Class Diary"))
    print(f"Today's date: {today}")

    name = input("Who's taking the class: ").title()
    lesson = input("What's the lesson: ").title()
    student = Student(name, 1)

    print(f"Starting session with {student.name}, lesson {lesson}")

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
