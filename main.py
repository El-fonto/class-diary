from datetime import date
import datetime
from pyfiglet import Figlet


class Student:
    def __init__(
        self,
        name: str | None,
        lesson_count: int | None,
    ) -> None:
        self.name = name
        self.lesson_count = lesson_count


def main():
    today = date.today()
    # f = Figlet(font="slant")
    # print(f.renderText("Class Diary"))
    print(f"Today's date: {today}")

    data = []
    time_log = []
    student = input("Who's taking the class: ").title()
    data.append(student)

    def log_input():
        time_log.append(datetime.datetime.now().strftime("%H:%M:%S"))
        return input("=====> data: (or 'done'): ")

    while True:
        entry = log_input().strip()
        if entry.strip() == "done":
            break
        data.append(entry.strip())

    print(f"Today's date: {today}")
    print(f"Student: {data[0]}")

    for i in range(1, len(data)):
        print(f"🕑️{time_log[i]} #{i}: {data[i]}")


if __name__ == "__main__":
    main()
