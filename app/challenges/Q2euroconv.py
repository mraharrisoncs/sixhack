E = 0.85 # NB. changing this invalidates the test cases!
f = input()
if f[0] in "eE€":
    t = float(f[1:]) * E
    c = "£"
else:
    t = float(f[1:]) / E
    c = "€"
o = c + str(round(t, 2))
print(o)

'''!SIX:
description = "Convert EUR<>GBP"
instructions = "Input a currency amount prefixed with its symbol (e.g. £3 or €5) and convert it to the other currency, displaying the result with the correct symbol."
difficulty = "easy"
topic = "arithmetic"
spec_level = "gcse"
hints = ["Debug: Try input '£10' — does it give the right EUR amount? The single-letter variable names make tracing the logic very hard.", "Structure: Separate the conversion into def convert(amount, from_currency): and keep input/output in the main block only."]

[[test_cases]]
number = 1
name = "Normal - EUR to GBP"
inputs = ["E100"]
expected_output = "£85.0\n"

[[test_cases]]
number = 2
name = "Normal - GBP to EUR"
inputs = ["£34.53"]
expected_output = "€40.62\n"

[[test_cases]]
number = 3
name = "Boundary - zero amount"
inputs = ["e0"]
expected_output = "£0.0\n"

[[test_cases]]
number = 4
name = "Normal - large EUR"
inputs = ["€1000"]
expected_output = "£850.0\n"

[[solutions]]
label = "Clean"
code = """
RATE = 0.85

amount_str = input()
prefix = amount_str[0]
amount = float(amount_str[1:])

if prefix in "eE€":
    converted = amount * RATE
    symbol = "£"
else:
    converted = amount / RATE
    symbol = "€"

print(symbol + str(round(converted, 2)))
"""

[[solutions]]
label = "Structured"
code = """
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
"""
!SIX.'''
