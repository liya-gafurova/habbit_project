import base64
import os
from datetime import time, timedelta, datetime

import streamlit as st
from pandas import DataFrame
from streamlit.state.widgets import NoValue

from app.domain.helpers import MonthsReverse, MonthsCycle, Months
from app.presenters.helpers import get_next_n_months_for_current
from app.use_cases.create_habit import create_habit, get_all_habits, get_habit_printed_flag, create_document

st.title('Habit App')

if 'WEEK' not in st.session_state:
    st.session_state.WEEK = []
if 'TIME' not in st.session_state:
    st.session_state.TIME = []


def display_habits_interface():
    st.write('Show all habits')
    habit_entities = get_all_habits()
    habit_data = [[habit_ent.data.name, habit_ent.data.description, habit_ent.place.place] for habit_ent in
                  habit_entities]
    df = DataFrame(habit_data, columns=['Name', 'Description', 'Location'])

    st.table(df)


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


def create_habit_interface():
    st.write('Create Habit')
    with st.form('Habit Parameters'):

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


def print_habit_interface():
    st.write('Print Habit Tracker')
    st.write('Show all habits')
    habit_entities = get_all_habits()
    habit_data = [[habit_ent.data.name,
                   habit_ent.data.description,
                   habit_ent.place.place,
                   get_habit_printed_flag(habit_ent)] for habit_ent in habit_entities]

    df = DataFrame(habit_data, columns=['Name', 'Description', 'Location', 'Printed'])

    st.table(df)
    habit_entity_to_print = st.number_input(label='Habit id, which will be printed',
                                            max_value=len(habit_entities) - 1,
                                            value=NoValue(),
                                            step=1)

    submitted = st.button(label='Print!', )
    if submitted:
        try:
            habit_entity = habit_entities[habit_entity_to_print]
            created_doc_path = create_document(habit_entity)
            st.markdown(get_binary_file_downloader_html(created_doc_path), unsafe_allow_html=True)

        except Exception as er:
            print(er.args)
            st.write('Please, enter valid habit id.')


display_funcs = {
    'Display habits 📜': display_habits_interface,
    'Create Habit 🆕': create_habit_interface,
    'Print HabitTracker 🖨': print_habit_interface
}
selected_functionality = st.sidebar.selectbox(
    label='Habit App',
    options=list(display_funcs.keys())
)

display_funcs[selected_functionality]()
