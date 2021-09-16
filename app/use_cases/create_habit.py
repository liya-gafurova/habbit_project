import datetime
from typing import List, Tuple

from app.db.repository import HabitRepository
from app.domain.habitentity import HabitEntity, HabitData, HabitLocation, WeekPeriod, HabitSchedule
from app.domain.helpers import DaysOfWeek, DaysOfWeekStr
from app.presenters.docx_document import DocxDocument
from app.presenters.latex_document import LatexDocument
from app.settings import FILES_PATH, FILES_EXTENSIONS


def create_habit(**data):
    # TODO added habit entity uuid
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
    uuid = repo.entity_to_db(habit)
    return uuid


def get_all_habits():
    repo = HabitRepository()
    habit_entities = repo.get_all_habits()
    return habit_entities


def create_habit_tracker_document(habit_ent, doc_type):
    doc_creators = {
        'DOCX': DocxDocument,
        'PDF': LatexDocument,
    }

    file_extensions = {
        FILES_EXTENSIONS[0]: str.lower(f'.{FILES_EXTENSIONS[0]}'),
        FILES_EXTENSIONS[1]: str.lower(f'.{FILES_EXTENSIONS[1]}'),
    }

    doc_creator = doc_creators[doc_type](habit_ent)
    doc_name = FILES_PATH + f'{habit_ent.data.name}{datetime.datetime.now()}{file_extensions[doc_type]}'
    doc_creator.create_document(doc_name)

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
