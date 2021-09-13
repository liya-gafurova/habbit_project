import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command, Table, Tabu
from pylatex.utils import italic, bold
import os

if __name__ == '__main__':


    geometry_options = {
        "landscape": True,
    }
    doc = Document(page_numbers=True, geometry_options=geometry_options)



    with doc.create(Section('Habit Name')):
        doc.append('Habit description: ')
        doc.append(bold('description'))

        doc.append('\nHabit preconditions: ')
        doc.append(bold('preconditions'))

        doc.append('\nHabit place: ')
        doc.append(bold('place'))

    with doc.create(Section('Habit Tracker')):
        with doc.create(Tabu("|c|c|c|c|c|c|c|")) as table:
            table.add_hline()
            table.add_row((1, 2, 3, 4, 5,6,7))
            table.add_hline()
            table.add_row((1, 2, 3, 4, 5,6,7))
            table.add_hline()
            table.add_row((1, 2, 3, 4, 5, 6, 7))
            table.add_hline()
            table.add_row((1, 2, 3, 4, 5, 6, 7))
            table.add_hline()





    doc.generate_pdf('full', clean_tex=False)
