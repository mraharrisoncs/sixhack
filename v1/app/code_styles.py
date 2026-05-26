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
                "message": "Code is not organised into functions.",
                "delta": -3
            },
            {
                "regex": r"not separated",
                "message": "Separation of concerns could be improved.",
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
                "message": "Poor variable or function naming.",
                "delta": -2
            },
            {
                "regex": r"C0301: .+",
                "message": "Line too long — break it up for readability.",
                "delta": -1
            },
            {
                "regex": r"C0326: .+",
                "message": "Missing whitespace around operator.",
                "delta": -1
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "readable"},
        "ast_feedback": [
            {
                "regex": r"no comments",
                "message": "Add comments to explain your code.",
                "delta": -3
            },
            {
                "regex": r"magic number",
                "message": "Avoid magic numbers — use named constants instead.",
                "delta": -2
            },
            {
                "regex": r"inconsistent indentation",
                "message": "Use consistent indentation throughout (2 or 4 spaces).",
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
                "message": "Avoid bare except clauses.",
                "delta": -3
            },
            {
                "regex": r"W0703: .+",
                "message": "Avoid catching broad exceptions.",
                "delta": -2
            }
        ],
        "ast_required": True,
        "ast_parameters": {"check": "robust"},
        "ast_feedback": [
            {
                "regex": r"input not type-checked",
                "message": "Type-check your inputs (e.g. use int() or float()).",
                "delta": -2
            },
            {
                "regex": r"input not validated",
                "message": "Validate your inputs — check they are within an acceptable range or format.",
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
    }
]
