from typing import List

import uuid
from peewee import fn

from app.db.db import Habit, Preconditions, WeekPeriods, PrintingEvents
from app.domain.habitentity import HabitEntity, HabitData, HabitSchedule, WeekPeriod, HabitLocation


class HabitRepository:

    def entity_to_db(self, habit: HabitEntity):
        new_habit_obj = Habit(
            uuid=uuid.uuid4().hex,
            name=habit.data.name,
            description=habit.data.description,
            place=habit.place.place,
            outside=habit.place.outside
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

        return new_habit_obj.uuid

    def entity_from_db(self, uuid):
        habit_obj: Habit = Habit.get(Habit.uuid==uuid)
        habit_entity = self._get_habit_info(habit_obj)

        return habit_entity

    def get_all_habits(self) -> List[HabitEntity]:
        all_habits_objs = Habit.select()
        habit_entities = []
        for habit_obj in all_habits_objs:
            habit_entities.append(self._get_habit_info(habit_obj))
        return habit_entities

    def is_already_printed(self, habit_ent):
        habit = Habit.select().where(Habit.name == habit_ent.data.name,
                                     Habit.description == habit_ent.data.description,
                                     Habit.place == habit_ent.place.place
                                     )
        times_printed = PrintingEvents.select().where(PrintingEvents.habit == habit).count()
        return times_printed > 0

    def update_printed(self, habit_ent):
        habit = Habit.select().where(Habit.name == habit_ent.data.name,
                                     Habit.description == habit_ent.data.description,
                                     Habit.place == habit_ent.place.place
                                     )
        event = PrintingEvents(habit=habit)
        event.save()

    def _get_habit_info(self, habit_obj):
        preconditions = Preconditions.select().where(Preconditions.habit == habit_obj)

        habit_entity = HabitEntity(habit_data=HabitData(
            name=habit_obj.name,
            description=habit_obj.description,
            preconditions=[obj.precondition for obj in preconditions]
        ))

        habit_entity.place = HabitLocation(place=habit_obj.place,
                                           outside=habit_obj.outside)

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
