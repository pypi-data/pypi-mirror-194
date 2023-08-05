import math

def add(*numbers):
	"""Add"""
	total = 0
	for number in numbers:
		total += number
	return total

def sub(*numbers):
	"""Subtract"""
	total = numbers[0]
	for number in numbers[1:]:
		total -= number
	return total

def mult(*numbers):
	"""Multiply"""
	total = 1
	for number in numbers:
		total *= number
	return total

def div(*numbers):
	"""Divide"""
	total = numbers[0]
	for number in numbers[1:]:
		total /= number
	return total

def int_div(*numbers):
	"""Integer (floor) division"""
	total = numbers[0]
	for number in numbers[1:]:
		total //= number
	return total
	
def rnd(number, accuracy):
	"""Round the number to the specified accuracy.
Example: v.maths.rnd(365, 10) == 370"""
	a = number / accuracy
	if a % 1 >= 0.5:
		a //= 1
		a += 1
	else:
		a //= 1
	b = a * accuracy
	if b % 1 == 0:
		return int(b)
	return b

def ceil(number):
	"""Round up the number to the nearest integer"""
	if number % 1 == 0:
		return int(number)
	return int(number) + 1

def floor(number):
	"""Round down the number to the nearest integer"""
	return int(number)

def comb(n, k):
	return math.comb(n, k)

def acos(x):
	return math.acos(x)

def acosh(x):
	return math.acosh(x)

def asin(x):
	return math.asin(x)
