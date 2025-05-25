CODE_STYLES = [
    {
        "key": "structured",
        "name": "Structured",
        "description": "Structured code that aligns to PEP8.",
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
        "ast_parameters": {"check": "function"},
        "ast_feedback": [
            {
                "regex": r"no function",
                "message": "Code is not organized into functions.",
                "delta": -3
            }
        ]
    },
    {
        "key": "annotated",
        "name": "Annotated",
        "description": "Code with docstrings and type hints (PEP257/PEP484).",
        "code_version": "# Annotated version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=C0111,missing-type-doc',
            '--msg-template="{msg_id}: {msg}"'
        ],
        "pylint_feedback": [
            {
                "regex": r"C0111: .+",
                "message": "Missing docstring.",
                "delta": -3
            },
            {
                "regex": r"missing-type-doc",
                "message": "Missing type annotation.",
                "delta": -3
            }
        ],
        "ast_required": False,
        "ast_parameters": None,
        "ast_feedback": []
    },
    {
        "key": "simple",
        "name": "Simple",
        "description": "Short, simple code with low complexity and separation of concerns.",
        "code_version": "# Simple version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=R0912,R0914,R0915,R0801,W0611,W0612,W0603',
            '--msg-template="{msg_id}: {msg}"'
        ],
        "pylint_feedback": [
            {
                "regex": r"R0912: .+",
                "message": "High cyclomatic complexity detected.",
                "delta": -2
            },
            {
                "regex": r"R0914: .+",
                "message": "Too many local variables.",
                "delta": -2
            },
            {
                "regex": r"R0915: .+",
                "message": "Too many statements in a function.",
                "delta": -2
            },
            {
                "regex": r"R0801: .+",
                "message": "Duplicate code detected.",
                "delta": -2
            },
            {
                "regex": r"W0611: .+",
                "message": "Unused import found.",
                "delta": -1
            },
            {
                "regex": r"W0612: .+",
                "message": "Unused variable found.",
                "delta": -1
            },
            {
                "regex": r"W0603: .+",
                "message": "Global variables used.",
                "delta": -1
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "separation_of_concerns"},
        "ast_feedback": [
            {
                "regex": r"not separated",
                "message": "Separation of concerns could be improved.",
                "delta": -2
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
                "message": "Unused import found.",
                "delta": -3
            },
            {
                "regex": r"W0612: .+",
                "message": "Unused variable found.",
                "delta": -3
            }
        ],
        "ast_required": False,
        "ast_parameters": None,
        "ast_feedback": []
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
                "message": "No class detected.",
                "delta": -5
            },
            {
                "regex": r"Method.*missing 'self'",
                "message": "Method missing 'self' parameter.",
                "delta": -2
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
                "message": "No recursion detected.",
                "delta": -7
            },
            {
                "regex": r"No base case detected",
                "message": "No base case detected in recursion.",
                "delta": -2
            }
        ]
    },
    {
        "key": "function",
        "name": "Function",
        "description": "Code organized into functions.",
        "code_version": "# Function version\n",
        "pylint_required": False,
        "pylint_parameters": [],
        "pylint_feedback": [],
        "ast_required": True,
        "ast_parameters": {"check": "function"},
        "ast_feedback": [
            {
                "regex": r"no function",
                "message": "Code is not organized into functions.",
                "delta": -3
            }
        ]
    }
]