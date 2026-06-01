CODE_STYLES = [
    {
        "key": "structured",
        "name": "Structured",
        "description": "Structured code that aligns to PEP8 with clear separation of concerns.",
        "code_version": "# Structured version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=C',
            '--msg-template="{msg_id}: {msg}"'
        ],
        "pylint_feedback": [
            {
                "regex": r"^C\d{4}: .+$",
                "message": None,
                "delta": -1
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "structured"},
        "ast_feedback": [
            {
                "regex": r"no function",
                "message": "Wrap your logic in a function — e.g. def calculate(): — and call it from a main block.",
                "delta": -3
            },
            {
                "regex": r"not separated",
                "message": "Keep input/output out of your calculation function — one function per job (get input, calculate, print result separately).",
                "delta": -2
            }
        ]
    },
    {
        "key": "readable",
        "name": "Readable",
        "description": "Code that is easy to read: meaningful names, comments, consistent indentation, no magic numbers.",
        "code_version": "# Readable version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=C0103,C0301,C0326',
            '--msg-template="{msg_id}: {msg}"'
        ],
        "pylint_feedback": [
            {
                "regex": r"C0103: .+",
                "message": "Use descriptive names — single letters and abbreviations make code hard to follow.",
                "delta": -2
            },
            {
                "regex": r"C0301: .+",
                "message": "Line too long — split it across multiple lines for readability.",
                "delta": -1
            },
            {
                "regex": r"C0326: .+",
                "message": "Add spaces around operators (e.g. x = a + b, not x=a+b).",
                "delta": -1
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "readable"},
        "ast_feedback": [
            {
                "regex": r"no comments",
                "message": "Add at least one comment explaining what your code does — use # to start a comment.",
                "delta": -3
            },
            {
                "regex": r"magic number",
                "message": "Replace raw numbers with named constants — e.g. TAX_RATE = 0.2 instead of 0.2 in the formula.",
                "delta": -2
            },
            {
                "regex": r"inconsistent indentation",
                "message": "Use consistent indentation — pick 4 spaces and stick to it throughout.",
                "delta": -2
            }
        ]
    },
    {
        "key": "robust",
        "name": "Robust",
        "description": "Code that handles errors and validates inputs.",
        "code_version": "# Robust version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=W0702,W0703',
            '--msg-template="{msg_id}: {msg}"'
        ],
        "pylint_feedback": [
            {
                "regex": r"W0702: .+",
                "message": "Avoid bare except: — always specify the exception type, e.g. except ValueError:",
                "delta": -3
            },
            {
                "regex": r"W0703: .+",
                "message": "Don't catch Exception broadly — catch specific errors like ValueError or TypeError.",
                "delta": -2
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "robust"},
        "ast_feedback": [
            {
                "regex": r"input not type-checked",
                "message": "Convert your input to the right type — e.g. num = int(input('Enter a number: ')).",
                "delta": -2
            },
            {
                "regex": r"input not validated",
                "message": "Validate your input — use a while loop or if statement to reject bad values before using them.",
                "delta": -2
            },
            {
                "regex": r"try/except found",
                "message": "Good — try/except error handling detected.",
                "delta": 0
            }
        ]
    },
    {
        "key": "oop",
        "name": "OOP",
        "description": "Object-oriented code using classes and methods.",
        "code_version": "# OOP version\n",
        "pylint_required": False,
        "pylint_parameters": [],
        "pylint_feedback": [],
        "ast_required": True,
        "ast_parameters": {"check": "oop"},
        "ast_feedback": [
            {
                "regex": r"No class detected",
                "message": "No class found — define a class using class MyClass: and put your methods inside it.",
                "delta": -5
            },
            {
                "regex": r"Method.*missing 'self'",
                "message": "Each method inside a class needs self as its first parameter — e.g. def calculate(self, x):",
                "delta": -2
            },
            {
                "regex": r"Class not instantiated",
                "message": "You defined a class but never created an object from it — e.g. obj = MyClass() somewhere in your code.",
                "delta": -3
            },
            {
                "regex": r"Class methods not used",
                "message": "You created an object but never called any of its methods — e.g. result = obj.calculate().",
                "delta": -3
            }
        ]
    },
    {
        "key": "recursive",
        "name": "Recursive",
        "description": "Code that uses recursion.",
        "code_version": "# Recursive version\n",
        "pylint_required": False,
        "pylint_parameters": [],
        "pylint_feedback": [],
        "ast_required": True,
        "ast_parameters": {"check": "recursive"},
        "ast_feedback": [
            {
                "regex": r"No recursion detected",
                "message": "No recursive call found — your function must call itself, e.g. return my_func(n - 1).",
                "delta": -7
            },
            {
                "regex": r"No base case detected",
                "message": "Add a base case — an if statement that stops the recursion, e.g. if n == 0: return 0.",
                "delta": -2
            },
            {
                "regex": r"Recursive function never called",
                "message": "Your recursive function exists but is never called — make sure you call it from outside the function.",
                "delta": -5
            }
        ]
    },
    {
        "key": "minimalist",
        "name": "Minimalist",
        "description": "Short, concise code with no unnecessary elements.",
        "code_version": "# Minimalist version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=W0611,W0612',
            '--msg-template="{msg_id}: {msg}"'
        ],
        "pylint_feedback": [
            {
                "regex": r"W0611: .+",
                "message": "Remove unused imports — only import what you actually use.",
                "delta": -3
            },
            {
                "regex": r"W0612: .+",
                "message": "Remove unused variables — if you assign it but never use it, delete it.",
                "delta": -3
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "minimalist"},
        "ast_feedback": [
            {
                "regex": r"Single-use variables could be inlined",
                "message": None,
                "delta": -2
            },
            {
                "regex": r"Too many lines",
                "message": None,
                "delta": -3
            },
            {
                "regex": r"Too many bytes",
                "message": None,
                "delta": -3
            }
        ]
    }
]
