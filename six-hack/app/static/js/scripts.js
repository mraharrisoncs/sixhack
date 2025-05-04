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
    populateDropdown(); // Refresh the dropdown
});

// Fetch available programs and populate the dropdown
async function populateDropdown() {
    const response = await fetch('/sandbox/programs');
    const programs = await response.json();
    const dropdown = document.getElementById('program-dropdown');
    dropdown.innerHTML = '<option value="" disabled selected>Select a program</option>'; // Reset dropdown
    programs.forEach(program => {
        const option = document.createElement('option');
        option.value = program.id;
        option.textContent = program.name;
        dropdown.appendChild(option);
    });
}

// Automatically populate the sandbox when a program is selected
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('program-dropdown').addEventListener('change', async (event) => {
        const programId = event.target.value;
        console.log(`Selected Program ID: ${programId}`); // Debugging

        const response = await fetch(`/sandbox/load?program_id=${programId}`);
        const program = await response.json();
        console.log('Program Response:', program); // Debugging

        if (program.error) {
            alert(program.error);
        } else {
            document.getElementById('code-input').value = program.code;
            loadTestCases(programId); // Load test cases for the selected program
        }
    });
});

// Fetch test cases dynamically and populate tabs
async function loadTestCases(programId) {
    const response = await fetch(`/sandbox/test_cases/${programId}`);
    const testCases = await response.json();

    if (testCases.error) {
        alert(testCases.error);
        return;
    }

    const tabButtons = document.getElementById('tab-buttons');
    const tabContent = document.getElementById('tab-content');

    // Clear existing buttons and content, but keep the user input box
    tabButtons.innerHTML = '<button class="tab-button" data-tab="test-0">User Input</button>';
    tabContent.innerHTML = `
        <div id="test-0" style="display: block;">
            <textarea class="test-input" placeholder="Enter inputs here, e.g., [1, 2]"></textarea>
        </div>
    `;

    // Add test cases as additional buttons
    testCases.forEach((test, index) => {
        const tabIndex = index + 1; // Start from 1 since 0 is the user input

        // Create button
        const button = document.createElement('button');
        button.className = 'tab-button';
        button.dataset.tab = `test-${tabIndex}`;
        button.textContent = `Test ${test.number}: ${test.name}`;
        tabButtons.appendChild(button);

        // Create tab content
        const content = document.createElement('div');
        content.id = `test-${tabIndex}`;
        content.style.display = 'none'; // Hide by default
        content.innerHTML = `
            <textarea class="test-input">${JSON.stringify(test.inputs)}</textarea>
        `;
        tabContent.appendChild(content);
    });

    // Add event listeners for buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('#tab-content div').forEach(div => {
                div.style.display = 'none';
            });
            document.getElementById(button.dataset.tab).style.display = 'block';
        });
    });
}

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

// Test the loaded program against stored test cases
document.getElementById('test-button').addEventListener('click', async () => {
    const dropdown = document.getElementById('program-dropdown');
    const programId = dropdown.value;
    const currentCode = document.getElementById('code-input').value;

    console.log('Testing Program ID:', programId); // Debugging
    console.log('Current Code:', currentCode); // Debugging

    if (!programId) {
        alert('Please select a program to test.');
        return;
    }

    const response = await fetch('/sandbox/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ program_id: programId, code: currentCode })
    });

    const data = await response.json();
    console.log('Test Response:', data); // Debugging
    const outputElement = document.getElementById('output');
    if (data.error) {
        outputElement.textContent = `Error:\n${data.error}`;
    } else {
        const results = data.results.map(
            (r, i) =>
                `Test Case ${i + 1}:\nInputs: ${r.inputs}\nExpected: ${r.expected}\nActual: ${r.actual}\nPassed: ${r.passed}\n`
        );
        outputElement.textContent = results.join('\n');
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
        populateDropdown(); // Refresh the dropdown after saving
    }
});

// Populate the dropdown on page load
populateDropdown();