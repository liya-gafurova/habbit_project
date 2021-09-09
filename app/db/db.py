import uuid as uuid
from peewee import *

db = SqliteDatabase('/home/lia/PycharmProjects/IPR/IPR3/atomic_habbits/habbit_project/app/db/db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Habit(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(column_name='name', null=False, )
    description = TextField(column_name='description', null=False)
    place = TextField(column_name='place', null=True)
    outside = BooleanField('outside', default=False)

    class Meta:
        table_name = 'habit'


class Preconditions(BaseModel):
    habit = ForeignKeyField(Habit, related_name='preconditions')
    precondition = TextField(column_name='precondition', null=False)

    class Meta:
        table_name = 'preconditions'


class WeekPeriods(BaseModel):
    habit = ForeignKeyField(Habit, related_name='days')
    day = IntegerField(column_name='day', null=False)
    time = TextField(column_name='time', null=True)
    month = IntegerField(column_name='month', null = False)
    year = IntegerField(column_name='year', null=False)

    class Meta:
        table_name = 'WeekPeriods'


def create_tables():
    with db:
        db.create_tables([Habit, Preconditions, WeekPeriods])


create_tables()