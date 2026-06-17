"""
[challenge]
id = "challenge_002"
title = "Currency Converter"
description = "Convert EUR<>GBP using a fixed exchange rate"
difficulty = "beginner"
spec_level = "gcse"
topic = "Arithmetic"
free = true

instructions = '''
Input a currency amount prefixed with its symbol (e.g. £3 or €5 or E5) and convert it
to the other currency, displaying the result with the correct symbol.

Use an exchange rate of 0.85 (1 EUR = 0.85 GBP).

Examples:
  Input: £10   Output: €11.76
  Input: E100  Output: £85.0
'''

starter_code = '''
E = 0.85
f = input()
if f[0] in "eE€":
    t = float(f[1:]) * E
    c = "£"
else:
    t = float(f[1:]) / E
    c = "€"
o = c + str(round(t, 2))
print(o)
'''

[[paradigms]]
paradigm = "all"
hints = [
    "Try input £10 — does it give the right EUR amount? The single-letter variable names make tracing very hard.",
    "The variable name E shadows the exchange rate constant — rename it RATE to avoid confusion.",
]

[[paradigms.tests]]
name = "Normal - EUR to GBP"
inputs = ["E100"]
expected_output = "£85.0"

[[paradigms.tests]]
name = "Normal - GBP to EUR"
inputs = ["£34.53"]
expected_output = "€40.62"

[[paradigms.tests]]
name = "Boundary - zero amount"
inputs = ["e0"]
expected_output = "£0.0"

[[paradigms.tests]]
name = "Normal - large EUR"
inputs = ["€1000"]
expected_output = "£850.0"

[[paradigms]]
paradigm = "structured"
hints = [
    "Separate the conversion into def convert(amount, from_currency): and keep input/output in the main block.",
]
code = '''
RATE = 0.85

def eur_to_gbp(amount):
    return round(amount * RATE, 2)

def gbp_to_eur(amount):
    return round(amount / RATE, 2)

def convert(input_str):
    prefix = input_str[0]
    amount = float(input_str[1:])
    if prefix in "eE€":
        return "£" + str(eur_to_gbp(amount))
    return "€" + str(gbp_to_eur(amount))

print(convert(input()))
'''

[[paradigms]]
paradigm = "readable"
hints = [
    "Use EXCHANGE_RATE as the constant name, and descriptive names like input_string, prefix, amount.",
]
code = '''
# Exchange rate: 1 EUR = 0.85 GBP
EXCHANGE_RATE = 0.85

input_string = input()
prefix = input_string[0]
amount = float(input_string[1:])

# Determine direction of conversion from prefix character
if prefix in "eE€":
    converted_amount = round(amount * EXCHANGE_RATE, 2)
    output_symbol = "£"
else:
    converted_amount = round(amount / EXCHANGE_RATE, 2)
    output_symbol = "€"

print(output_symbol + str(converted_amount))
'''

[[paradigms]]
paradigm = "robust"
hints = [
    "What if the user types an amount with no prefix? Add a check for a valid prefix character.",
]
code = '''
RATE = 0.85
EUR_PREFIXES = "eE€"
GBP_PREFIXES = "£"

def convert(input_str):
    if not input_str:
        raise ValueError("Empty input")
    prefix = input_str[0]
    if prefix not in EUR_PREFIXES + GBP_PREFIXES:
        raise ValueError(f"Unknown currency prefix: {prefix!r}")
    try:
        amount = float(input_str[1:])
    except ValueError:
        raise ValueError(f"Invalid amount: {input_str[1:]!r}")
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if prefix in EUR_PREFIXES:
        return "£" + str(round(amount * RATE, 2))
    return "€" + str(round(amount / RATE, 2))

print(convert(input()))
'''

[[paradigms]]
paradigm = "oop"
hints = [
    "Create a CurrencyConverter class with a convert(amount_string) method.",
]
code = '''
class CurrencyConverter:
    RATE = 0.85

    def __init__(self):
        self.last_result = None

    def convert(self, input_str):
        prefix = input_str[0]
        amount = float(input_str[1:])
        if prefix in "eE€":
            self.last_result = "£" + str(round(amount * self.RATE, 2))
        else:
            self.last_result = "€" + str(round(amount / self.RATE, 2))
        return self.last_result

converter = CurrencyConverter()
print(converter.convert(input()))
'''

[[paradigms]]
paradigm = "recursive"
hints = [
    "Not natural for conversion — but you could build the rounding recursively as a learning exercise.",
]
code = '''
RATE = 0.85

def round_recursive(value, places):
    factor = 10 ** places
    return int(value * factor + 0.5) / factor

def convert(input_str):
    prefix = input_str[0]
    amount = float(input_str[1:])
    if prefix in "eE€":
        return "£" + str(round_recursive(amount * RATE, 2))
    return "€" + str(round_recursive(amount / RATE, 2))

print(convert(input()))
'''

[[paradigms]]
paradigm = "minimalist"
hints = [
    "The conversion logic fits in a few lines using a ternary expression.",
]
code = '''
RATE = 0.85
s = input()
p, a = s[0], float(s[1:])
print(("£" + str(round(a * RATE, 2))) if p in "eE€" else ("€" + str(round(a / RATE, 2))))
'''

"""

# Illustrative only
E = 0.85
f = input()
if f[0] in "eE€":
    t = float(f[1:]) * E
    c = "£"
else:
    t = float(f[1:]) / E
    c = "€"
print(c + str(round(t, 2)))
