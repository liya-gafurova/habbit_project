import datetime
import calendar
import math
from dataclasses import dataclass

from docx import Document
from docx.shared import Inches, RGBColor
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_ALIGN_PARAGRAPH

from app.domain.habitentity import HabitEntity


@dataclass
class OneDay:
    day_number: int
    weekday_number: int
    weekday_letter: str
    time: str


class HabitDocument:
    CURRENT_YEAR = datetime.datetime.today().year
    NUMBER_OF_DAYS_IN_ROW = 7  # week in row
    DocumentDaysOfWeek = dict(zip([1, 2, 3, 4, 5, 6, 7, ],
                                  ['M', 'T', 'W', 'T', 'F', 'S', 'S']))

    def __init__(self, habit: HabitEntity):
        self.habit: HabitEntity = habit

        self.document: Document = Document()
        self.days_in_month = self.get_number_of_days_in_months()
        self.planned_month = self.get_planned_month()

    def create_document(self, document_name):
        self.make_landscape_orientation()
        self.make_description_info()
        self.make_table()
        self.document.save(document_name)

    def make_landscape_orientation(self):
        # landscape orientation
        section = self.document.sections[0]
        new_width, new_height = section.page_height, section.page_width
        section.orientation = WD_ORIENTATION.LANDSCAPE
        section.page_width = new_width
        section.page_height = new_height

    def make_description_info(self):
        self.add_heading()
        self.add_description_paragraph()
        self.add_preconditions_paragraph()
        self.add_place_paragraph()

    def add_heading(self):
        # Heading - name of Habit
        heading = self.document.add_heading(self.habit.data.name)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def add_description_paragraph(self):
        line = self.document.add_paragraph('Description: ')
        line.add_run(self.habit.data.description).bold = True

    def add_preconditions_paragraph(self):
        line = self.document.add_paragraph('Preconditions: ')
        for precondition in self.habit.data.preconditions:
            line.add_run(precondition).bold = True
            line.add_run(', ').bold = True

    def add_place_paragraph(self):
        line = self.document.add_paragraph('Place: ')
        line.add_run(self.habit.place.place).bold = True

    def make_table(self):
        table = self.add_empty_table()
        self.fill_table(table)

    def add_empty_table(self):
        rows, columns = self._calculate_table_size()
        return self.document.add_table(rows=rows, cols=columns)

    def fill_table(self, table):
        day_counter = 1
        for row in table.rows:
            for cell in row.cells:
                one_day = self.planned_month[day_counter]
                self.add_cell_header(cell, one_day)
                self.add_cell_time_paragraph(cell, one_day)

                if day_counter == self.days_in_month:
                    break
                day_counter += 1

    def add_cell_header(self, cell, day: OneDay):
        space_fillers = self._calculate_number_of_spaces(day.day_number)
        zero_month_filler = 0 if self.habit.schedule.month < 10 else ''
        cell_header = cell.paragraphs[0].add_run(
            f"{day.day_number}/{zero_month_filler}{self.habit.schedule.month}{space_fillers}{day.weekday_letter}")
        cell_header.font.color.rgb = RGBColor(120, 120, 120)

    def add_cell_time_paragraph(self, cell, day: OneDay):
        habit_time_line = cell.add_paragraph().add_run(" " * 6 + f'{day.time}\n')
        habit_time_line.font.bold = True

    def get_number_of_days_in_months(self):
        _, days_in_month = calendar.monthrange(self.habit.schedule.year, self.habit.schedule.month)
        return days_in_month

    def get_planned_month(self):
        month_with_planned_habit = {}
        for day in range(1, self.days_in_month + 1):
            weekday_number = datetime.datetime.isoweekday(
                datetime.datetime(self.habit.schedule.year, self.habit.schedule.month, day))
            time = ''
            for week_period in self.habit.schedule.week_periods:
                if weekday_number in week_period.days_of_week:
                    time = week_period.time

            month_with_planned_habit[day] = OneDay(
                day_number=day,
                weekday_number=weekday_number,
                weekday_letter=self.DocumentDaysOfWeek[weekday_number],
                time=time
            )
        return month_with_planned_habit

    def _calculate_table_size(self):
        rows = math.ceil(self.days_in_month / self.NUMBER_OF_DAYS_IN_ROW)
        columns = self.NUMBER_OF_DAYS_IN_ROW
        return rows, columns

    def _calculate_number_of_spaces(self, day_of_month):
        return ' ' * 9 if day_of_month > 9 else ' ' * 11
