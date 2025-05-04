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
document.getElementById('import-button').addEventListener('click', async () => {
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
document.getElementById('program-dropdown').addEventListener('change', async (event) => {
    const programId = event.target.value;
    const response = await fetch(`/sandbox/load?program_id=${programId}`);
    const program = await response.json();

    if (program.error) {
        alert(program.error);
    } else {
        document.getElementById('code-input').value = program.code;
        loadTestCases(programId); // Load test cases for the selected program
    }
});

// Fetch test cases dynamically and populate tabs
async function loadTestCases(programId) {
    const response = await fetch(`/sandbox/test_cases/${programId}`);
    const testCases = await response.json();

    if (testCases.error) {
        alert(testCases.error);
        return;
    }

    const tabList = document.getElementById('tab-list');
    const tabContent = document.getElementById('tab-content');
    tabList.innerHTML = '';
    tabContent.innerHTML = '';

    testCases.forEach((test, index) => {
        // Create tab with test number and name
        const tab = document.createElement('li');
        tab.innerHTML = `<a href="#test-${test.number}">Test ${test.number}: ${test.name}</a>`;
        tabList.appendChild(tab);

        // Create tab content with inputs
        const content = document.createElement('div');
        content.id = `test-${test.number}`;
        content.style.display = index === 0 ? 'block' : 'none'; // Show the first tab by default
        content.innerHTML = `
            <textarea class="test-input">${JSON.stringify(test.inputs)}</textarea>
        `;
        tabContent.appendChild(content);
    });

    // Add event listeners for tabs
    document.querySelectorAll('#tab-list li a').forEach((tab, index) => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('#tab-content div').forEach(div => {
                div.style.display = 'none';
            });
            document.getElementById(`test-${testCases[index].number}`).style.display = 'block';
        });
    });
}

// Run the code with user-provided input values
document.getElementById('run-button').addEventListener('click', async () => {
    const code = document.getElementById('code-input').value;
    const inputValues = document.querySelector('.test-input').value;

    const response = await fetch('/sandbox/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, input: JSON.parse(inputValues) })
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