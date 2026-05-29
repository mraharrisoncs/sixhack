ram = int(input())
vm = int(input())
used_ram = 0
used_vm = 0
n = int(input())
for i in range(n):
    p = int(input())
    if used_ram + p <= ram:
        used_ram = used_ram + p
        print("Loaded into RAM")
    else:
        if used_vm + p <= vm:
            used_vm = used_vm + p
            print("Swapped to virtual memory")
        else:
            print("Error: out of memory")

'''!SIX:
description = "Simulate loading programs into RAM with virtual memory overflow"
difficulty = "medium"
topic = "systems"
spec_level = "a_level"
hints = ["What happens if a single program is larger than all remaining RAM and VM combined?", "The logic is correct but deeply nested — could you flatten it?", "No functions make this hard to test or extend"]

[[test_cases]]
number = 1
name = "Normal - fits in RAM"
inputs = [100, 50, 2, 40, 30]
expected_output = "Loaded into RAM\nLoaded into RAM\n"

[[test_cases]]
number = 2
name = "Normal - second spills to VM"
inputs = [50, 100, 2, 40, 30]
expected_output = "Loaded into RAM\nSwapped to virtual memory\n"

[[test_cases]]
number = 3
name = "Normal - out of memory"
inputs = [50, 30, 3, 40, 30, 20]
expected_output = "Loaded into RAM\nSwapped to virtual memory\nError: out of memory\n"

[[test_cases]]
number = 4
name = "Boundary - exactly fills RAM"
inputs = [100, 50, 2, 60, 40]
expected_output = "Loaded into RAM\nLoaded into RAM\n"

[[test_cases]]
number = 5
name = "Boundary - single program too large for everything"
inputs = [50, 50, 1, 200]
expected_output = "Error: out of memory\n"

[[solutions]]
label = "Clean"
code = """
ram = int(input())
vm = int(input())
used_ram = 0
used_vm = 0

def load_program(size):
    global used_ram, used_vm
    if used_ram + size <= ram:
        used_ram += size
        return "Loaded into RAM"
    elif used_vm + size <= vm:
        used_vm += size
        return "Swapped to virtual memory"
    return "Error: out of memory"

n = int(input())
for _ in range(n):
    print(load_program(int(input())))
"""

[[solutions]]
label = "Structured"
code = """
class MemoryManager:
    def __init__(self, ram, vm):
        self.ram = ram
        self.vm = vm
        self.used_ram = 0
        self.used_vm = 0

    def load(self, size):
        if self.used_ram + size <= self.ram:
            self.used_ram += size
            return "Loaded into RAM"
        elif self.used_vm + size <= self.vm:
            self.used_vm += size
            return "Swapped to virtual memory"
        return "Error: out of memory"

ram = int(input())
vm = int(input())
manager = MemoryManager(ram, vm)
n = int(input())
for _ in range(n):
    print(manager.load(int(input())))
"""
!SIX.'''
