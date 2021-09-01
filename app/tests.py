import datetime

from app.db.repository import HabitRepository
from app.domain.habitentity import HabitEntity, HabitData, HabitPlace, HabitSchedule, WeekPeriod
from app.domain.helpers import DaysOfWeek, Months


def test_habit_creation():
    habit_name = HabitData(
        name='Walking',
        description='Walking or Other outside  everyday activity',
        preconditions=[
            'After work during Mn-Fr',
        ]
    )
    habit_place = HabitPlace(
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

    repo = HabitRepository()
    habit_obj_id = repo.entity_to_db(habit)
    habit_entity = repo.entity_from_db(habit_obj_id)

    assert habit.__str__() == '{"name": "Walking", "description": "Walking or Other outside  everyday activity", "place": "In the park / On the embankment"}'
    assert habit.data.name == habit_entity.data.name

test_habit_creation()