import json
import os
from fpdf import FPDF


class PDF(FPDF):
    def note_title(self, date, lesson_number, lesson_title, name):
        title = f"Lesson #{lesson_number} - {lesson_title}"
        title2 = f"{date} - {name}"

        self.set_font("Times", "B", 14)
        self.set_fill_color(200, 220, 255)  # light blue
        self.cell(0, 6, title2, False, 1, "C")
        self.cell(0, 6, title, False, 1, "C")
        self.ln(6)

    def note_body(self, note_entries):
        self.set_font("Arial", "", 12)
        self.ln(2)
        self.multi_cell(0, 6, note_entries, "J")
        self.ln(4)


def load_json_data(filepath) -> dict | None:
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'.")
        return None


def create_class_report_pdf(json_path: str, pdf_path: str):
    pdf = PDF(format="Letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    data = load_json_data(json_path)
    lesson_count = data.get("lesson_count")
    student_name = data.get("student_name")
    session_date = data.get("session_date")
    iso_date = data.get("iso_date")
    lesson_title = data.get("lesson_title")
    entries: list = data.get("entries")

    note_body = "\n".join(entries)

    pdf.note_title(session_date, lesson_count, lesson_title, student_name)
    pdf.note_body(note_body)

    report_name = f"{iso_date}_{lesson_title}_{student_name}_{lesson_count}.pdf"
    report_path = os.path.join(pdf_path, report_name)

    pdf.output(report_path, "F")
    return report_path
