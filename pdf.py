from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import date
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class PDFCreator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.c = canvas.Canvas(self.file_name, pagesize=letter)
        self.value_font = "Helvetica"
        self.value_font_size = 12
        self.title_font = "Helvetica-Bold"
        self.title_font_size = 28
        self.y_position = 750

    def write_text(self, text, font, font_size, x, y):
        self.c.setFont(font, font_size)
        self.c.drawString(x, y, text)

    def write_info(self, info_text, offset=0):
        self.y_position -= 30 + offset
        self.write_text(info_text, self.value_font, self.value_font_size, 50, self.y_position)

    def draw_table(self, rows, columns, values, column_headers):
        modified_values = [[''] + column_headers] + [[i + 1] + values[i * columns:(i + 1) * columns] for i in range(rows)]

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('SIZE', (0, 0), (-1, -1), 12),
            ('LEADING', (0, 0), (-1, -1), 14),
        ])

        table = Table(modified_values)
        table.setStyle(table_style)

        table_width, table_height = table.wrapOn(self.c, 0, 0)

        table_y_position = self.y_position - table_height - 120 - ((750 - self.y_position) - table_height) / 2

        table.drawOn(self.c, x=(letter[0] - table_width) / 2, y=table_y_position)

    def save_pdf(self):
        self.c.save()

    def count_values(self, value):
        values = value.split(',')
        return len(values)

    def write_title(self, title_text):
        title_width = self.c.stringWidth(title_text, self.title_font, self.title_font_size)
        title_x = (letter[0] - title_width) / 2
        self.write_text(title_text, self.title_font, self.title_font_size, title_x, self.y_position - 30)

def create_pdf():
    file_name = "spechtlab_pdf.pdf"
    pdf_generator = PDFCreator(file_name)

    today = date.today().strftime("%d-%m-%Y")

    user_object = input("Please enter the measured object: ")
    user_value = input("Please enter the measured value (write, separated by commas): ")

    value_count = pdf_generator.count_values(user_value)

    while True:
        try:
            measurement_count = int(input("Enter the number of measurements to be taken: "))
            break
        except ValueError:
            print("Please enter a valid numeric value.")

    values_to_add = []
    for i in range(measurement_count):
        for j in range(value_count):
            value = input(f"Enter value for {user_value.split(',')[j]} in measurement {i + 1}: ")
            values_to_add.append(value)

    user_value_columns = user_value.split(',')

    pdf_generator.write_title("SPECHTLAB")
    pdf_generator.write_info(f"Report Date: {today}", offset=40)
    pdf_generator.write_info(f"Measured Object: {user_object}", offset=10)
    pdf_generator.write_info(f"Measured Value: {', '.join(user_value_columns)}", offset=10)
    pdf_generator.write_info(f"Number of Measurements: {measurement_count}", offset=10)

    pdf_generator.draw_table(rows=measurement_count, columns=value_count, values=values_to_add, column_headers=user_value_columns)

    pdf_generator.save_pdf()

if __name__ == "__main__":
    create_pdf()
