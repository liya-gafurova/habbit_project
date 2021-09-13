import datetime
from typing import List, Tuple, Any

from app.db.repository import HabitRepository
from app.domain.habitentity import HabitEntity, HabitData, HabitLocation, WeekPeriod, HabitSchedule
from app.domain.helpers import DaysOfWeek, DaysOfWeekStr
from app.presenters.docx_document import HabitDocument


FILES_PATH = '/home/lia/PycharmProjects/IPR/IPR3/atomic_habbits/habbit_project/files/'

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
    return db_id


def get_all_habits():
    repo = HabitRepository()
    habit_entities = repo.get_all_habits()
    return habit_entities


def get_habit_printed_flag(habit_ent):
    repo = HabitRepository()
    return repo.is_already_printed(habit_ent)


def create_document(habit_ent):
    # create document
    doc = HabitDocument(habit_ent)
    doc_name = FILES_PATH + f'{habit_ent.data.name}{datetime.datetime.now()}.docx'
    doc.create_document(doc_name)

    # update Printed Event
    repo = HabitRepository()
    repo.update_printed(habit_ent)

    return doc_name


def _create_week_periods_entities(periods: List[Tuple]):
    period_entities = []
    for period in periods:

        time = period[1][0].strftime('%H:%M')
        wp = WeekPeriod(time=time, days_of_week=[])
        for day in period[0]:
            wp.days_of_week.append(DaysOfWeek[DaysOfWeekStr[day].value])

        period_entities.append(wp)
    return period_entities
