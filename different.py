import logging
import typing
from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple, ChainMap

import pytest
from docx import Document

import app.habit as habit

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Money(NamedTuple):
    currency: str
    value: int


Line = namedtuple('Line', ['sku', 'qty'])


def test_equality():
    # objects with equal fields are equal
    assert Money('gbp', 10) == Money('gbp', 10)
    assert Name('Harry', 'Percival') != Name('Bob', 'Gregory')
    assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)


test_equality()

fiver = Money('gbp', 5)
tenner = Money('gbp', 10)


def can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner


def can_subtract_money_values():
    assert tenner - fiver == fiver


def adding_different_currencies_fails():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('gbp', 10)


def can_multiply_money_by_a_number():
    assert fiver * 5 == Money('gbp', 25)


def multiplying_two_money_values_is_an_error():
    with pytest.raises(TypeError):
        tenner * fiver


fruit_prices = {
    'apples': 98,
    'oranges': 110,
    'bananas': 120,
    'pineapples': 60,
}

vegetable_prices = {
    'tomatoes': 70,
    'cucumbers': 40,
    'pineapples': 888,
}

assortment = ChainMap(fruit_prices, vegetable_prices)

print(assortment)
print(assortment.values())
print(assortment.keys())

for key, item in assortment.items():
    print(key, item)  ## passes repeated key 'pineapples'


############################################################

def function_to_be_tested(param: int):
    return f'You have entered number: {param}'


############################################################

def test_create_document():
    document = Document()

    document.add_heading('Document Title', 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='List Number'
    )

    document.add_picture('./q101.jpg', width=Inches(1.25))

    records = (
        (3, '101', 'Spam'),
        (7, '422', 'Eggs'),
        (4, '631', 'Spam, spam, eggs, and spam')
    )

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    for qty, id, desc in records:
        row_cells = table.add_row().cells
        row_cells[0].text = str(qty)
        row_cells[1].text = id
        row_cells[2].text = desc

    document.add_page_break()

    document.save('demo.docx')


############################################################

## abstract protocol that describes behavior of an paticular class

class TransformationParamsToDocumentUseCase(typing.Protocol):
    def transform(self, params, document):
        pass


class TransformHabitToDocument(TransformationParamsToDocumentUseCase):
    def transform(self, params: habit.HabitEntity, document: habit.DocxDocument):
        pass
