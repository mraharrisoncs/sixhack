/**
 * Six Hack — sandbox scripts
 *
 * Manages the code editor, style tabs, test case tabs, program loading,
 * scoring display, save/load game, and the intro modal.
 */

let codeMirrorEditor;
let styleScores = {};
let currentProgramMaxLines = null;
let currentProgramMaxBytes = null;
let currentTab = null;

const MAX_SCORE = 60;

/** Recalculates the total score from styleScores and updates the display. */
function updateTotalScore() {
    const total = Object.values(styleScores).reduce((a, b) => a + b, 0);
    document.getElementById('total-score-text').textContent = `Total Score: ${total} / ${MAX_SCORE}`;
    document.getElementById('total-score-meter').value = total;
}

/**
 * Records a score for a style tab, updates its progress fill and tooltip,
 * then refreshes the total score display.
 * @param {string} styleKey
 * @param {number} score
 * @param {string[]} feedbackArr
 */
function updateStyleScore(styleKey, score, feedbackArr) {
    styleScores[styleKey] = score;
    updateTabProgress(styleKey, score, feedbackArr);
    updateTotalScore();
}

/**
 * Repaints all style tab progress fills — called after a theme toggle so
 * fill colours update to match the new theme.
 */
function repaintTabFills() {
    Object.entries(styleScores).forEach(([key, score]) => {
        if (score > 0) updateTabProgress(key, score);
    });
}

/**
 * Updates the visual progress fill and score tooltip on a single style tab.
 * @param {string} styleKey
 * @param {number} score  Raw score (clamped to 0–10 internally)
 * @param {string[]} [feedbackArr]
 */
function updateTabProgress(styleKey, score, feedbackArr) {
    const button = document.getElementById(`tab-btn-${styleKey}`);
    if (!button) return;
    score = Math.max(0, Math.min(10, score));
    const percent = (score / 10) * 100;
    const isDark = document.body.classList.contains('dark');
    const fillColor = isDark ? '#700CBC' : '#c49ad8';
    const unfilled  = isDark ? '#333'    : '#b8caf0';
    button.style.background = `linear-gradient(to right, ${fillColor} ${percent}%, ${unfilled} ${percent}%)`;
    let tooltip = `${score}/10`;
    if (feedbackArr && feedbackArr.length) {
        tooltip += '\n' + feedbackArr.join('\n');
    }
    button.setAttribute('data-feedback', tooltip);
}

/**
 * Shows the intro modal on first visit. Suppressed if the user has previously
 * ticked "Don't show this again" (stored in localStorage).
 */
