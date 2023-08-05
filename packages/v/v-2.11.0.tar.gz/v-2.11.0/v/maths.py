import math

def add(*numbers):
	total = 0
	for number in numbers:
		total += number
	return total

def sub(*numbers):
	total = numbers[0]
	for number in numbers[1:]:
		total -= number
	return total

def mult(*numbers):
	total = 1
	for number in numbers:
		total *= number
	return total

def div(*numbers):
	total = numbers[0]
	for number in numbers[1:]:
		total /= number
	return total

def int_div(*numbers):
	total = numbers[0]
	for number in numbers[1:]:
		total //= number
	return total
	
def rnd(number, accuracy):
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
	if number % 1 == 0:
		return int(number)
	return int(number) + 1

def floor(number):
	return int(number)

def comb(n, k):
	return math.comb(n, k)

def acos(x):
	return math.acos(x)

def acosh(x):
	return math.acosh(x)

