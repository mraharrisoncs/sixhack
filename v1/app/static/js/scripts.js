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
    console.log("DOM fully loaded and parsed."); // Debugging

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
    const tabContent = document.getElementById('tab-content');
    const testContainer = document.querySelector('.test-container'); // Preserve the test-container

    if (!codeTabsContainer) {
        console.error("Error: #code-tabs container not found."); // Debugging
        return;
    }

    if (!codeInput) {
        console.error("Error: #code-input textarea not found."); // Debugging
        return;
    }

    if (!tabContent) {
        console.error("Error: #tab-content container not found."); // Debugging
        return;
    }

    // Clear existing tabs to prevent duplicates
    codeTabsContainer.innerHTML = '';

    // Create tabs dynamically
    codeTabs.forEach((tab, index) => {
        console.log(`Creating tab: ${tab}`); // Debugging
        const button = document.createElement('button');
        button.className = 'tab-button';
        button.dataset.tab = `code-${index}`;
        button.textContent = tab.charAt(0).toUpperCase() + tab.slice(1); // Capitalize first letter
        if (index === 0) button.classList.add('active'); // Set the first tab as active by default
        codeTabsContainer.appendChild(button);

        // Add event listener for each tab
        button.addEventListener('click', () => {
            console.log(`Tab clicked: ${tab}`); // Debugging
            // Remove active class from all tabs
            document.querySelectorAll('#code-tabs .tab-button').forEach(btn => btn.classList.remove('active'));

            // Add active class to the clicked tab
            button.classList.add('active');

            // Load the corresponding code version into the editor
            if (tab === 'original') {
                console.log("Loading original code..."); // Debugging
                loadOriginalCode(); // Load the original code dynamically
            } else {
                codeInput.value = codeVersions[tab];
            }

            // Re-add the test-container to ensure it is not flushed
            if (testContainer && !tabContent.contains(testContainer)) {
                tabContent.appendChild(testContainer);
            }
        });
    });

    // Load the first version of the code by default
    console.log("Loading default code version: original"); // Debugging
    loadOriginalCode();

    // Initialize program dropdown
    const programDropdown = document.getElementById('program-dropdown');

    if (!programDropdown) {
        console.error("Error: #program-dropdown element not found."); // Debugging
        return;
    }

    programDropdown.addEventListener('change', (e) => {
        const programId = e.target.value;
        loadTestCases(programId); // Load the test cases into the tabbed input box
        loadOriginalCode(programId); // Load the original code for the selected program
    });

    // Load programs into the dropdown on page load
    loadPrograms();
});

// Fetch test cases dynamically and populate tabs
function loadTestCases(programId) {
    fetch(`/sandbox/test_cases/${programId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(testCases => {
        const tabList = document.getElementById('tab-buttons');
        const tabContent = document.getElementById('tab-content');
        const testContainer = document.querySelector('.test-container'); // Preserve the test-container

        // Clear only the dynamically created test tabs
        tabList.innerHTML = '';

        // Preserve the test-container and only clear dynamically created test content
        tabContent.innerHTML = ''; // Clear all content
        if (testContainer) {
            tabContent.appendChild(testContainer); // Re-add the test-container
        }

        // Create test tabs dynamically
        testCases.forEach((test, index) => {
            // Create tab button
            const tabButton = document.createElement('button');
            tabButton.className = 'tab-button';
            tabButton.dataset.tab = `test-${index}`;
            tabButton.textContent = `${test.number}: ${test.name}`; // Updated to show number and name only
            tabList.appendChild(tabButton);

            // Create tab content
            const content = document.createElement('div');
            content.id = `test-${index}`;
            content.style.display = index === 0 ? 'block' : 'none'; // Show the first tab by default
            content.innerHTML = `
                <textarea class="test-input">${JSON.stringify(test.inputs)}</textarea>
            `;
            tabContent.appendChild(content);
        });

        // Dynamically create the "All Tests" button
        const allTestsButton = document.createElement('button');
        allTestsButton.className = 'tab-button';
        allTestsButton.id = 'all-tests-button';
        allTestsButton.textContent = 'All Tests';
        tabList.appendChild(allTestsButton);

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
Expected: ${result.expected}; Actual: ${result.actual}
Passed: ${result.passed ? "✅" : "❌"}`;
                }).join("\n");

                // Display the formatted results in the output box
                outputElement.textContent = results;
            }
        });

        // Add event listeners for individual test tabs
        document.querySelectorAll('.tab-button').forEach((button) => {
            button.addEventListener('click', (e) => {
                document.querySelectorAll('#tab-content div').forEach(div => {
                    div.style.display = 'none';
                });
                document.getElementById(button.dataset.tab).style.display = 'block';
            });
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

    // Get the currently visible input box
    const activeInput = document.querySelector('#tab-content div[style="display: block;"] .test-input').value;

    const response = await fetch('/sandbox/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, input: JSON.parse(activeInput) })
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
