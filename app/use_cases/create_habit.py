import datetime
from typing import List, Tuple, Any

from app.db.repository import HabitRepository
from app.domain.habitentity import HabitEntity, HabitData, HabitLocation, WeekPeriod, HabitSchedule
from app.domain.helpers import DaysOfWeek, DaysOfWeekStr

"""
сюда должны данные приходить уже!!!!!!
и тут мы с ними делаем какие-то действия с привычкой - например, сохраняем в базу
"""


def create_habit(**data):
    print(data)
    habit_data = HabitData(name=data['name'], description=data['description'], preconditions=data['preconditions'])
    habit_place = HabitLocation(place=data['place'], outside=data['outside'])
    hs = HabitSchedule(
        year=data['year'],
        month=data['month'],
        week_periods=[]
    )
    hs.week_periods = _create_week_periods_entities(data['week_periods'])

    habit = HabitEntity(habit_data=habit_data)
    habit.where(habit_place)
    habit.when(hs)

    repo = HabitRepository()
    db_id = repo.entity_to_db(habit)
    print(db_id)


def get_all_habits():
    repo = HabitRepository()
    habit_entities = repo.get_all_habits()
    return habit_entities

def _create_week_periods_entities(periods: List[Tuple]):
    period_entities = []
    for period in periods:

        time = period[1][0].strftime('%H:%M')
        wp = WeekPeriod(time=time, days_of_week=[])
        for day in period[0]:
            wp.days_of_week.append(DaysOfWeek[DaysOfWeekStr[day].value])

        period_entities.append(wp)
    return period_entities
