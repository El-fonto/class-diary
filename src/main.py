from diary import Diary
# from report import create_class_report_pdf


profile_path = "./content/profiles/"
#!TODO:
# Next up, would be getting the Calendar working


def main():
    diary = Diary(profile_path)

    name = input("Who's taking the class: ").strip().title()
    lesson = input("Which lesson: ").title()

    diary.get_or_create_profile(name)
    notes = diary.add_notes(lesson)

    while True:
        entry = input("=====> jot down (or 'done'): ").strip()
        if entry.lower() == "done":
            break
        notes.add_entry(entry)
        print(f"Saved entry at {notes.entries[-1][0].strftime("%H:%M:%S")}")

    diary.close()
    # create_class_report_pdf(diary.data["student_profile"], diary.data["student_path"])


if __name__ == "__main__":
    main()
