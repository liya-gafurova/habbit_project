import datetime

from app.db.repository import HabitRepository
from app.domain.habitentity import HabitEntity


"""
сюда должны данные приходить уже!!!!!!
и тут мы с ними делаем какие-то действия с привычкой - например, сохраняем в базу
"""

# все, что должно быть в юзкейсе, ниже
# можно еще добавить сохранение в базу
# def create_habit(habit_name,habit_place, schedule):
#     habit = HabitEntity(habit_name)
#     habit.where(habit_place)
#     habit.when(schedule)
#
#     repo = HabitRepository(habit)
#     obj_id = repo.entity_to_db()
#     print(habit)
#     print(obj_id)

def create_habit(**data):
    print(data)
