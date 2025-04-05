# Nytescript
![Python Version](https://img.shields.io/badge/Python-%3E=3.12-blue.svg) \
It is a simple, interpreted esoteric programming language (esolang) implemented in Python. It's designed to be an easy language to use and remember syntax for,
similar to the ancient BASIC. Examples of functions include ```print()```, ```input_char()```, ```run()``` (Runs Nytescript Files) and so on.

### Warning:
Nytescript is not intended for practical use. Its primary purpose is for fun, experimentation, and exploring the boundaries of my skill :)

## Getting Started
### Prerequisites

* **Python 3.12 or higher:** Ensure you have Python installed on your system. You can download it from [Python Downloads](https://www.python.org/downloads/).

### Installation
1.  Clone or download the Nytescript repository:
    ```zsh
    git clone [https://github.com/nnnGi/nytescript.git](https://www.google.com/search?q=https://github.com/nnnGi/nytescript.git)
    cd nytescript
    ```
2. (Optional) Create a virtual environment:
    ```zsh
	python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
3. Run ```shell.py``` from python and enjoy!


# Further Information
Nytescript Esolang, written by @\_nnn_ (A.K.A @FlyBoyAce2) in Python 3.12.9 and 3.13.2	

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

This is an interpreted programming Language made in Python named Nytescript. It has essential functions such as
printing, input, conditional statements, definable functions, while and for loops, and the ability to run files and 
exit the programme. It supports comments in regional currency symbols $, £, #, € and ¥ with a format like Python for single line comments.

Nothing needs to be installed except the ```Nytescript.py``` file, preferably Python 3.12 and above.

© Copyright @\_nnn_ 2025 - 2025

### Example Program (File is included in repository)

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
