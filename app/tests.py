import datetime

from app.domain.habit import Habit, HabitData, HabitPlace, HabitSchedule, WeekPeriod
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

    habit = Habit(habit_name)
    habit.where(habit_place)
    habit.when(schedule)

    assert habit.__str__() == '{"name": "Walking", "description": "Walking or Other outside  everyday activity", "place": "In the park / On the embankment"}'
