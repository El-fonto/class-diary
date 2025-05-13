import json
from fpdf import FPDF


class PDF(FPDF):
    def note_title(self, lesson_number: int, name: str):
        self.set_font("Times", "B", 16)
        self.set_fill_color(200, 220, 255)  # light blue
        self.cell(
            w=0,
            h=6,
            text="Lesson %d: %s" % (lesson_number, name),
            border=False,
            ln=1,
            align="C",
        )
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

    # title
    pdf.note_title(data.get("lesson_count"), data.get("student_name"))

    pdf.output(pdf_path)
