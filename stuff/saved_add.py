# Structured version
def add2(operand1, operand2):
    return operand1 + operand2

def getter():
    num1 = int(input())
    num2 = int(input())
    return num1, num2

a,b = getter()
print(add2(a,b))


# Annotated version
def add2(operand1, operand2):
    ''' add two numbers '''
    return operand1 + operand2

def getter():
    ''' get two numbers '''
    num1 = int(input())
    num2 = int(input())
    return num1, num2

a,b = getter()
print(add2(a,b))


# OOP version
class Calc:
    def __init__(self):
        self.a = 0
        self.b = 0
    def add(self):
        return self.a + self.b
    def get(self):
        self.a = int(input())
        self.b = int(input())

calc1 = Calc()
calc1.get()
print(calc1.add())


# Recursive version
def adder(list_of_operands):
    if len(list_of_operands) == 1:
        return list_of_operands[0]
    else:
        return list_of_operands[0] + adder(list_of_operands[1:])

a = int(input())
b = int(input())
print(adder([a,b]))

