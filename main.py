from collections import ChainMap

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


############################################################3

def function_to_be_tested(param: int):
    return f'You have entered number: {param}'
