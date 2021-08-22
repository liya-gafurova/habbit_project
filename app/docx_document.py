import datetime
import calendar
import math

from docx import Document
from docx.shared import Inches
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_ALIGN_PARAGRAPH

from app.habit import Habit, Months


def test_create_document():
    document = Document()

    document.add_heading('Document Title', 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='List Number'
    )

    document.add_picture('./q101.jpg', width=Inches(1.25))

    records = (
        (3, '101', 'Spam'),
        (7, '422', 'Eggs'),
        (4, '631', 'Spam, spam, eggs, and spam')
    )

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    for qty, id, desc in records:
        row_cells = table.add_row().cells
        row_cells[0].text = str(qty)
        row_cells[1].text = id
        row_cells[2].text = desc

    document.add_page_break()

    document.save('demo.docx')


class HabitDocument:
    CURRENT_YEAR = datetime.datetime.today().year

    def __init__(self, name, description, preconditions, place, week_periods, month, year=None):
        self.name_of_habit = name
        self.habit_description = description
        self.preconditions = preconditions
        self.place = place
        self.week_periods = week_periods
        self.month = month
        self.year = year if year else self.CURRENT_YEAR

        self.document: Document = Document()

    def create_document(self, document_name):
        self._create_document_heading()
        self.document.save(document_name)

    def _create_document_heading(self):
        # landscape orientation
        section = self.document.sections[0]
        new_width, new_height = section.page_height, section.page_width
        section.orientation = WD_ORIENTATION.LANDSCAPE
        section.page_width = new_width
        section.page_height = new_height

        # Heading - name of Habit
        heading = self.document.add_heading(self.name_of_habit)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        line = self.document.add_paragraph('Description: ')
        line.add_run(self.habit_description).bold = True

        line = self.document.add_paragraph('Preconditions: ')
        for precondition in self.preconditions:
            line.add_run(precondition).bold = True
            line.add_run(', ').bold = True

        line = self.document.add_paragraph('Place: ')
        line.add_run(self.place).bold = True

        # TODO check table !!!
        empty_table = EmptyHabitTable(self.month, self.year, self.document)
        empty_table.draw_table_on_document()




class EmptyHabitTable:
    NUMBER_OF_DAYS_IN_ROW = 7 # week in row

    def __init__(self, month: int, year: int, document: HabitDocument):
        self.month = month
        self.year = year
        self.habit_document = document

    @property
    def number_of_days_in_month(self):
        return calendar.monthrange(self.year, self.month)

    @property
    def number_of_rows(self):
        return math.ceil(self.number_of_days_in_month / self.NUMBER_OF_DAYS_IN_ROW)

    def draw_table_on_document(self):
        self.habit_document.add_table(rows=self.number_of_rows,
                                              cols=self.NUMBER_OF_DAYS_IN_ROW)




my_habit = Habit(name='Reading',
                 description='Habit of reading 10 pages of professional literature every day')
my_habit.set_precondition('After work')
my_habit.set_place('At work table')

doc = HabitDocument(
    name=my_habit.name,
    description=my_habit.description,
    preconditions=my_habit.preconditions,
    place=my_habit.place
)
doc.create_document(f'../files/first_habit_doc_{datetime.datetime.now()}.docx')
