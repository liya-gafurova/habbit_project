"""
Привычка:
 - Что?  name, description, preconditions --???
 - Где? place
 - Когда? week_periods, month, year=None
"""
import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class HabitData:
    # What?
    name: str
    description: str
    preconditions: List[str]


@dataclass
class HabitPlace:
    # Where?
    place: str


@dataclass
class WeekPeriod:
    days_of_week: List[int]
    time: str

    def to_dict(self):
        return asdict(self)


@dataclass
class HabitSchedule:
    # When?
    week_periods: List[WeekPeriod]
    month: int
    year: int


class Habit:

    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description
        self.preconditions = list()
        self.place = None

        self.periods: List[WeekPeriod] = list()

    def set_period(self, week_period: WeekPeriod):
        # определить набор периодов, когда я буду реализовывать привычку для одной недели
        # этот набор периодов будет повторяться каждую неделю
        self.periods.append(week_period)

    def set_place(self, place: str):
        self.place = place

    def set_precondition(self, precondition: str):
        # text description about what should be before habit
        self.preconditions.append(precondition)

    def __str__(self):
        return self.__representation_pattern()

    def __representation_pattern(self):
        pattern = {
            'name': self.name,
            'description': self.description,
            'place': self.place,
            'preconditions': self.preconditions,
            'periods': [p.to_dict() for p in self.periods]
        }
        return json.dumps(pattern)


"""
документ должен принимать только то, что связано с документом 
то есть количество строк, столбцов, обьединение ячеек, название таблиц, подписиб заголовки...
Документ не должен знать ничего про то, что такое  Привычка, 
он должен уметь создавать документы для любого типа сущности
"""


class TransformHabitToDocumentParameters:
    def __init__(self):
        pass


class DocxDocument:
    def __init__(self, ):
        pass


class HabitTrackerDocxDocument(DocxDocument):
    def __init__(self):
        super().__init__()
        ...


class HabitTrackerTable:
    def __init__(self):
        pass
