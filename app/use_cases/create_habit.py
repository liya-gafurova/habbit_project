import datetime

from app.domain.habit import HabitData, HabitPlace, HabitSchedule, WeekPeriod, Habit
from app.domain.helpers import DaysOfWeek, Months

"""
сюда должны данные приходить уже!!!!!!
и тут мы с ними делаем какие-то действия с привычкой - например, сохраняем в базу
"""
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

# все, что должно быть в юзкейсе, ниже
# можно еще добавить сохранение в базу
habit = Habit(habit_name)
habit.set_place(habit_place)
habit.set_period(schedule)
print(habit)
