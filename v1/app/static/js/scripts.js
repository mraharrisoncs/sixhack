let codeMirrorEditor;
let styleScores = {};
let totalScore = 0;
let currentProgramMaxLines = null;
let currentProgramMaxBytes = null;
const MAX_SCORE = 60;
let currentTab = null; // <-- Move this here, at the top!

function updateTotalScore() {
    totalScore = Object.values(styleScores).reduce((a, b) => a + b, 0);
    const scoreText = document.getElementById('total-score-text');
    const scoreMeter = document.getElementById('total-score-meter');
    scoreText.textContent = `Total Score: ${totalScore} / ${MAX_SCORE}`;
    scoreMeter.value = totalScore;
}

function updateStyleScore(styleKey, score, feedbackArr) {
    styleScores[styleKey] = score;
    updateTabProgress(styleKey, score, feedbackArr);
    updateTotalScore();
}

function repaintTabFills() {
    Object.entries(styleScores).forEach(([key, score]) => {
        if (score > 0) updateTabProgress(key, score);
    });
}

function updateTabProgress(styleKey, score, feedbackArr) {
    const button = document.getElementById(`tab-btn-${styleKey}`);
    if (!button) return;
    // Clamp score between 0 and 10
    score = Math.max(0, Math.min(10, score));
    const percent = (score / 10) * 100;
    const fillColor = document.body.classList.contains('dark') ? 'steelblue' : '#700CBC';
    button.style.background = `linear-gradient(to right, ${fillColor} ${percent}%, #333 ${percent}%)`;
    // Tooltip: show score and feedback
    let tooltip = `${score}/10`;
    if (feedbackArr && feedbackArr.length) {
        tooltip += "\n" + feedbackArr.join('\n');
    }
    button.setAttribute('data-feedback', tooltip);
}

function setMeterFeedback(styleKey, feedback) {
    const feedbackDiv = document.getElementById(`meter-feedback-${styleKey}`);
    feedbackDiv.textContent = feedback;
}

