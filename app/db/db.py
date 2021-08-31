from peewee import *

connection = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = connection


class Habit(BaseModel):
    id = AutoField(column_name='id')
    name = TextField(column_name='Name', null=False, )
    description = TextField(column_name='Description', null=False)
    place = TextField(column_name='Place', null=True)

    class Meta:
        table_name = 'Habit'


class Preconditions(BaseModel):
    habit = ForeignKeyField(Habit)
    pass

    class Meta:
        table_name = 'Preconditions'


class WeekPeriods(BaseModel):
    habit = ForeignKeyField(Habit)
    day = IntegerField(column_name='Day', null=False)
    time = TextField(column_name='Time', null=True)
    pass

    class Meta:
        table_name = 'WeekPeriods'
