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

// Populate the dropdown with available programs
async function populateDropdown() {
    const response = await fetch('/sandbox/programs');
    const programs = await response.json();
    const dropdown = document.getElementById('program-dropdown');
    programs.forEach(program => {
        const option = document.createElement('option');
        option.value = program.id;
        option.textContent = program.name;
        dropdown.appendChild(option);
    });
}

// Load the selected program into the sandbox
document.getElementById('load-button').addEventListener('click', async () => {
    const dropdown = document.getElementById('program-dropdown');
    const programId = dropdown.value;

    if (!programId) {
        alert('Please select a program to load.');
        return;
    }

    const response = await fetch(`/sandbox/load?program_id=${programId}`);
    const program = await response.json();

    if (program.error) {
        alert(program.error);
    } else {
        document.getElementById('code-input').value = program.code;
    }
});

// Run the code with user-provided input values
document.getElementById('run-button').addEventListener('click', async () => {
    const code = document.getElementById('code-input').value;
    const inputValues = document.getElementById('input-values').value.split(',');

    const response = await fetch('/sandbox/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, input: inputValues })
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

    if (!programId) {
        alert('Please select a program to test.');
        return;
    }

    const response = await fetch('/sandbox/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ program_id: programId })
    });

    const data = await response.json();
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
    const code = document.getElementById('code-input').value;
    const inputValues = document.getElementById('input-values').value.split(',');
    const expectedOutput = prompt("Enter the expected output:");

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
    alert(data.message || "Challenge saved successfully!");
});

// Populate the dropdown on page load
populateDropdown();