document.addEventListener('DOMContentLoaded', () => {
    let originalCode = "";
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
        theme: localStorage.getItem('theme') === 'dark' ? 'material' : 'default',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autofocus: true
    });

    codeMirrorEditor.setValue(
        `# Welcome to Six Hack!
#
# Your goal is to find six different ways to solve the same problem.
# Given some starting code, you must rewrite or refactor it six ways:
#
#   Structured, Readable, Robust, OOP, Recursive and Minimalist
#
# Choose a challenge from the dropdown above to begin!`
    );

    // Create a single tooltip div
    const tabTooltip = document.createElement('div');
    tabTooltip.className = 'tab-tooltip';
    document.body.appendChild(tabTooltip);

    // Fetch code styles from backend and build tabs
    fetch('/sandbox/styles')
        .then(response => response.json())
        .then(styles => {
            codeStyles = styles;
            codeTabsContainer.innerHTML = '';
            styles.forEach((style, index) => {
                // Tab button
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'tab-button';
                button.id = `tab-btn-${style.key}`;
                button.textContent = style.name;
                if (index === 0) button.classList.add('active');
                codeTabsContainer.appendChild(button);

                // Tab click handler
                button.addEventListener('click', () => {
                    // Save current code to the current tab
                    if (currentTab !== null) {
                        tabCodes[currentTab] = codeMirrorEditor.getValue();
                    }

                    // Switch active tab
                    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    currentTab = style.key;

                    // If this tab has no code yet, initialize it (only if a program is loaded)
                    if (!tabCodes[currentTab] || tabCodes[currentTab] === "") {
                        tabCodes[currentTab] = originalCode ? style.code_version + originalCode : "";
                    }
                    if (tabCodes[currentTab]) codeMirrorEditor.setValue(tabCodes[currentTab]);
                });
            });

            // Load the first version of the code by default
            currentTab = styles[0].key;
            if (originalCode) {
                tabCodes[currentTab] = styles[0].code_version + originalCode;
                codeMirrorEditor.setValue(tabCodes[currentTab]);
            }
        });

    // Show tooltip on hover
    codeTabsContainer.addEventListener('mouseover', function (e) {
        if (e.target.classList.contains('tab-button')) {
            const feedback = e.target.getAttribute('data-feedback');
            if (feedback) {
                tabTooltip.textContent = feedback;
                const rect = e.target.getBoundingClientRect();
                tabTooltip.style.left = `${rect.left + window.scrollX}px`;
                tabTooltip.style.top = `${rect.bottom + window.scrollY + 4}px`;
                tabTooltip.style.display = 'block';
            }
        }
    });
    codeTabsContainer.addEventListener('mouseout', function (e) {
        if (e.target.classList.contains('tab-button')) {
            tabTooltip.style.display = 'none';
        }
    });

    // Handle program dropdown selection
    const programDropdown = document.getElementById('program-dropdown');
    if (programDropdown) {
        programDropdown.addEventListener('change', (e) => {
            const programId = e.target.value;

            // Offer to save if there's any progress and this isn't a restore
            if (!window.pendingGameRestore && Object.values(styleScores).some(s => s > 0)) {
                if (confirm("Save your current progress before switching challenge?")) {
                    if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();
                    const gameData = { programId: programDropdown.dataset.lastId, tabCodes: { ...tabCodes }, currentTab, styleScores: { ...styleScores } };
                    const blob = new Blob([JSON.stringify(gameData, null, 2)], { type: "application/json" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url; a.download = "sixhack_save.json"; a.click();
                    URL.revokeObjectURL(url);
                }
            }
            programDropdown.dataset.lastId = programId;

            fetch(`/sandbox/original_code/${programId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.original_code) {
                        originalCode = data.original_code;
                        Object.keys(tabCodes).forEach(tab => { tabCodes[tab] = ""; });
                        tabCodes[currentTab] = codeStyles.find(style => style.key === currentTab).code_version + originalCode;
                        codeMirrorEditor.setValue(tabCodes[currentTab]);

                        // Reset scores, tab colours, and output
                        Object.keys(styleScores).forEach(key => {
                            styleScores[key] = 0;
                            const btn = document.getElementById(`tab-btn-${key}`);
                            if (btn) { btn.style.background = ''; btn.removeAttribute('data-feedback'); }
                        });
                        document.getElementById('output').textContent = '';
                        updateTotalScore();

                        // Apply a pending game restore if one was queued by Load Game
                        if (window.pendingGameRestore && window.pendingGameRestore.programId == programId) {
                            const restore = window.pendingGameRestore;
                            window.pendingGameRestore = null;
                            Object.assign(tabCodes, restore.tabCodes);
                            if (restore.styleScores) Object.assign(styleScores, restore.styleScores);
                            const savedTabBtn = document.getElementById(`tab-btn-${restore.currentTab}`);
                            if (savedTabBtn) {
                                savedTabBtn.click();
                            } else {
                                codeMirrorEditor.setValue(tabCodes[currentTab]);
                            }
                            updateTotalScore();
                        }
                    }
                })
                .catch(error => console.error('Error fetching original code:', error));

            fetch(`/sandbox/load?program_id=${programId}`)
                .then(response => response.json())
                .then(data => {
                    currentProgramMaxLines = data.max_lines ?? null;
                    currentProgramMaxBytes = data.max_bytes ?? null;
                })
                .catch(error => console.error('Error fetching program constraints:', error));

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
        if (inputBox.placeholder.startsWith('Type')) {
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
            document.getElementById('output-window').innerHTML = '<span class="output-error">Error: Invalid input format. Please provide valid JSON.</span>';
            return;
        }

        const response = await fetch('/sandbox/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, input: inputs })
        });

        const data = await response.json();
        const outputWindow = document.getElementById('output-window');
        if (data.error) {
            outputWindow.innerHTML = `<span class="output-error">Error:<br>${data.error}</span>`;
        } else {
            outputWindow.innerHTML = `<div><strong>Output:</strong><br><pre>${data.output}</pre></div>`;
        }
    });

    // Save the current program as a new challenge
    // --- Add save/load game functionality ---
    document.getElementById('save-game-button').addEventListener('click', () => {
        // Flush current editor content before saving
        if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();

        const programId = document.getElementById('program-dropdown')?.value || null;
        if (!programId) { alert("Select a challenge before saving."); return; }

        const gameData = {
            programId,
            tabCodes: { ...tabCodes },
            currentTab,
            styleScores: { ...styleScores },
        };
        const blob = new Blob([JSON.stringify(gameData, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = "sixhack_game_save.json";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    document.getElementById('load-game-button').addEventListener('click', () => {
        document.getElementById('load-game-input').click();
    });

    document.getElementById('load-game-input').addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function (e) {
            try {
                const gameData = JSON.parse(e.target.result);
                if (!gameData.programId || !gameData.tabCodes) throw new Error("Invalid save file.");

                // Queue the restore — the change handler will apply it after resetting tab codes
                window.pendingGameRestore = gameData;

                const dropdown = document.getElementById('program-dropdown');
                dropdown.value = gameData.programId;
                dropdown.dispatchEvent(new Event('change'));
                loadTestCases(gameData.programId);
            } catch (err) {
                alert("Failed to load game: " + err);
            }
        };
        reader.readAsText(file);
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
            dropdown.innerHTML = '<option value="" disabled selected>Select a challenge</option>';
            programs.forEach(program => {
                const option = document.createElement('option');
                option.value = program.id;
                const desc = program.description || program.name;
                const diff = program.difficulty ? ` [${program.difficulty}]` : '';
                option.textContent = desc + diff;
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
                button.textContent = `${index + 1}: ${test.name || ''}`;
                tabButtons.appendChild(button);

                button.addEventListener('click', async () => {
                    // Populate the input box with this test's inputs (single line)
                    const inputBox = document.getElementById('input-box');
                    if (inputBox) {
                        inputBox.value = JSON.stringify(test.inputs);
                    }

                    // Get the current code from the editor
                    const code = codeMirrorEditor.getValue();

                    // Run the code with this test's input
                    let actualOutput = '""';
                    let passed = false;
                    let errorMsg = null;
                    try {
                        const response = await fetch('/sandbox/run', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ code, input: test.inputs })
                        });
                        const data = await response.json();
                        if (data.error) {
                            errorMsg = data.error;
                        } else {
                            actualOutput = (data.output === undefined || data.output === null || data.output === '') ? '""' : data.output;
                            // Compare with expected output
                            let expected = (test.expected_output ?? "");
                            if (!isNaN(actualOutput) && !isNaN(expected) && actualOutput !== "" && expected !== "") {
                                passed = Number(actualOutput) === Number(expected);
                            } else {
                                passed = String(actualOutput).trim() === String(expected).trim();
                            }
                        }
                    } catch (err) {
                        errorMsg = err.toString();
                    }

                    // Format output for this test case
                    let outputHtml = `<div>`;
                    outputHtml += `<strong>Test ${index + 1}: ${test.name || ''}</strong>, Inputs: <code>${JSON.stringify(test.inputs)}</code><br>`;
                    outputHtml += `Expected Output: <code>${test.expected_output ?? '""'}</code><br>`;
                    if (errorMsg) {
                        outputHtml += `<span class="output-error">Error:<br>${errorMsg}</span>`;
                    } else {
                        outputHtml += `Actual Output:&nbsp;&nbsp;&nbsp;<code>${actualOutput}</code><br>`;
                        outputHtml += `Result: <span class="output-result">${passed ? 'PASS ✅' : 'FAIL ❌'}</span>`;
                        if (!passed) outputHtml += ` <span class="output-penalty">score -2</span>`;
                    }
                    outputHtml += `</div>`;

                    const outputWindow = document.getElementById('output-window');
                    if (outputWindow) {
                        outputWindow.innerHTML = outputHtml;
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

                fetch('/sandbox/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        program_id: programId, code, style: currentTab,
                        max_lines: currentProgramMaxLines, max_bytes: currentProgramMaxBytes
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        // Format test results
                        let outputHtml = `<div>`;
                        outputHtml += `<strong>Running test cases...</strong><br>`;
                        if (data.results && Array.isArray(data.results)) {
                            data.results.forEach((test, idx) => {
                                const pass = test.passed;
                                const tick = pass ? '✅' : '';
                                const cross = pass ? '' : '❌';
                                // Fix undefined/blank output
                                const actualOutput = (test.actual_output === undefined || test.actual_output === null || test.actual_output === '') ? '""' : test.actual_output;
                                const expectedOutput = (test.expected_output === undefined || test.expected_output === null || test.expected_output === '') ? '""' : test.expected_output;
                                outputHtml += `<div class="output-test">`;
                                outputHtml += `<strong>Test ${idx + 1}: ${test.name || ''}</strong>, Inputs: <code>${JSON.stringify(test.inputs)}</code><br>`;
                                outputHtml += `Expected Output: <code>${expectedOutput}</code><br>`;
                                if (test.error) {
                                    outputHtml += `<span class="output-error">Error: ${test.error}</span><br>`;
                                } else {
                                    outputHtml += `Actual Output:&nbsp;&nbsp;&nbsp;<code>${actualOutput}</code><br>`;
                                }
                                outputHtml += `Result: <span class="output-result">${pass ? 'PASS' : 'FAIL'} ${tick}${cross}</span>`;
                                if (!pass) outputHtml += ` <span class="output-penalty">score -2</span>`;
                                outputHtml += `</div>`;
                            });
                        }
                        outputHtml += `<hr><strong>Running style checks...</strong><br>`;
                        // Only show style feedback (not test feedback) here
                        if (data.feedback && Array.isArray(data.feedback)) {
                            // Filter out test feedback lines (those starting with 'Test "') and score line
                            const styleFeedback = data.feedback.filter(line =>
                                !/^Test "\w+/.test(line) && !/^Score: /.test(line)
                            );
                            styleFeedback.forEach(line => {
                                outputHtml += `${line}<br>`;
                            });
                        }
                        // Show score at the bottom
                        if (typeof data.score === 'number') {
                            outputHtml += `<hr><strong>Score: ${data.score}/10</strong>`;
                        }
                        outputHtml += `</div>`;

                        // Write output to output window
                        const outputWindow = document.getElementById('output-window');
                        if (outputWindow) {
                            outputWindow.innerHTML = outputHtml;
                        }

                        // Update tab score and tooltip
                        updateStyleScore(currentTab, data.score, data.feedback);
                    })
                    .catch(error => {
                        const outputWindow = document.getElementById('output-window');
                        if (outputWindow) {
                            outputWindow.textContent = 'Error running tests: ' + error;
                        }
                    });
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
