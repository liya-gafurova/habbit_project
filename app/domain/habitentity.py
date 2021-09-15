"""
Привычка:
 - Что?  name, description, preconditions --???
 - Где? place
 - Когда? week_periods, month, year=None
"""
import json
from dataclasses import dataclass, asdict
from typing import List

import uuid


@dataclass
class HabitData:
    # What?
    name: str
    description: str
    preconditions: List[str]


@dataclass
class HabitLocation:
    # Where?
    place: str
    outside: bool


@dataclass
class WeekPeriod:
    days_of_week: List[int]
    time: str


@dataclass
class HabitSchedule:
    # When?
    week_periods: List[WeekPeriod]
    month: int
    year: int


class HabitEntity:

    def __init__(self, habit_data: HabitData):
        self.uuid = None
        self.data = habit_data
        self.place: HabitLocation = None
        self.schedule: HabitSchedule = None

        self._set_uuid()

    def when(self, habit_schedule: HabitSchedule):
        # определить набор периодов, когда я буду реализовывать привычку для одной недели
        # этот набор периодов будет повторяться каждую неделю
        self.schedule = habit_schedule

    def where(self, habit_place: HabitLocation):
        self.place = habit_place

    def _set_uuid(self):
        self.uuid = uuid.uuid4()

    def __str__(self):
        return self.__representation_pattern()

    def __representation_pattern(self):
        pattern = {
            'name': self.data.name,
            'description': self.data.description,
            'place': self.place.place
        }
        return json.dumps(pattern)
