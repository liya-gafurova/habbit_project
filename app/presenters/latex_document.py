import datetime
import math

import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command, Table, Tabu, NewLine, LineBreak
from pylatex.base_classes import LatexObject
from pylatex.utils import italic, bold
import os

from app.domain.habitentity import HabitEntity, HabitData, HabitLocation, HabitSchedule, WeekPeriod
from app.domain.helpers import DaysOfWeek, Months
from app.presenters.data_extractor import DataExtractor, OneDay
from app.settings import FILES_PATH


class LatexDocument:
    NUMBER_OF_DAYS_IN_ROW = 7  # week in row
    geometry_options = {
        "landscape": True,
    }

    def __init__(self, habit_entity: HabitEntity):
        self.data_extractor = DataExtractor(habit_entity)
        self.doc = Document(page_numbers=True, geometry_options=self.geometry_options)

    def create_document(self, document_path=f'{FILES_PATH}latex_{datetime.datetime.now()}'):
        self._create_header()
        self._create_table()
        self.doc.generate_pdf(document_path, clean_tex=False)

    def _create_header(self):
        header_content = self.data_extractor.get_header_content()
        with self.doc.create(Section(header_content.name)):
            self.doc.append('Habit description: ')
            self.doc.append(bold(header_content.description))

            self.doc.append('\nHabit preconditions: ')
            self.doc.append(bold(header_content.preconditions))

            self.doc.append('\nHabit place: ')
            self.doc.append(bold(header_content.place))

    def _create_table(self):
        rows, cols = self._calculate_table_size(self.data_extractor.days_in_month)

        with self.doc.create(Section('Habit Tracker')):
            day_counter = 1
            with self.doc.create(Tabu("|c|" + "c|" * (cols - 1))) as table:
                table.add_hline()
                day_counter = 1
                for row in range(rows):
                    self._fill_row(table,  day_counter)
                    day_counter += cols

    def _fill_row(self, table,  day_counter):
        row = []

        for wd in range(day_counter, day_counter+self.NUMBER_OF_DAYS_IN_ROW):
            if day_counter <= self.data_extractor.days_in_month:
                one_day = self.data_extractor.planned_month[day_counter]
                cell_header = self.add_cell_header(one_day)
                time_line = self.add_cell_time_paragraph(one_day)
                row.append(f'{cell_header}  {time_line}')

            else:
                row.append('')
            day_counter += 1

        table.add_row(row, escape=True)
        table.add_hline()

    def add_cell_header(self, day):
        space_fillers = self._calculate_number_of_spaces(day.day_number)
        zero_month_filler = 0 if day.month < 10 else ''  # data extractors
        cell_header =f"{day.day_number}/{zero_month_filler}{day.month}{space_fillers}{day.weekday_letter}"
        # make  grey text

        return cell_header

    def add_cell_time_paragraph(self,  day: OneDay):
        habit_time_line = " " * 6 + f'{day.time}\n'
        # habit_time_line.font.bold = True
        return  habit_time_line


    def _calculate_number_of_spaces(self, day_of_month):
        return ' ' * 9 if day_of_month > 9 else ' ' * 11

    def _calculate_table_size(self, days_in_month):
        rows = math.ceil(days_in_month / self.NUMBER_OF_DAYS_IN_ROW)
        columns = self.NUMBER_OF_DAYS_IN_ROW
        return rows, columns


if __name__ == '__main__':
    habit_name = HabitData(
        name='Walking',
        description='Walking or Other outside  everyday activity',
        preconditions=[
            'After work during Mn-Fr',
        ]
    )
    habit_place = HabitLocation(
        place='In the park / On the embankment',
        outside=True
    )

    schedule = HabitSchedule(
        week_periods=[
            WeekPeriod(
                days_of_week=[DaysOfWeek.MONDAY, DaysOfWeek.TUESDAY, DaysOfWeek.WEDNESDAY, \
                              DaysOfWeek.THURSDAY, DaysOfWeek.FRIDAY],
                time="18:00"),
            WeekPeriod(
                days_of_week=[DaysOfWeek.SUNDAY, DaysOfWeek.SATURDAY],
                time="12:00 - 21:00"),

        ],
        month=Months.SEPTEMBER,
        year=datetime.datetime.today().year
    )

    habit = HabitEntity(habit_name)
    habit.where(habit_place)
    habit.when(schedule)

    doc_latex = LatexDocument(habit)
    doc_latex.create_document()