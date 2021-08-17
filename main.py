from habit import Habit, WeekPeriod, DaysOfWeek


my_habit = Habit(name='Reading',
                 description='Habit of reading 10 pages of professional literature every day')
my_habit.set_precondition('After work')
my_habit.set_place('At work table')

my_habit.set_period(
    WeekPeriod(days_of_week=[DaysOfWeek.MONDAY,
                             DaysOfWeek.TUESDAY,
                             DaysOfWeek.WEDNESDAY,
                             DaysOfWeek.THURSDAY,
                             DaysOfWeek.FRIDAY],
               time = '21:00')
)
my_habit.set_period(
    WeekPeriod(days_of_week=[DaysOfWeek.SATURDAY,
                             DaysOfWeek.SUNDAY],
               time = '11:00')
)

print(my_habit)
