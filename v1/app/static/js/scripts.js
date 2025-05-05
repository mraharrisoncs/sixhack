document.getElementById('sandbox-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const code = document.getElementById('code-input').value;
    const inputValues = document.getElementById('input-values').value.split(',');

    // Send the code and input values to the server
    const response = await fetch('/sandbox', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, input: inputValues })
    });

    // Get the response and display it in the output window
    const data = await response.json();
    const outputElement = document.getElementById('output');
    if (data.error) {
        outputElement.textContent = `Error: ${data.error}`;
    } else {
        outputElement.textContent = data.output;
    }
});

// Load new challenges into the database
document.getElementById('load-db-button').addEventListener('click', async () => {
    const response = await fetch('/sandbox/load-db', { method: 'POST' });
    const data = await response.json();
    alert(data.message || "Database updated successfully!");
    loadPrograms(); // Refresh the dropdown
});

// Fetch available programs and populate the dropdown
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
            option.value = program.id; // Use program ID for fetching test cases
            option.textContent = program.name;
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error loading programs:', error));
}

// Automatically populate the sandbox when a program is selected
document.addEventListener('DOMContentLoaded', () => {
    let originalCode = ""; // Variable to store the original code

    const codeTabs = ['original', 'modular', 'robust', 'fast', 'documented', 'minimalist'];
    const codeVersions = {
        modular: "# Modular version of the code\nprint('This is modular code')",
        robust: "# Robust version of the code\nprint('This is robust code')",
        fast: "# Fast version of the code\nprint('This is fast code')",
        documented: "# Documented version of the code\nprint('This is documented code')",
        minimalist: "# Minimalist version of the code\nprint('This is minimalist code')"
    };

    const codeTabsContainer = document.getElementById('code-tabs');
    const codeInput = document.getElementById('code-input');

    if (!codeTabsContainer || !codeInput) {
        console.error("Error: Missing required elements in DOM.");
        return;
    }

    // Clear existing tabs to prevent duplicates
    codeTabsContainer.innerHTML = '';

    // Create tabs dynamically
    codeTabs.forEach((tab, index) => {
        const button = document.createElement('button');
        button.className = 'tab-button';
        button.textContent = tab.charAt(0).toUpperCase() + tab.slice(1);
        if (index === 0) button.classList.add('active');
        codeTabsContainer.appendChild(button);

        button.addEventListener('click', () => {
            // Remove active class from all tabs
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));

            // Add active class to the clicked tab
            button.classList.add('active');

            // Load the corresponding code version into the editor
            if (tab === 'original') {
                codeInput.value = originalCode; // Always show the original code
            } else {
                codeInput.value = codeVersions[tab];
            }
        });
    });

    // Load the first version of the code by default
    codeInput.value = originalCode;

    // Handle program dropdown selection
    const programDropdown = document.getElementById('program-dropdown');
    if (programDropdown) {
        programDropdown.addEventListener('change', (e) => {
            const programId = e.target.value;

            // Fetch the original code for the selected program
            fetch(`/sandbox/original_code/${programId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.original_code) {
                        originalCode = data.original_code; // Store the original code
                        codeInput.value = originalCode; // Load the original code into the editor
                    }
                })
                .catch(error => console.error('Error fetching original code:', error));

            // Load the test cases for the selected program
            loadTestCases(programId);
        });
    }

    // Load programs into the dropdown on page load
    loadPrograms();
});

// Fetch test cases dynamically and populate tabs
function loadTestCases(programId) {
    fetch(`/sandbox/test_cases/${programId}`)
        .then(response => response.json())
        .then(testCases => {
            const tabButtons = document.getElementById('tab-buttons');
            const tabContent = document.getElementById('tab-content');
            const testContainer = document.querySelector('.test-container'); // Preserve the test-container

            // Clear only the dynamically created test tabs
            tabButtons.innerHTML = '';

            // Preserve the test-container and only clear dynamically created test content
            tabContent.innerHTML = '';
            if (testContainer) {
                tabContent.appendChild(testContainer); // Re-add the test-container
            }

            // Create test tabs dynamically
            testCases.forEach((test, index) => {
                const button = document.createElement('button');
                button.className = 'tab-button';
                button.textContent = `${test.number}: ${test.name}`;
                tabButtons.appendChild(button);

                // Add event listener for individual test tabs
                button.addEventListener('click', () => {
                    // Load test inputs into the static input-box
                    const inputBox = document.getElementById('input-box');
                    if (inputBox) {
                        inputBox.value = JSON.stringify(test.inputs); // Ensure inputs are properly formatted as JSON
                    }
                });
            });

            // Add the "All Tests" button
            const allTestsButton = document.createElement('button');
            allTestsButton.className = 'tab-button';
            allTestsButton.id = 'all-tests-button';
            allTestsButton.textContent = 'All Tests';
            tabButtons.appendChild(allTestsButton);

            // Add event listener for "All Tests" button
            allTestsButton.addEventListener('click', async () => {
                const code = document.getElementById('code-input').value;

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
                    // Format the test results
                    const results = data.results.map((result, index) => {
                        return `Test ${index + 1}: ${result.name}
Inputs: ${JSON.stringify(result.inputs)}
Expected: ${result.expected}; Actual: ${result.actual}
Passed: ${result.passed ? "✅" : "❌"}`;
                    }).join("\n");

                    // Display the formatted results in the output box
                    outputElement.textContent = results;
                }
            });
        })
        .catch(error => console.error('Error loading test cases:', error));
}

// Truncate long names for display
function truncateName(name, maxLength = 8) {
    return name.length > maxLength ? name.slice(0, maxLength) + '...' : name;
}

// Clear the input box
function clearInputBox() {
    const inputBox = document.getElementById('input-box');
    inputBox.value = '';
    inputBox.placeholder = 'Type input here e.g. [1,2] or click a numbered test above';
}

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
    const code = document.getElementById('code-input').value;
    const inputBox = document.getElementById('input-box');
    let inputs;

    try {
        inputs = JSON.parse(inputBox.value); // Parse the input as JSON
    } catch (error) {
        console.error('Invalid JSON input:', error);
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

    const code = document.getElementById('code-input').value;
    const inputValues = document.getElementById('input-values').value.split(',').map(value => value.trim());
    const expectedOutput = document.getElementById('output').textContent.trim();

    if (!code || inputValues.length === 0 || !expectedOutput) {
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
        loadPrograms(); // Refresh the dropdown after saving
    }
});

document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();

        // Remove active class from all buttons
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));

        // Add active class to the clicked button
        button.classList.add('active');

        // Hide all tab content
        document.querySelectorAll('#tab-content div').forEach(div => {
            div.style.display = 'none';
        });

        // Show the selected tab content
        document.getElementById(button.dataset.tab).style.display = 'block';
    });
});

function loadOriginalCode(programId = null) {
    const codeInput = document.getElementById('code-input');

    if (!codeInput) {
        console.error("Error: #code-input element not found.");
        return;
    }

    if (!programId) {
        codeInput.value = "# Select a program to load its original code.";
        return;
    }

    fetch(`/sandbox/original_code/${programId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error loading original code:", data.error);
            codeInput.value = "# Error loading original code.";
        } else {
            console.log("Original code loaded successfully.");
            codeInput.value = data.original_code; // Update only the value of the textarea
        }
    })
    .catch(error => {
        console.error("Error fetching original code:", error);
        codeInput.value = "# Error fetching original code.";
    });
}
