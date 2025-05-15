import typer
from diary import Diary
from rich import print
from rich.prompt import Prompt, Confirm
from report import create_class_report_pdf


profile_path = "../content/tests/"
#!TODO:
# finish typer tutorial.
# Add colors to summary and update messages.
# try using typer, not rich for Console, Prompt and Confirm
# Uniform library usage: https://typer.tiangolo.com/tutorial/printing/#color
# Decide on color palette logic to avoid overwhelming design decision.
# Read about UX color usage if necessary.


def main(name: str, lesson: str = "Conversation practice"):
    """
    Write the 'name' of the student.
    If --lesson is used, lesson title is added.
    """
    diary = Diary(profile_path)
    diary.get_or_create_profile(name)
    notes = diary.add_notes(lesson)

    while True:
        entry = Prompt.ask(" - :writing_hand: Write something (or 'done'): ").strip()
        if entry.lower() == "done":
            break
        notes.add_entry(entry)
        print(
            f"[green italic]Saved entry at {notes.entries[-1][0].strftime("%H:%M:%S")}"
        )

    note_json_path = diary.close()
    print_report = Confirm.ask("Would you like [bold red]a PDF[/bold red] from this?")
    if print_report:
        pdf_path = create_class_report_pdf(note_json_path, diary.data["student_path"])
        print(f"[green bold]PDF printed at [link={pdf_path}]{pdf_path}[/link]")
    else:
        print(
            f"[italic][magenta]PDF not printed[/magenta] for [blue]{name}'s lesson:[/blue] [dark_orange]{lesson}[/dark_orange]. Thanks!"
        )


if __name__ == "__main__":
    typer.run(main)