function showIntroModal() {
    if (localStorage.getItem('sixhack_intro_seen')) return;

    const overlay = document.createElement('div');
    overlay.id = 'intro-overlay';
    overlay.innerHTML = `
        <div id="intro-modal">
            <h2>Welcome to Six Hack!</h2>
            <p>Your goal is to find <strong>six different ways</strong> to solve the same problem.</p>
            <p>Given a starting function, rewrite or refactor it in each of these styles:</p>
            <ul>
                <li><strong>Structured</strong> — clear, step-by-step with functions</li>
                <li><strong>Readable</strong> — self-documenting, easy to follow</li>
                <li><strong>Robust</strong> — handles edge cases and errors</li>
                <li><strong>OOP</strong> — object-oriented with classes</li>
                <li><strong>Recursive</strong> — solves the problem by calling itself</li>
                <li><strong>Minimalist</strong> — as short and clean as possible</li>
            </ul>
            <p>Choose a challenge from the dropdown, then use the style tabs to switch between your six versions. Hit <strong>All Tests</strong> to score your code!</p>
            <div class="modal-buttons">
                <label><input type="checkbox" id="intro-dont-show"> Don't show this again</label>
                <button id="intro-close-btn">Let's go! 🚀</button>
            </div>
        </div>`;
    document.body.appendChild(overlay);

    document.getElementById('intro-close-btn').addEventListener('click', () => {
        if (document.getElementById('intro-dont-show').checked) {
            localStorage.setItem('sixhack_intro_seen', '1');
        }
        overlay.remove();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    showIntroModal();

    let originalCode = '';
    const tabCodes = {};
    let codeStyles = [];

    const codeTabsContainer = document.getElementById('code-tabs');
    const codeInputTextarea = document.getElementById('code-input');

    if (!codeTabsContainer || !codeInputTextarea) {
        console.error('Six Hack: missing required DOM elements.');
        return;
    }

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
    codeMirrorEditor.setSize(null, 600);

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

    // Tooltip element shared across all style tabs
    const tabTooltip = document.createElement('div');
    tabTooltip.className = 'tab-tooltip';
    document.body.appendChild(tabTooltip);

    fetch('/sandbox/styles')
        .then(r => r.json())
        .then(styles => {
            codeStyles = styles;
            codeTabsContainer.innerHTML = '';
            styles.forEach((style, index) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'tab-button';
                button.id = `tab-btn-${style.key}`;
                button.textContent = style.name;
                if (index === 0) button.classList.add('active');
                codeTabsContainer.appendChild(button);

                button.addEventListener('click', () => {
                    if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();

                    document.querySelectorAll('#code-tabs .tab-button').forEach(b => b.classList.remove('active'));
                    button.classList.add('active');
                    currentTab = style.key;

                    // Initialise tab code on first visit if a program is loaded
                    if (!tabCodes[currentTab]) {
                        tabCodes[currentTab] = originalCode ? style.code_version + originalCode : '';
                    }
                    if (tabCodes[currentTab]) codeMirrorEditor.setValue(tabCodes[currentTab]);
                });
            });

            currentTab = styles[0].key;
        });

    codeTabsContainer.addEventListener('mouseover', (e) => {
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
    codeTabsContainer.addEventListener('mouseout', (e) => {
        if (e.target.classList.contains('tab-button')) tabTooltip.style.display = 'none';
    });

    const programDropdown = document.getElementById('program-dropdown');
    programDropdown.addEventListener('change', (e) => {
        const programId = e.target.value;

        // Offer to save progress before switching challenge (skip during a game restore)
        if (!window.pendingGameRestore && Object.values(styleScores).some(s => s > 0)) {
            if (confirm('Save your current progress before switching challenge?')) {
                if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();
                const gameData = {
                    programId: programDropdown.dataset.lastId,
                    tabCodes: { ...tabCodes },
                    currentTab,
                    styleScores: { ...styleScores }
                };
                const url = URL.createObjectURL(new Blob([JSON.stringify(gameData, null, 2)], { type: 'application/json' }));
                const a = document.createElement('a');
                a.href = url; a.download = 'sixhack_save.json'; a.click();
                URL.revokeObjectURL(url);
            }
        }
        programDropdown.dataset.lastId = programId;

        fetch(`/sandbox/original_code/${programId}`)
            .then(r => r.json())
            .then(data => {
                if (!data.original_code) return;
                originalCode = data.original_code;
                Object.keys(tabCodes).forEach(tab => { tabCodes[tab] = ''; });
                tabCodes[currentTab] = codeStyles.find(s => s.key === currentTab).code_version + originalCode;
                codeMirrorEditor.setValue(tabCodes[currentTab]);

                Object.keys(styleScores).forEach(key => {
                    styleScores[key] = 0;
                    const btn = document.getElementById(`tab-btn-${key}`);
                    if (btn) { btn.style.background = ''; btn.removeAttribute('data-feedback'); }
                });
                document.getElementById('output').textContent = '';
                updateTotalScore();

                // Apply a pending game restore queued by Load Game
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
            })
            .catch(err => console.error('Error fetching original code:', err));

        fetch(`/sandbox/load?program_id=${programId}`)
            .then(r => r.json())
            .then(data => {
                currentProgramMaxLines = data.max_lines ?? null;
                currentProgramMaxBytes = data.max_bytes ?? null;
            })
            .catch(err => console.error('Error fetching program constraints:', err));

        loadTestCases(programId);
    });

    loadPrograms();

    document.getElementById('clear-button').addEventListener('click', clearInputBox);

    document.getElementById('input-box').addEventListener('focus', (e) => {
        if (e.target.placeholder.startsWith('Type input')) e.target.placeholder = '';
    });

    document.getElementById('run-button').addEventListener('click', async () => {
        const code = codeMirrorEditor.getValue();
        const inputBox = document.getElementById('input-box');
        let inputs;
        try {
            inputs = JSON.parse(inputBox.value);
        } catch {
            document.getElementById('output-window').innerHTML =
                '<span class="output-error">Error: Invalid input format. Please provide valid JSON.</span>';
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

    document.getElementById('save-game-button').addEventListener('click', () => {
        if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();
        const programId = programDropdown.value || null;
        if (!programId) { alert('Select a challenge before saving.'); return; }

        const gameData = { programId, tabCodes: { ...tabCodes }, currentTab, styleScores: { ...styleScores } };
        const url = URL.createObjectURL(new Blob([JSON.stringify(gameData, null, 2)], { type: 'application/json' }));
        const a = document.createElement('a');
        a.href = url; a.download = 'sixhack_game_save.json';
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    document.getElementById('load-game-button').addEventListener('click', () => {
        document.getElementById('load-game-input').click();
    });

    document.getElementById('load-game-input').addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const gameData = JSON.parse(e.target.result);
                if (!gameData.programId || !gameData.tabCodes) throw new Error('Invalid save file.');
                window.pendingGameRestore = gameData;
                programDropdown.value = gameData.programId;
                programDropdown.dispatchEvent(new Event('change'));
            } catch (err) {
                alert('Failed to load game: ' + err);
            }
        };
        reader.readAsText(file);
    });
});

// ── Program loading ──────────────────────────────────────────────────────────

/** Fetches available challenges, populates the dropdown, and auto-selects the first. */
function loadPrograms() {
    fetch('/sandbox/programs')
        .then(r => r.json())
        .then(programs => {
            const dropdown = document.getElementById('program-dropdown');
            dropdown.innerHTML = '<option value="" disabled selected>Select a challenge</option>';
            programs.forEach(program => {
                const option = document.createElement('option');
                option.value = program.id;
                const diff = program.difficulty ? ` [${program.difficulty}]` : '';
                option.textContent = (program.description || program.name) + diff;
                dropdown.appendChild(option);
            });
            if (programs.length > 0) {
                dropdown.value = programs[0].id;
                dropdown.dispatchEvent(new Event('change'));
            }
        })
        .catch(err => console.error('Error loading programs:', err));
}

// ── Test case tabs ───────────────────────────────────────────────────────────

/** Fetches test cases for a challenge and renders numbered tabs plus "All Tests". */
function loadTestCases(programId) {
    fetch(`/sandbox/test_cases/${programId}`)
        .then(r => r.json())
        .then(testCases => {
            const tabButtons = document.getElementById('tab-buttons');
            tabButtons.innerHTML = '';

            testCases.forEach((test, index) => {
                const button = document.createElement('button');
                button.className = 'tab-button';
                button.textContent = `${index + 1}: ${test.name || ''}`;
                tabButtons.appendChild(button);

                button.addEventListener('click', async () => {
                    document.querySelectorAll('#tab-buttons .tab-button').forEach(b => b.classList.remove('active'));
                    button.classList.add('active');

                    const inputBox = document.getElementById('input-box');
                    if (inputBox) inputBox.value = JSON.stringify(test.inputs);

                    const code = codeMirrorEditor.getValue();
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
                            actualOutput = (data.output == null || data.output === '') ? '""' : data.output;
                            const expected = test.expected_output ?? '';
                            if (!isNaN(actualOutput) && !isNaN(expected) && actualOutput !== '' && expected !== '') {
                                passed = Number(actualOutput) === Number(expected);
                            } else {
                                passed = String(actualOutput).trim() === String(expected).trim();
                            }
                        }
                    } catch (err) {
                        errorMsg = err.toString();
                    }

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
                    if (outputWindow) outputWindow.innerHTML = outputHtml;
                });
            });

            // Remove stale All Tests button before re-adding for the new program
            document.getElementById('all-tests-button')?.remove();

            const allTestsButton = document.createElement('button');
            allTestsButton.className = 'tab-button';
            allTestsButton.id = 'all-tests-button';
            allTestsButton.textContent = 'All Tests';
            tabButtons.appendChild(allTestsButton);

            allTestsButton.addEventListener('click', async () => {
                document.querySelectorAll('#tab-buttons .tab-button').forEach(b => b.classList.remove('active'));
                allTestsButton.classList.add('active');

                const code = codeMirrorEditor.getValue();
                fetch('/sandbox/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        program_id: programId, code, style: currentTab,
                        max_lines: currentProgramMaxLines, max_bytes: currentProgramMaxBytes
                    })
                })
                    .then(r => r.json())
                    .then(data => {
                        let outputHtml = `<div><strong>Running test cases...</strong><br>`;
                        if (data.results && Array.isArray(data.results)) {
                            data.results.forEach((test, idx) => {
                                // Normalise blank/undefined outputs to empty-string sentinel
                                const actualOutput = (test.actual_output == null || test.actual_output === '') ? '""' : test.actual_output;
                                const expectedOutput = (test.expected_output == null || test.expected_output === '') ? '""' : test.expected_output;
                                outputHtml += `<div class="output-test">`;
                                outputHtml += `<strong>Test ${idx + 1}: ${test.name || ''}</strong>, Inputs: <code>${JSON.stringify(test.inputs)}</code><br>`;
                                outputHtml += `Expected Output: <code>${expectedOutput}</code><br>`;
                                if (test.error) {
                                    outputHtml += `<span class="output-error">Error: ${test.error}</span><br>`;
                                } else {
                                    outputHtml += `Actual Output:&nbsp;&nbsp;&nbsp;<code>${actualOutput}</code><br>`;
                                }
                                outputHtml += `Result: <span class="output-result">${test.passed ? 'PASS ✅' : 'FAIL ❌'}</span>`;
                                if (!test.passed) outputHtml += ` <span class="output-penalty">score -2</span>`;
                                outputHtml += `</div>`;
                            });
                        }
                        outputHtml += `<hr><strong>Running style checks...</strong><br>`;
                        if (data.feedback && Array.isArray(data.feedback)) {
                            // Strip per-test lines and the raw score line — only show style feedback
                            data.feedback
                                .filter(line => !/^Test "\w+/.test(line) && !/^Score: /.test(line))
                                .forEach(line => { outputHtml += `${line}<br>`; });
                        }
                        if (typeof data.score === 'number') {
                            outputHtml += `<hr><strong>Score: ${data.score}/10</strong>`;
                        }
                        outputHtml += `</div>`;

                        const outputWindow = document.getElementById('output-window');
                        if (outputWindow) outputWindow.innerHTML = outputHtml;
                        updateStyleScore(currentTab, data.score, data.feedback);
                    })
                    .catch(err => {
                        const outputWindow = document.getElementById('output-window');
                        if (outputWindow) outputWindow.textContent = 'Error running tests: ' + err;
                    });
            });
        })
        .catch(err => console.error('Error loading test cases:', err));
}

// ── Utilities ────────────────────────────────────────────────────────────────

/** Clears the input box and restores its placeholder text. */
function clearInputBox() {
    const inputBox = document.getElementById('input-box');
    inputBox.value = '';
    inputBox.placeholder = 'Type input e.g. [0,1] or click a tab above';
}
