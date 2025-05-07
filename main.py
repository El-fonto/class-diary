from datetime import date
from pyfiglet import Figlet


class Session:
    def __init__(self) -> None:
        pass


def main():
    today = date.today()
    f = Figlet(font="slant")
    print(f.renderText("==== Diary is running ===="))
    print(f"Today's date: {today}")


if __name__ == "__main__":
    main()
