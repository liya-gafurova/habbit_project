import datetime

from app.domain.habit import HabitData, HabitPlace, HabitSchedule, WeekPeriod, Habit
from app.domain.helpers import DaysOfWeek, Months

"""
сюда должны данные приходить уже!!!!!!
и тут мы с ними делаем какие-то действия с привычкой - например, сохраняем в базу
"""

# все, что должно быть в юзкейсе, ниже
# можно еще добавить сохранение в базу
def create_habit(habit_name,habit_place, schedule):
    habit = Habit(habit_name)
    habit.where(habit_place)
    habit.when(schedule)
    print(habit)
