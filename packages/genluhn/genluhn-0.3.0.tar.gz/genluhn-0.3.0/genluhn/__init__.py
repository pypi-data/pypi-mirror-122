#!/usr/bin/env python
# -*- coding: utf-8 -*-

# genluhn, a library to compute and validate Luhn check digit on any base
# Copyright (C) 2021 Barcelona Supercomputinh Center, José M. Fernández
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

__author__ = 'José M. Fernández <https://orcid.org/0000-0002-4806-5140>'
__copyright__ = '© 2021 Barcelona Supercomputing Center (BSC), ES'
__license__ = 'LGPL-2.1'

# https://www.python.org/dev/peps/pep-0396/
__version__ = '0.3.0'

from typing import List, NewType, Union

Digit = NewType('Digit', int)
Digits = List[Digit]

def intToDigits(number:int, base:int) -> Digits:
	"""
	This method translates any integer to the digits notation
	"""
	
	# We are only going to deal with positive numbers
	if number < 0:
		number = -number
	
	digits = []
	while number >= base:
		digits.append(int(number % base))
		digits //= base
	digits.append(number)
	
	# Now, reverse it before returning it
	digits.reverse()
	
	return digits

MAX_STRTODIGITS_BASE = ord('z') - ord('a') + 1 + ord('9') - ord('0') + 1

def strToDigits(numstr:str, base:int) -> Digits:
	"""
	This method translates from a string notation to a list of digits.
	It removes dashes from the string, which are usually separators.
	This method only works with bases from 1 to 36
	"""
	
	if base > MAX_STRTODIGITS_BASE:
		raise ValueError('In str representations, base can be at most {}'.format(MAX_STRTODIGITS_BASE))
		
	# First, normalize the string, by removing dashes and translating
	# it to lower case
	numstr = numstr.replace('-','').lower()
	
	# Then, translate and check base validity
	digits = []
	ord0 = ord('0')
	# Tweak
	orda = ord('a') - 10
	for iletter,letter in enumerate(numstr):
		digit = None
		ordletter = ord(letter)
		if letter >= '0' and letter <= '9':
			digit = ordletter - ord0
		elif letter >= 'a' and letter <= 'z':
			digit = ordletter - orda
		
		if (digit is None) or digit >= base:
			raise ValueError("Invalid symbol '{}' at position {} for base {}".format(letter, iletter, base))
		
		digits.append(digit)
	
	return digits

def bytesToDigits(byteslike:Union[bytes, bytearray], base:int) -> Digits:
	"""
	This method translates from a byte notation to a list of digits.
	This method only works with bases 16 and 256
	"""
	
	if base==256:
		return list(byteslike)
	elif base==16:
		digits = []
		for bytelike in byteslike:
			digits.append((bytelike & 0xF0) >> 4)
			digits.append(bytelike & 0x0F)
		return digits
	else:
		raise ValueError('In bytes representations, base can be either 16 or 256')

def compute(digits:Union[str, int, bytes, bytearray, Digits], base:int) -> Digit:
	"""
	The input are either a list of integers, representing the digits
	of a number in a custom base, or a string representing the base
	(for instance, in hexadecimal textual notation) or an arbitrary
	large integer, which must be interpreted in the given base
	"""
	
	if not isinstance(base, int) or base < 1:
		raise ValueError('base must be an integer greater than 0')
	
	theDigits = None
	if isinstance(digits, int):
		theDigits = intToDigits(digits, base)
	elif isinstance(digits, str):
		theDigits = strToDigits(digits, base)
	elif isinstance(digits, (bytes, bytearray)):
		theDigits = bytesToDigits(digits, base)
	elif isinstance(digits, (list,tuple)):
		for idigit, digit in enumerate(digits):
			if digit < 0 or digit >= base:
				raise ValueError("Invalid digit '{}' at position {} for base {}".format(digit, idigit, base))
				
		theDigits = digits
	else:
		raise ValueError("digits must be either an int, a str, or an array of int")
	
	sumidx = len(theDigits) % 2
	
	# Half is summed
	partial = sum(theDigits[sumidx::2])
	# Half is doubled, digit summed and summed
	partial += sum(map(lambda d: sum(divmod(2*d, base)), theDigits[(1-sumidx)::2]))
	partial *= (base-1)
		
	return partial % base

def validate(digits:Union[str, int, bytes, bytearray, Digits], base:int, checkdigit:Digit) -> bool:
	return compute(digits, base) == checkdigit