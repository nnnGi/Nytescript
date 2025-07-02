#######################################
# INTERNAL IMPORTS
#######################################

import string
import os, sys, subprocess
import time

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters + '_'
LETTERS_DIGITS = LETTERS + DIGITS
VERSION = '0.8.6'
FILE_EXTENSION = '.ns'

#######################################
# STDLIB
#######################################

STDLIB = {
	"python": """
	pass
""",
	"math": """
# Constants
var pi = 3.1415926535897932384626433832795028841971693993751
var e = 2.71828182845904523536028747135266249775724709369995
var tau = 2 * pi

# Simple Functions
func add(a, b) -> a + b
func sub(a, b) -> a - b
func mul(a, b) -> a * b
func div(a, b) -> a / b
func pow(a, b) -> a ^ b
func fdiv(a, b) -> a // b
func mod(a, b) -> a % b
func sqrt(n) -> n ^ (1/2)
func cbrt(n) -> n ^ (1/3)
func exp(n) -> e ^ x
func floor(n) -> Number(n // 1)
func ceil(n) -> if n % 1 == 0 then n else Number(n // 1) + 1
func abs(n) -> if n > 0 then n else 0 - n

# Complex Functions
func gamma(n)
	var torun = `math.gamma(${Number(n)})`
	import python
	return Number(Number(torun))
end 

func log2(n)
	var torun = `math.log2(${Number(n)})`
	import python
	return Number(Number(torun))
end 

func log10(n)
	var torun = `math.log10(${Number(n)})`
	import python
	return Number(Number(torun))
end 

func sin(n)
	var torun = `math.sin(${Number(n)})`
	import python
	return Number(Number(torun))
end

func cos(n)
	var torun = `math.cos(${Number(n)})`
	import python
	return Number(Number(torun))
end

func tan(n)
	var torun = `math.tan(${Number(n)})`
	import python
	return Number(Number(torun))
end

func log(n, b)
	var torun = `math.log10(${Number(n)})`
	import python
	var n = Number(Number(torun))

	var torun = `math.log10(${Number(b)})`
	import python
	var b = Number(Number(torun))

	return Number(n / b)
end

func factorial(n)
	var result = 1
	if n == 0 then
		return 1
	end

	for i = 0 to n then
		var result = result * (i + 1)
	end
	
	return result
end

func comb(n, k)
	if n == 0 then
		return 0
	end
	if k == 0 then
		return 0
	end

	var fn = 1
	var fk = 1
	var fnk = 1
	for i = 0 to n then 
		var fn = fn * (i + 1)
	end
	for i = 0 to k then 
		var fk = fk * (i + 1)
	end
	for i = 0 to n - k then 
		var fnk = fnk * (i + 1)
	end

	return Number(fn / (fk * fnk))
end

func fib(n)
	if n < 0 then
		return None
	elif n // 1 != n then
		return None
	elif n <= 1 then
		return n
	else
		var a = 0
		var b = 1

		for i = 2 to n + 1 then
			var temp = a
			var a = b
			var b = temp + b
		end

		return b
	end
end 
""",
	"random": """
func rand()
	var torun = 'random.random()'
	import python
	return Number(torun)
end

func randint(a, b)
	var torun = `random.randint(${a}, ${b})`
	import python
	return Number(torun)
end

func uniform(a, b)
	var torun = `random.uniform(${a}, ${b})`
	import python
	return Number(torun)
end

func randrange(start, stop, ste)
	var torun = `random.randrange(${start}, ${stop}, ${ste})`
	import python
	return Number(torun)
end
""",
	"str": """
func starmap(elements, fun)
	var new_elements = []

	for i = 0 to len(elements) then
		append(new_elements, fun(elements/i))
	end

	return new_elements
end

func getat(str, idx)
	if is_str(str) != True then; return None; end
	if is_num(idx) != True then; return None; end
	return str / idx
end
""",
}
