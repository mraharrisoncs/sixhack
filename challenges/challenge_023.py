"""
[challenge]
id = "challenge_023"
title = "Contact Records"
description = "Store and search contact records by name"
difficulty = "intermediate"
spec_level = "gcse"
topic = "Data Structures"
free = false

instructions = '''
Read a list of contacts and search for a contact by name.

Input format:
  Line 1: number of contacts N
  Next N lines: each contact as "name,phone,email"
  Last line: search name

Output: matching contact(s) as "name | phone | email", one per line.
        Print "Not found" if no match exists.

The robust paradigm searches case-insensitively.

Examples:
  Input: 2 contacts (Alice and Bob), search "Alice"
  Output: Alice | 123-456 | alice@example.com

  Input: 2 contacts (Alice and Bob), search "Charlie"
  Output: Not found
'''

starter_code = '''
n = int(input())
contacts = []
for _ in range(n):
    parts = input().split(",")
    contacts.append({"name": parts[0], "phone": parts[1], "email": parts[2]})
search_name = input().strip()
# Your code here: find and print matching contacts or "Not found"
'''

hints = [
    "Debug: Print the contacts list after reading it — check each dict has the right keys and values.",
    "Structured: Write a find_contact(contacts, name) function that loops and returns matching dicts.",
    "Readable: Use clear variable names; loop with for contact in contacts and check contact['name'].",
    "Robust: Use .lower() on both the contact name and search term to make the search case-insensitive.",
    "OOP: Create a ContactBook class with add(name, phone, email) and search(name) methods.",
    "Recursive: Search recursively — check the first contact, then recurse on the rest of the list.",
    "Minimalist: Use a list comprehension to filter matching contacts in one line.",
]

[[solutions]]
paradigm = "structured"
code = '''
def find_contacts(contacts, name):
    results = []
    for contact in contacts:
        if contact["name"] == name:
            results.append(contact)
    return results

n = int(input())
contacts = []
for _ in range(n):
    parts = input().split(",")
    contacts.append({"name": parts[0], "phone": parts[1], "email": parts[2]})
search_name = input().strip()

results = find_contacts(contacts, search_name)
if results:
    for c in results:
        print(f"{c['name']} | {c['phone']} | {c['email']}")
else:
    print("Not found")
'''

[[solutions]]
paradigm = "readable"
code = '''
# Read contacts and search by name
n = int(input())
contact_list = []
for _ in range(n):
    name, phone, email = input().split(",")
    contact_list.append({"name": name, "phone": phone, "email": email})

search_name = input().strip()

# Find all contacts whose name matches exactly
matching_contacts = []
for contact in contact_list:
    if contact["name"] == search_name:
        matching_contacts.append(contact)

if matching_contacts:
    for contact in matching_contacts:
        print(f"{contact['name']} | {contact['phone']} | {contact['email']}")
else:
    print("Not found")
'''

[[solutions]]
paradigm = "robust"
code = '''
def find_contacts(contacts, name):
    name_lower = name.strip().lower()
    return [c for c in contacts if c["name"].lower() == name_lower]

try:
    n = int(input())
    if n < 0:
        raise ValueError("Number of contacts cannot be negative")
    contacts = []
    for _ in range(n):
        parts = input().split(",")
        if len(parts) != 3:
            raise ValueError("Each contact must have name, phone, and email")
        contacts.append({"name": parts[0].strip(), "phone": parts[1].strip(), "email": parts[2].strip()})
    search_name = input().strip()
    results = find_contacts(contacts, search_name)
    if results:
        for c in results:
            print(f"{c['name']} | {c['phone']} | {c['email']}")
    else:
        print("Not found")
except ValueError as e:
    print(f"Error: {e}")
'''

[[solutions]]
paradigm = "oop"
code = '''
class ContactBook:
    def __init__(self):
        self._contacts = []

    def add(self, name, phone, email):
        self._contacts.append({"name": name, "phone": phone, "email": email})

    def search(self, name):
        return [c for c in self._contacts if c["name"] == name]

n = int(input())
book = ContactBook()
for _ in range(n):
    name, phone, email = input().split(",")
    book.add(name, phone, email)
search_name = input().strip()

results = book.search(search_name)
if results:
    for c in results:
        print(f"{c['name']} | {c['phone']} | {c['email']}")
else:
    print("Not found")
'''

[[solutions]]
paradigm = "recursive"
code = '''
def find_contacts(contacts, name, index=0):
    if index >= len(contacts):
        return []
    current = contacts[index]
    rest = find_contacts(contacts, name, index + 1)
    if current["name"] == name:
        return [current] + rest
    return rest

n = int(input())
contacts = []
for _ in range(n):
    parts = input().split(",")
    contacts.append({"name": parts[0], "phone": parts[1], "email": parts[2]})
search_name = input().strip()

results = find_contacts(contacts, search_name)
if results:
    for c in results:
        print(f"{c['name']} | {c['phone']} | {c['email']}")
else:
    print("Not found")
'''

[[solutions]]
paradigm = "minimalist"
code = '''
n = int(input())
contacts = [dict(zip(["name","phone","email"], input().split(","))) for _ in range(n)]
name = input().strip()
found = [c for c in contacts if c["name"] == name]
print("\n".join(f"{c['name']} | {c['phone']} | {c['email']}" for c in found) if found else "Not found")
'''

[[tests]]
paradigm = "all"
name = "Find existing contact"
inputs = ["2", "Alice,123-456,alice@example.com", "Bob,789-012,bob@example.com", "Alice"]
expected_output = "Alice | 123-456 | alice@example.com"

[[tests]]
paradigm = "all"
name = "No match found"
inputs = ["2", "Alice,123-456,alice@example.com", "Bob,789-012,bob@example.com", "Charlie"]
expected_output = "Not found"

[[tests]]
paradigm = "all"
name = "Find second contact"
inputs = ["2", "Alice,123-456,alice@example.com", "Bob,789-012,bob@example.com", "Bob"]
expected_output = "Bob | 789-012 | bob@example.com"

[[tests]]
paradigm = "robust"
name = "Case-insensitive search"
inputs = ["2", "Alice,123-456,alice@example.com", "Bob,789-012,bob@example.com", "alice"]
expected_output = "Alice | 123-456 | alice@example.com"
"""

# Illustrative only
n = int(input())
contacts = []
for _ in range(n):
    parts = input().split(",")
    contacts.append({"name": parts[0], "phone": parts[1], "email": parts[2]})
search_name = input().strip()
found = [c for c in contacts if c["name"] == search_name]
print("\n".join(f"{c['name']} | {c['phone']} | {c['email']}" for c in found) if found else "Not found")
