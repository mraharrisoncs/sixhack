'''!SIX:
description = "Convert EUR<>GBP"
difficulty = "easy"

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
!SIX.'''
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
