import json
from dataclasses import dataclass, asdict
import time
from enum import IntEnum
from typing import List

"""
PeriodN (object Value - from Architecture Patterns with Python): 
    - days of the week 
    - time 

1 unit of Period - 1 week
1 unit of Doc - 1 month
1 unit of Habit - 1 Period
"""


class DaysOfWeek(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


@dataclass()
class WeekPeriod:
    days_of_week: List[int]
    time: str

    def to_dict(self):
        return asdict(self)


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


class Document:
    def __init__(self, ):
        pass


class HabitTrackerDocument(Document):
    def __init__(self):
        super().__init__()
        ...


class HabitTrackerTable:
    def __init__(self):
        pass
