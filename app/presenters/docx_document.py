import datetime
import calendar
import math

from docx import Document
from docx.shared import Inches, RGBColor
from docx.enum.section import WD_ORIENTATION
from docx.enum.text import WD_ALIGN_PARAGRAPH

from app.domain.habit import WeekPeriod, Habit
from app.domain.helpers import DaysOfWeek, Months






class HabitDocument:
    CURRENT_YEAR = datetime.datetime.today().year
    NUMBER_OF_DAYS_IN_ROW = 7  # week in row
    DocumentDaysOfWeek = dict(zip([1, 2, 3, 4, 5, 6, 7, ],
                                  ['M', 'T', 'W', 'T', 'F', 'S', 'S']))

    def __init__(self, habit: Habit):
        # self.name_of_habit = name
        # self.habit_description = description
        # self.preconditions = preconditions
        # self.place = place
        # self.week_periods: WeekPeriod = week_periods
        # self.month = month
        # self.year = year if year else self.CURRENT_YEAR
        self.habit: Habit = habit

        self.document: Document = Document()
        self._days_in_month = self._get_number_of_days_in_months()

    def _get_number_of_days_in_months(self):
        _, days_in_month = calendar.monthrange(self.habit.schedule.year, self.habit.schedule.month)
        return days_in_month
# WIP
    @property
    def days_of_week_over_month_distribution(self):

        days_of_week_over_month_distribution = {}
        for day in range(1, self._days_in_month + 1):
            week_day_number = datetime.datetime.isoweekday(datetime.datetime(self.year, self.month, day))
            time = ''
            for week_period in self.week_periods:
                if week_day_number in week_period.days_of_week:
                    time = week_period.time
            days_of_week_over_month_distribution[day] = (week_day_number, time)

        return days_of_week_over_month_distribution

    def create_document(self, document_name):
        self._create_document_heading()
        self._create_table()
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

    def _create_table(self):
        rows, columns = self._calculate_table_size()
        table = self.document.add_table(rows=rows, cols=columns)
        day_counter = 1
        zero_month_filler = 0 if self.month < 10 else ''

        for row in table.rows:
            for cell in row.cells:
                space_fillers = ' ' * 9 if day_counter > 9 else ' ' * 11
                day_of_week = DocumentDaysOfWeek[self.days_of_week_over_month_distribution[day_counter][0]]
                time = self.days_of_week_over_month_distribution[day_counter][1]

                cell_header = cell.paragraphs[0].add_run(
                    f"{day_counter}/{zero_month_filler}{self.month}{space_fillers}{day_of_week}")
                cell_header.font.color.rgb = RGBColor(120, 120, 120)

                habit_time_line = cell.add_paragraph().add_run(" " * 6 + f'{time}\n')
                habit_time_line.font.bold = True

                if day_counter == self._days_in_month:
                    break
                day_counter += 1

    def _calculate_table_size(self):

        rows = math.ceil(self._days_in_month / self.NUMBER_OF_DAYS_IN_ROW)
        columns = self.NUMBER_OF_DAYS_IN_ROW

        return rows, columns


doc.create_document(f'../files/first_habit_doc_{datetime.datetime.now()}.docx')