from datetime import time, timedelta, datetime

import streamlit as st

from app.domain.helpers import MonthsReverse, MonthsCycle, Months
from app.use_cases.create_habit import create_habit

st.title('Create Your Habit Tracker')

if 'WEEK' not in st.session_state:
    st.session_state.WEEK = []
if 'TIME' not in st.session_state:
    st.session_state.TIME = []


def get_next_n_months_for_current(current: int, n: int):
    months_numbers = [current, ]
    while True:
        if next(MonthsCycle) == current:
            break
    for i in range(n):
        months_numbers.append(
            next(MonthsCycle)
        )
    return months_numbers


with st.form('Habit Parameters'):
    # TODO Add month andd year
    name = st.text_input('Name')
    description = st.text_input('Description')
    place = st.text_input('Place')
    outside = st.checkbox(label='Outside')

    st.write('Preconditions')
    preconditions = st.text_input(
        'Please, enter your preconditions. If you have more. than 1, then separate them with ";"')

    year = st.selectbox(
        label='Year',
        options=[datetime.today().year, datetime.today().year + 1],
    )

    month_name = st.selectbox(
        label='Month',
        options=[name for n, name in MonthsReverse.items() if
                 n in get_next_n_months_for_current(current=datetime.today().month, n=2)]

    )
    number_of_week_periods = st.number_input('Number of Week Periods', max_value=10, step=1)
    n = 1
    if not number_of_week_periods:
        st.warning('Please input a number of Periods.')
        submitted = st.form_submit_button(label='Define')
        if submitted:
            n = int(number_of_week_periods)

        st.stop()



    else:

        for i in range(int(number_of_week_periods)):
            vals = st.multiselect(

                label="Days of week",
                options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                key=i,
            )
            appointment = st.slider(
                label='Time',
                min_value=time(0, 0),
                max_value=time(23, 59),

                step=timedelta(minutes=15),
                key=i + 10,
            )
            if vals:
                st.session_state.WEEK.append(vals)
            if appointment and vals != []:
                st.session_state.TIME.append([appointment] * len(vals))

    submitted = st.form_submit_button(label='Create Habit')

    if submitted:
        periods = list(zip(st.session_state.WEEK, st.session_state.TIME))
        print(periods)
        create_habit(
            name=name,
            description=description,
            place=place,
            outside=outside,
            preconditions=preconditions.split(';'),
            month=Months[month_name],
            year=year,
            week_periods=periods,
        )
        st.session_state.WEEK = []
        st.session_state.TIME = []
        st.write('Accepted!')
