let codeMirrorEditor; // <-- Move this to the top, outside any function

document.addEventListener('DOMContentLoaded', () => {
    let originalCode = "";
    let currentTab = null;
    const tabCodes = {}; // Store code for each tab
    let codeStyles = [];

    const codeTabsContainer = document.getElementById('code-tabs');
    const codeInputTextarea = document.getElementById('code-input');

    if (!codeTabsContainer || !codeInputTextarea) {
        console.error("Error: Missing required elements in DOM.");
        return;
    }

    // Initialize CodeMirror for the code-input textarea
    codeMirrorEditor = CodeMirror.fromTextArea(codeInputTextarea, {
        mode: 'python',
        theme: 'material',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        matchBrackets: true,
        autofocus: true
    });

    // Fetch code styles from backend and build tabs
    fetch('/sandbox/styles')
        .then(response => response.json())
        .then(styles => {
            codeStyles = styles;
            codeTabsContainer.innerHTML = '';
            styles.forEach((style, index) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'tab-button';
                button.textContent = style.name;
                if (index === 0) button.classList.add('active');
                codeTabsContainer.appendChild(button);

                button.addEventListener('click', () => {
                    // Save current code to the current tab
                    if (currentTab !== null) {
                        tabCodes[currentTab] = codeMirrorEditor.getValue();
                    }

                    // Switch active tab
                    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    currentTab = style.key;

                    // If this tab has no code yet, initialize it
                    if (!tabCodes[currentTab] || tabCodes[currentTab] === "") {
                        tabCodes[currentTab] = style.code_version + originalCode;
                    }
                    codeMirrorEditor.setValue(tabCodes[currentTab]);
                    // Optionally show style.description somewhere in the UI
                });
            });

            // Load the first version of the code by default
            currentTab = styles[0].key;
            tabCodes[currentTab] = styles[0].code_version + originalCode;
            codeMirrorEditor.setValue(tabCodes[currentTab]);
        });

    // Handle program dropdown selection
    const programDropdown = document.getElementById('program-dropdown');
    if (programDropdown) {
        programDropdown.addEventListener('change', (e) => {
            const programId = e.target.value;

            fetch(`/sandbox/original_code/${programId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.original_code) {
                        originalCode = data.original_code;
                        // Reset all tab codes
                        Object.keys(tabCodes).forEach(tab => {
                            tabCodes[tab] = "";
                        });
                        // Set the current tab's code
                        tabCodes[currentTab] = codeStyles.find(style => style.key === currentTab).code_version + originalCode;
                        codeMirrorEditor.setValue(tabCodes[currentTab]);
                    }
                })
                .catch(error => console.error('Error fetching original code:', error));

            loadTestCases(programId);
        });
    }

    // Load programs into the dropdown on page load
    loadPrograms();

    // Add event listener for the "Clear" button
    document.getElementById('clear-button').addEventListener('click', clearInputBox);

    // Clear placeholder when user begins typing
    document.getElementById('input-box').addEventListener('focus', () => {
        const inputBox = document.getElementById('input-box');
        if (inputBox.placeholder === 'Type input here e.g. [1,2] or click a numbered test above') {
            inputBox.placeholder = '';
        }
    });

    // Run the code with user-provided input values
    document.getElementById('run-button').addEventListener('click', async () => {
        const code = codeMirrorEditor.getValue();
        const inputBox = document.getElementById('input-box');
        let inputs;

        try {
            inputs = JSON.parse(inputBox.value);
        } catch (error) {
            document.getElementById('output').textContent = 'Error: Invalid input format. Please provide valid JSON.';
            return;
        }

        const response = await fetch('/sandbox/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, input: inputs })
        });

        const data = await response.json();
        const outputElement = document.getElementById('output');
        if (data.error) {
            outputElement.textContent = `Error:\n${data.error}`;
        } else {
            outputElement.textContent = data.output;
        }
    });

    // Save the current program as a new challenge
    document.getElementById('save-button').addEventListener('click', async () => {
        const programName = prompt("Enter a name for the challenge:");
        if (!programName) {
            alert("Challenge name is required!");
            return;
        }

        const code = codeMirrorEditor.getValue();
        const inputBox = document.getElementById('input-box');
        let inputValues;
        try {
            inputValues = JSON.parse(inputBox.value);
        } catch {
            alert("Please provide valid JSON input values before saving.");
            return;
        }
        const expectedOutput = document.getElementById('output').textContent.trim();

        if (!code || !inputValues || !expectedOutput) {
            alert("Please ensure the code, inputs, and expected output are filled in before saving.");
            return;
        }

        const response = await fetch('/sandbox/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: programName,
                code: code,
                test_cases: [
                    {
                        inputs: inputValues,
                        expected_output: expectedOutput
                    }
                ]
            })
        });

        const data = await response.json();
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            alert(data.message || "Challenge saved successfully!");
            loadPrograms();
        }
    });

    // Load new challenges into the database
    document.getElementById('load-db-button').addEventListener('click', async () => {
        const response = await fetch('/sandbox/load-db', { method: 'POST' });
        const data = await response.json();
        alert(data.message || "Database updated successfully!");
        loadPrograms();
    });
});

// --- Fetch available programs and populate the dropdown ---

function loadPrograms() {
    fetch('/sandbox/programs', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(programs => {
        const dropdown = document.getElementById('program-dropdown');
        dropdown.innerHTML = '<option value="" disabled selected>Select a program</option>';
        programs.forEach(program => {
            const option = document.createElement('option');
            option.value = program.id;
            option.textContent = program.name;
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error loading programs:', error));
}

// --- Fetch test cases dynamically and populate tabs ---

function loadTestCases(programId) {
    fetch(`/sandbox/test_cases/${programId}`)
        .then(response => response.json())
        .then(testCases => {
            const tabButtons = document.getElementById('tab-buttons');
            const tabContent = document.getElementById('tab-content');
            const testContainer = document.querySelector('.test-container');

            tabButtons.innerHTML = '';
            tabContent.innerHTML = '';
            if (testContainer) {
                tabContent.appendChild(testContainer);
            }

            testCases.forEach((test, index) => {
                const button = document.createElement('button');
                button.className = 'tab-button';
                button.textContent = `${test.number}: ${test.name}`;
                tabButtons.appendChild(button);

                button.addEventListener('click', () => {
                    const inputBox = document.getElementById('input-box');
                    if (inputBox) {
                        inputBox.value = JSON.stringify(test.inputs);
                    }
                });
            });

            // Remove existing All Tests button if present
            const existingAllTestsButton = document.getElementById('all-tests-button');
            if (existingAllTestsButton) {
                existingAllTestsButton.remove();
            }

            // Add the "All Tests" button
            const allTestsButton = document.createElement('button');
            allTestsButton.className = 'tab-button';
            allTestsButton.id = 'all-tests-button';
            allTestsButton.textContent = 'All Tests';
            tabButtons.appendChild(allTestsButton);

            allTestsButton.addEventListener('click', async () => {
                const code = codeMirrorEditor.getValue();

                const response = await fetch('/sandbox/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ program_id: programId, code })
                });

                const data = await response.json();
                const outputElement = document.getElementById('output');

                if (data.error) {
                    outputElement.textContent = `Error:\n${data.error}`;
                } else {
                    const results = data.results.map((result, index) => {
                        return `Test ${index + 1}: ${result.name}
Inputs: ${JSON.stringify(result.inputs)}
Expected: ${result.expected}; Actual: ${result.actual}
Passed: ${result.passed ? "✅" : "❌"}`;
                    }).join("\n");
                    outputElement.textContent = results;
                }
            });
        })
        .catch(error => console.error('Error loading test cases:', error));
}

// --- Utility functions ---

function clearInputBox() {
    const inputBox = document.getElementById('input-box');
    inputBox.value = '';
    inputBox.placeholder = 'Type input here e.g. [1,2] or click a numbered test above';
}
