CODE_STYLES = [
    {
        "key": "structured",
        "name": "Structured",
        "description": "Structured code that aligns to PEP8.",
        "code_version": "# Structured version\n",
        "pylint_required": True,
        "pylint_parameters": ['--disable=all', '--enable=C'],
        "ast_required": False,
        "ast_parameters": None
    },
    {
        "key": "annotated",
        "name": "Annotated",
        "description": "Code with docstrings and type hints (PEP257/PEP484).",
        "code_version": "# Annotated version\n",
        "pylint_required": True,
        "pylint_parameters": ['--disable=all', '--enable=C0111,missing-type-doc'],
        "ast_required": False,
        "ast_parameters": None
    },
    {
        "key": "simple",
        "name": "Simple",
        "description": "Short, simple code with low complexity and separation of concerns.",
        "code_version": "# Simple version\n",
        "pylint_required": True,
        "pylint_parameters": [
            '--disable=all',
            '--enable=R0912,R0914,R0915,R0801,W0611,W0612,W0603'
        ],
        "ast_required": True,
        "ast_parameters": {"check": "separation_of_concerns"}
    },
    {
        "key": "oop",
        "name": "OOP",
        "description": "Object-oriented code using classes and methods.",
        "code_version": "# OOP version\n",
        "pylint_required": False,
        "pylint_parameters": [],
        "ast_required": True,
        "ast_parameters": {"check": "oop"}
    },
    {
        "key": "recursive",
        "name": "Recursive",
        "description": "Code that uses recursion.",
        "code_version": "# Recursive version\n",
        "pylint_required": False,
        "pylint_parameters": [],
        "ast_required": True,
        "ast_parameters": {"check": "recursive"}
    },
    {
        "key": "minimalist",
        "name": "Minimalist",
        "description": "Short, concise code with no unnecessary elements.",
        "code_version": "# Minimalist version\n",
        "pylint_required": True,
        "pylint_parameters": ['--disable=all', '--enable=W0611,W0612'],
        "ast_required": False,
        "ast_parameters": None
    }
]