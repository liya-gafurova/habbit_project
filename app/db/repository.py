from peewee import fn

from app.db.db import Habit, Preconditions, WeekPeriods
from app.domain.habitentity import HabitEntity, HabitData, HabitSchedule, WeekPeriod


class HabitRepository:

    def entity_to_db(self, habit: HabitEntity):
        new_habit_obj = Habit(
            name=habit.data.name,
            description=habit.data.description,
            place=habit.place
        )
        new_habit_obj.save()

        for precondition in habit.data.preconditions:
            Preconditions.create(
                habit=new_habit_obj,
                precondition=precondition
            )

        month = habit.schedule.month
        year = habit.schedule.year
        for week_period in habit.schedule.week_periods:
            for day in week_period.days_of_week:
                WeekPeriods.create(
                    habit=new_habit_obj,
                    day=day,
                    time=week_period.time,
                    month=month,
                    year=year
                )

        return new_habit_obj.id

    def entity_from_db(self, id):
        habit_obj: Habit = Habit.get_by_id(id)
        preconditions = Preconditions.select().where(Preconditions.habit == habit_obj)

        habit_entity = HabitEntity(habit_data=HabitData(
            name=habit_obj.name,
            description=habit_obj.description,
            preconditions=[obj.precondition for obj in preconditions]
        ))

        habit_entity.place = habit_obj.place

        # manage days
        convert_days = lambda s: [int(i) for i in (s or '').split(',') if i]
        one_period_days = (fn
                           .GROUP_CONCAT(WeekPeriods.day)
                           .python_value(convert_days))

        query = (WeekPeriods
                 .select(WeekPeriods.time, one_period_days.alias('days'), WeekPeriods.month, WeekPeriods.year)
                 .where(WeekPeriods.habit == habit_obj)
                 .group_by(WeekPeriods.time))

        periods = []
        month = ''
        year = ''
        for period in query:
            print(period.days, period.time)
            periods.append(
                WeekPeriod(
                    days_of_week=period.days,
                    time=period.time
                )
            )
            month, year = period.month, period.year

        habit_entity.when(
            habit_schedule=HabitSchedule(week_periods=periods, month=month, year=year))

        return habit_entity
