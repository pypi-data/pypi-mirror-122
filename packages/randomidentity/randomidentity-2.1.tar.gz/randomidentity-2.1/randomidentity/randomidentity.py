import random

from .data import *


def identity():
	"""This function returns random data of people that you can use in your projects."""
	return '\n' + random.choice(names) + ' ' + random.choice(surnames) + '\n' + random.choice(streets_num) + ' '\
		+ random.choice(streets) + '\n' + random.choice(cities) + ', ' + random.choice(postal_codes) + '\n'\
		+ f'({random.choice(num_code)}) xxx-xxxx'


def name():
	"""This function returns random name that you can use in your projects."""
	return random.choice(names)


def surname():
	"""This function returns random surname that you can use in your projects."""
	return random.choice(surnames)


def street():
	"""This function returns random street that you can use in your projects."""
	return random.choice(streets)


def city():
	"""This function returns random city that you can use in your projects."""
	return random.choice(cities)


def postcode():
	"""This function returns random postcode that you can use in your projects."""
	return random.choice(postal_codes)
