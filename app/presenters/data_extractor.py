import calendar
import datetime
from dataclasses import dataclass
from typing import List

from app.domain.habitentity import HabitEntity


@dataclass
class OneDay:
    day_number: int
    weekday_number: int
    weekday_letter: str
    time: str
    month: int


@dataclass
class HabitTrackerHeader:
    name: str
    description: str
    preconditions: List[str]
    place: str


class DataExtractor:
    CURRENT_YEAR = datetime.datetime.today().year

    DocumentDaysOfWeek = dict(zip([1, 2, 3, 4, 5, 6, 7, ],
                                  ['M', 'T', 'W', 'T', 'F', 'S', 'S']))

    def __init__(self, habit_entity: HabitEntity):
        self.habit_ent = habit_entity

        self.days_in_month = self._get_number_of_days_in_months()
        self.planned_month = self._get_table_content()

    def get_header_content(self):
        outside = 'Outside' if self.habit_ent.place.outside else 'Inside'
        return HabitTrackerHeader(
            name=self.habit_ent.data.name,
            description=self.habit_ent.data.description,
            preconditions=', '.join(self.habit_ent.data.preconditions),
            place=f"{self.habit_ent.place.place}, {outside}",
        )

    def _get_table_content(self):
        month_with_planned_habit = {}
        for day in range(1, self.days_in_month + 1):
            weekday_number = datetime.datetime.isoweekday(
                datetime.datetime(self.habit_ent.schedule.year, self.habit_ent.schedule.month, day))
            time = ''
            for week_period in self.habit_ent.schedule.week_periods:
                if weekday_number in week_period.days_of_week:
                    time = week_period.time

            month_with_planned_habit[day] = OneDay(
                day_number=day,
                weekday_number=weekday_number,
                weekday_letter=self.DocumentDaysOfWeek[weekday_number],
                time=time,
                month=self.habit_ent.schedule.month,
            )
        return month_with_planned_habit

    def _get_number_of_days_in_months(self):
        _, days_in_month = calendar.monthrange(self.habit_ent.schedule.year, self.habit_ent.schedule.month)
        return days_in_month
