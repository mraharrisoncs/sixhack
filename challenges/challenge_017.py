"""
[challenge]
id = "challenge_017"
title = "Memory Manager"
description = "Simulate loading programs into RAM with virtual memory overflow"
difficulty = "intermediate"
spec_level = "a_level"
topic = "Systems"
free = false

instructions = '''
Simulate a simple memory manager. Input:
  Line 1: total RAM capacity
  Line 2: total virtual memory capacity
  Line 3: number of programs to load (N)
  Lines 4 to N+3: size of each program

For each program print:
  "Loaded into RAM" if it fits in remaining RAM
  "Swapped to virtual memory" if RAM is full but it fits in virtual memory
  "Error: out of memory" if neither has enough space

Example (RAM=50, VM=100, 2 programs of sizes 40 and 30):
  Loaded into RAM
  Swapped to virtual memory
'''

starter_code = '''
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
'''

hints = [
    "Debug: Use RAM=10, VM=5, then load programs of sizes 6, 4, 8 — trace each Loaded/Swapped/Error decision.",
    "Debug: The code works but uses deeply nested if/else — an elif flattens this.",
    "Structured: Extract def load_program(size, used_ram, ram, used_vm, vm): returning a status string.",
    "Readable: Use descriptive names like ram_capacity, vm_capacity, programs_to_load, program_size.",
    "Robust: What if a program size is 0 or negative? What if RAM or VM capacity is 0? Add validation.",
    "OOP: Create a MemoryManager class that tracks state and has a load(size) method.",
    "Recursive: Not natural here, but you could process the list of program sizes recursively.",
    "Minimalist: The nested if/else can be flattened into a short elif chain.",
]

[[solutions]]
paradigm = "structured"
code = '''
def load_program(size, used_ram, ram, used_vm, vm):
    if used_ram + size <= ram:
        return "Loaded into RAM", used_ram + size, used_vm
    elif used_vm + size <= vm:
        return "Swapped to virtual memory", used_ram, used_vm + size
    return "Error: out of memory", used_ram, used_vm

ram = int(input())
vm = int(input())
used_ram = 0
used_vm = 0
n = int(input())
for _ in range(n):
    size = int(input())
    status, used_ram, used_vm = load_program(size, used_ram, ram, used_vm, vm)
    print(status)
'''

[[solutions]]
paradigm = "readable"
code = '''
# Simulate loading programs into RAM with virtual memory overflow
ram_capacity = int(input())
vm_capacity = int(input())
program_count = int(input())

used_ram = 0
used_vm = 0

for _ in range(program_count):
    program_size = int(input())

    # Try RAM first, then virtual memory, then report failure
    if used_ram + program_size <= ram_capacity:
        used_ram += program_size
        print("Loaded into RAM")
    elif used_vm + program_size <= vm_capacity:
        used_vm += program_size
        print("Swapped to virtual memory")
    else:
        print("Error: out of memory")
'''

[[solutions]]
paradigm = "robust"
code = '''
def validate_positive(value, name):
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")

def load_program(size, used_ram, ram, used_vm, vm):
    validate_positive(size, "Program size")
    if used_ram + size <= ram:
        return "Loaded into RAM", used_ram + size, used_vm
    elif used_vm + size <= vm:
        return "Swapped to virtual memory", used_ram, used_vm + size
    return "Error: out of memory", used_ram, used_vm

try:
    ram = int(input())
    vm = int(input())
    n = int(input())
    used_ram, used_vm = 0, 0
    for _ in range(n):
        size = int(input())
        status, used_ram, used_vm = load_program(size, used_ram, ram, used_vm, vm)
        print(status)
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
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

    def free_ram(self):
        return self.ram - self.used_ram

    def free_vm(self):
        return self.vm - self.used_vm

ram = int(input())
vm = int(input())
manager = MemoryManager(ram, vm)
n = int(input())
for _ in range(n):
    print(manager.load(int(input())))
'''

[[solutions]]
paradigm = "recursive"
code = '''
def process_programs(sizes, used_ram, ram, used_vm, vm):
    if not sizes:
        return
    size = sizes[0]
    if used_ram + size <= ram:
        print("Loaded into RAM")
        process_programs(sizes[1:], used_ram + size, ram, used_vm, vm)
    elif used_vm + size <= vm:
        print("Swapped to virtual memory")
        process_programs(sizes[1:], used_ram, ram, used_vm + size, vm)
    else:
        print("Error: out of memory")
        process_programs(sizes[1:], used_ram, ram, used_vm, vm)

ram = int(input())
vm = int(input())
n = int(input())
sizes = [int(input()) for _ in range(n)]
process_programs(sizes, 0, ram, 0, vm)
'''

[[solutions]]
paradigm = "minimalist"
code = '''
ram, vm = int(input()), int(input())
ur, uv = 0, 0
for _ in range(int(input())):
    p = int(input())
    if ur+p<=ram: ur+=p; print("Loaded into RAM")
    elif uv+p<=vm: uv+=p; print("Swapped to virtual memory")
    else: print("Error: out of memory")
'''

[[tests]]
paradigm = "all"
name = "Normal - fits in RAM"
inputs = ["100", "50", "2", "40", "30"]
expected_output = "Loaded into RAM\nLoaded into RAM"

[[tests]]
paradigm = "all"
name = "Normal - second spills to VM"
inputs = ["50", "100", "2", "40", "30"]
expected_output = "Loaded into RAM\nSwapped to virtual memory"

[[tests]]
paradigm = "all"
name = "Normal - out of memory"
inputs = ["50", "30", "3", "40", "30", "20"]
expected_output = "Loaded into RAM\nSwapped to virtual memory\nError: out of memory"

[[tests]]
paradigm = "all"
name = "Boundary - exactly fills RAM"
inputs = ["100", "50", "2", "60", "40"]
expected_output = "Loaded into RAM\nLoaded into RAM"

[[tests]]
paradigm = "all"
name = "Boundary - single program too large for everything"
inputs = ["50", "50", "1", "200"]
expected_output = "Error: out of memory"
"""

# Illustrative only
ram = int(input())
vm = int(input())
used_ram, used_vm = 0, 0
n = int(input())
for _ in range(n):
    p = int(input())
    if used_ram + p <= ram:
        used_ram += p
        print("Loaded into RAM")
    elif used_vm + p <= vm:
        used_vm += p
        print("Swapped to virtual memory")
    else:
        print("Error: out of memory")
