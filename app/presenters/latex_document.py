import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command, Table, Tabu
from pylatex.utils import italic, bold
import os

if __name__ == '__main__':
    doc = Document('basic')
    doc.documentclass = Command(
        'documentclass',
        options=['12pt', 'landscape'],
        arguments=['article'],
    )
    doc.preamble.append(Command('title', 'Habit Name'))
    with doc.create(Section('Habit Data')):
        doc.append(bold('Habit description'))
        doc.append(italic('description'))

        doc.append(bold('\nHabit preconditions'))
        doc.append('preconditions')

        doc.append(bold('\nHabit place'))
        doc.append('place')

    with doc.create(Section('Table')):
        with doc.create(Tabu("X[r] X[r] X[r] X[r] X[r] X[r] X[r]")) as table:
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
