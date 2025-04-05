# Nytescript
Interpreted Programming Language (Esolang) made using Python; an example file is attached for reference

# Grammar
Found in the ```Grammar.txt``` file

# Description
Nytescript Esolang, written by @\_nnn_ (A.K.A @FlyBoyAce2) in Python 3.12.9 and 3.13.2	

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

This is an interpreted programming Language made in Python named Nytescript. It has essential functions such as
printing, input, conditional statements, definable functions, while and for loops, and the ability to run files and 
exit the programme. It supports comments in regional currency symbols $, £, #, € and ¥ with a format like Python for single line comments.

Nothing needs to be installed except the ```Nytescript.py``` file, preferably Python 3.12 and above.

© Copyright @\_nnn_ 2025 - 2025

# Example Program (File is included)

```
# This is a very useful piece of software
£ Regional Currency Symbols supported :p

func oopify(prefix) -> prefix + "oop"

func join(elements, separator)
	var result = ""
	var len = len(elements)

	for i = 0 to len then
		var result = result + elements/i
		if i != len - 1 then 
			var result = result + separator
		end
	end

	return result
end

func map(elements, fun)
	var new_elements = []

	for i = 0 to len(elements) then
		append(new_elements, fun(elements/i))
	end

	return new_elements
end

print("Greetings Nytescript")

for i = 0 to 5 then
	print(join(map(["l", "sp"], oopify), ", "))
end

print("Goodbye World")
```
