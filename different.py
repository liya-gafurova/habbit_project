import copy
import logging
import random
import re
import typing
from dataclasses import dataclass
from functools import reduce
from typing import NamedTuple
from collections import namedtuple, ChainMap, Counter

import pytest
from docx import Document

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

# class TransformationParamsToDocumentUseCase(typing.Protocol):
#     def transform(self, params, document):
#         pass
#
#
# class TransformHabitToDocument(TransformationParamsToDocumentUseCase):
#     def transform(self, params: habit.HabitEntity, document: habit.DocxDocument):
#         pass


## Polymorphism

class Cat:
    def __init__(self, name):
        self.name = name
        self.sound = 'Purrrr'

    def make_sound(self):
        print(self.sound)


class Dog:
    def __init__(self, name):
        self.name = name
        self.sound = 'Auff'

    def make_sound(self):
        print(self.sound)


animals = [Dog('Bobic'), Cat('Marysa'), Dog('Jack')]
for animal in animals:
    animal.make_sound()

# try lambdas

# сделать какое-то действие над каждым элементом списка
l = [46, 4, 11, 12, 64, 59, 59, 96, 39, 61, 80, 12, 32, 30, 14, 38, 53, 72, 11, 16]
l2 = list(map(lambda x: x // 10, l))

# https://tproger.ru/problems/python-3-exercises-for-beginners-geekbrains/
# Задача 22
# Напишите программу, которая принимает текст и выводит два слова: наиболее часто встречающееся и самое длинное.
text = '''In this situation, both the normal function and the lambda behave similarly. In the next section, you’ll see a situation where the behavior of a lambda can be deceptive due to its evaluation time (definition time vs runtime).'''

words = re.sub(re.compile('[.,!?-`\'’()]'), '', text).split(' ')
word_lens = list(map(len, words))
word_counts = Counter(words)
longest = words[word_lens.index(max(word_lens))]
frequent = next(
    iter({k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}))  # sort dict by value
print(longest, frequent)

## ----
word_counts = Counter(words)
frequent = word_counts.most_common()[0]
longest = max(words, key=len)
print(longest, frequent)

# С помощью анонимной функции (!!! lambda) извлеките (!!! filter()) из списка числа (list), делимые на 15.
l = [46, 4, 11, 12, 64, 59, 59, 96, 39, 30, 61, 80, 12, 32, 30, 14, 38, 53, 72, 11, 16]
ll = list(filter(lambda element: element % 15 == 0, l))
# https://acmp.ru/index.asp?main=tasks&str=%20&page=19&id_type=0 -- олимпиадные  задачи по программированию
# map / reduce

# map ()
# filter()
# reduce()

numbers = [3, 4, 5, 6]


def cum_sum(first, second):
    return first + second


d = reduce(cum_sum, numbers)
print(d)


# decorators

def wrapper(func):
    def inner(list_range):
        print('before function')
        func(list_range)
        print('after_function')

    return inner


@wrapper
def test_func(list_range):
    print([random.randint(1, list_range) for i in range(list_range)])


test_func(5)

## interpolation

from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=41, endpoint=True)

plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()
