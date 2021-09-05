## for API start
from datetime import time

import streamlit as st
from app.domain.helpers import DaysOfWeek

st.title('Create Your Habit Tracker')

if 'WEEK' not in st.session_state:
    st.session_state.WEEK = []
if 'TIME' not in st.session_state:
    st.session_state.TIME = []

with st.form('Habit Parameters'):
    name = st.text_input('Name')
    description = st.text_input('Description')
    place = st.text_input('Place')

    st.write('Preconditions')
    preconditions = st.text_input(
        'Please, enter your preconditions. If you have more. than 1, then separate them with ";"')

    number_of_week_periods = st.number_input('Number of Week Periods')
    n = 1
    if not number_of_week_periods:
        st.warning('Please input a number of Periods.')
        submitted = st.form_submit_button(label='Define', on_click=display_week, )
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
                # value=(time(12, 30)),
                key=i + 10,
            )
            if vals:
                st.session_state.WEEK.extend(vals)
            if appointment:
                st.session_state.TIME.append(appointment)

    submitted = st.form_submit_button(label='Create Habit')

    if submitted:
        st.write('Accepted!')
