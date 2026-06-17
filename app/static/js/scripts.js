/**
 * Six Hack — sandbox scripts
 */

let codeMirrorEditor;
let currentTab = null;
let currentProgramId = null;
let currentProgramIndex = 0;   // 1-based display number of active challenge

// Per-style scores for the current challenge (reset when switching)
let styleScores = {};

// Full save state: allChallenges[programId] = { tabCodes, styleScores }
let allChallenges = {};

// Constraints for minimalist check
let currentProgramMaxLines = null;
let currentProgramMaxBytes = null;

const MAX_STYLE_SCORE = 10;
const NUM_STYLES = 6;
const MAX_CHALLENGE_SCORE = MAX_STYLE_SCORE * NUM_STYLES; // 60

const AUTOSAVE_KEY = 'sixhack_autosave';

// ── Ranks ─────────────────────────────────────────────────────────────────────
let rankData = [];

fetch('/sandbox/ranks')
    .then(r => r.json())
    .then(data => { rankData = data; updateHeaderScores(); });

function getRank(totalScore) {
    for (let i = rankData.length - 1; i >= 0; i--) {
        if (totalScore >= rankData[i].min) {
            return `${rankData[i].name} ${rankData[i].emoji}`;
        }
    }
    return rankData.length ? `${rankData[0].name} ${rankData[0].emoji}` : '';
}

// ── Stage workflow state ──────────────────────────────────────────────────────
let currentStage = 'debug';   // 'debug' | 'unit' | 'final'

// ── Skulpt input mode ─────────────────────────────────────────────────────
// 'interactive' = inline input element in output window (Debug stage)
// 'server'      = unit test tabs post to /sandbox/run, Skulpt not used
let skulptInputMode = 'interactive';
let stageDebugDone = false;    // true once Skulpt has been run at least once
let unitTestsViewed = new Set(); // indices of unit test tabs clicked
let totalUnitTests = 0;

// ── Style tab state ───────────────────────────────────────────────────────────
let firstStyleKey = null;

// ── Timer ─────────────────────────────────────────────────────────────────────
let timerSeconds = 0;
let timerInterval = null;

function formatTimer(secs) {
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    const mm = String(m).padStart(2, '0');
    const ss = String(s).padStart(2, '0');
    return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
}

function updateTimerDisplay() {
    const el = document.getElementById('timer-display');
    if (el) el.textContent = formatTimer(timerSeconds);
}

function startTimer() {
    if (timerInterval) return;
    timerInterval = setInterval(() => { timerSeconds++; updateTimerDisplay(); }, 1000);
}

// ── Stage workflow ───────────────────────────────────────────────────────────

function switchStage(stage) {
    currentStage = stage;
    document.getElementById('debug-panel').style.display = stage === 'debug' ? '' : 'none';
    document.getElementById('unit-panel').style.display = stage === 'unit' ? '' : 'none';
    document.getElementById('final-panel').style.display = stage === 'final' ? '' : 'none';
    document.querySelectorAll('.stage-tab').forEach(btn => btn.classList.remove('stage-active'));
    document.getElementById(`stage-${stage}`).classList.add('stage-active');
    document.getElementById('output-window').classList.toggle('output-open-top', stage === 'debug');
    clearOutputTerminal();
    document.getElementById('output-window').innerHTML = '<pre id="output"></pre>';
}

function resetStageState() {
    stageDebugDone = false;
    unitTestsViewed = new Set();
    document.getElementById('stage-final').disabled = true;
    document.getElementById('stage-final').classList.remove('stage-unlocked');
    switchStage('debug');
}

function checkFinalUnlock() {
    const stageUnitDone = totalUnitTests > 0 && unitTestsViewed.size >= totalUnitTests;
    const finalBtn = document.getElementById('stage-final');
    if (stageDebugDone && stageUnitDone) {
        finalBtn.disabled = false;
        finalBtn.classList.add('stage-unlocked');
    }
}

// ── Style tab visibility ──────────────────────────────────────────────────────

function showStyleTabs() {
    document.getElementById('code-tabs').style.display = '';
    const banner = document.getElementById('style-tab-banner');
    if (banner) banner.style.display = 'none';
    if (currentProgramId) {
        if (!allChallenges[currentProgramId]) allChallenges[currentProgramId] = { tabCodes: {}, styleScores: {} };
        allChallenges[currentProgramId].stylesUnlocked = true;
    }
}

function hideStyleTabs() {
    document.getElementById('code-tabs').style.display = 'none';
    const banner = document.getElementById('style-tab-banner');
    if (banner) banner.style.display = '';
}

function applyStyleTabVisibility() {
    if (allChallenges[currentProgramId]?.stylesUnlocked) {
        showStyleTabs();
    } else {
        hideStyleTabs();
    }
}

// ── Debug style check ─────────────────────────────────────────────────────────

function runStyleCheck(code) {
    fetch('/sandbox/style_check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            style: currentTab,
            code,
            max_lines: currentProgramMaxLines,
            max_bytes: currentProgramMaxBytes
        })
    })
        .then(r => r.json())
        .then(results => {
            const outputWindow = document.getElementById('output-window');
            if (!outputWindow || !outputWindow.classList.contains('skulpt-terminal')) return;
            const NOISE = /^(No major issues detected\.|AST checks passed\.|(structured|readable|robust|oop|recursive|minimalist) OK)$/i;
            const msgs = [];
            Object.values(results).forEach(r => {
                if (r.feedback) r.feedback.filter(m => !NOISE.test(m.trim())).forEach(m => msgs.push(m));
            });
            const div = document.createElement('div');
            div.className = 'skulkt-style-check';
            if (msgs.length === 0) {
                div.innerHTML = '<div class="skulkt-style-label">Style ✔ No issues detected</div>' +
                    '<div class="skulkt-style-next">When you\'re ready to run Unit Tests click the Unit Tests button</div>';
            } else {
                div.innerHTML = '<div class="skulkt-style-label">Style</div>' +
                    msgs.map(m => `<div class="skulkt-style-msg">💡 ${m}</div>`).join('');
            }
            outputWindow.appendChild(div);
            outputWindow.scrollTop = outputWindow.scrollHeight;
        })
        .catch(() => { });
}

// ── Score helpers ────────────────────────────────────────────────────────────

function getChallengeScore(programId) {
    const c = allChallenges[programId];
    if (!c) return 0;
    return Object.values(c.styleScores || {}).reduce((a, b) => a + b, 0);
}

function getGrandTotal() {
    return Object.keys(allChallenges).reduce((sum, id) => sum + getChallengeScore(id), 0);
}

function updateHeaderScores() {
    const challengeEl = document.getElementById('challenge-score-display');
    const totalEl = document.getElementById('total-score-display');
    const rankEl = document.getElementById('rank-display');
    const scoreBox = document.getElementById('challenge-score-box');

    if (challengeEl) {
        const score = getChallengeScore(currentProgramId);
        const display = currentProgramId ? `${score}/${MAX_CHALLENGE_SCORE}` : '–';
        challengeEl.textContent = display;
        if (scoreBox) {
            scoreBox.title = currentProgramId
                ? `Score for this challenge: ${score}/${MAX_CHALLENGE_SCORE}`
                : 'Score for this challenge';
        }
    }

    const total = getGrandTotal();
    if (totalEl) totalEl.textContent = total;
    if (rankEl && rankData.length) rankEl.textContent = getRank(total);
}

function updateHexFill(programId) {
    const hex = document.querySelector(`.level-hex-wrap[data-id="${programId}"] .level-hex`);
    if (!hex) return;
    const score = getChallengeScore(programId);
    const pct = ((score / MAX_CHALLENGE_SCORE) * 100).toFixed(1);
    hex.style.setProperty('--fill-pct', `${pct}%`);
}


// ── Style tab score tracking ─────────────────────────────────────────────────

function updateStyleScore(styleKey, score, feedbackArr) {
    styleScores[styleKey] = score;
    // Mirror into allChallenges so it's always up to date
    if (currentProgramId) {
        if (!allChallenges[currentProgramId]) allChallenges[currentProgramId] = { tabCodes: {}, styleScores: {} };
        allChallenges[currentProgramId].styleScores[styleKey] = score;
    }
    updateTabProgress(styleKey, score, feedbackArr);
    updateHexFill(currentProgramId);
    updateHeaderScores();
}

function repaintTabFills() {
    document.querySelectorAll('#code-tabs .tab-button').forEach(btn => {
        const key = btn.id.replace('tab-btn-', '');
        updateTabProgress(key, styleScores[key] || 0);
    });
}

function updateTabProgress(styleKey, score, feedbackArr) {
    const button = document.getElementById(`tab-btn-${styleKey}`);
    if (!button) return;
    score = Math.max(0, Math.min(10, score));
    const percent = (score / 10) * 100;
    const isDark = document.body.classList.contains('dark');
    const fillColor = isDark ? '#700CBC' : '#c49ad8';
    const unfilled = isDark ? '#333' : '#b8caf0';
    button.style.background = `linear-gradient(to right, ${fillColor} ${percent}%, ${unfilled} ${percent}%)`;
    let tooltip = `${score}/10`;
    if (feedbackArr && feedbackArr.length) tooltip += '\n' + feedbackArr.join('\n');
    button.setAttribute('data-feedback', tooltip);
}

// ── Persistence ──────────────────────────────────────────────────────────────

function buildSaveData() {
    // Snapshot current tab before saving
    if (currentTab !== null && currentProgramId !== null) {
        if (!allChallenges[currentProgramId]) allChallenges[currentProgramId] = { tabCodes: {}, styleScores: {} };
        allChallenges[currentProgramId].tabCodes[currentTab] = codeMirrorEditor.getValue();
        allChallenges[currentProgramId].styleScores = { ...styleScores };
    }
    return {
        version: 1,
        currentProgramId,
        currentTab,
        timerSeconds,
        challenges: allChallenges
    };
}

function autoSave() {
    try {
        localStorage.setItem(AUTOSAVE_KEY, JSON.stringify(buildSaveData()));
    } catch (e) {
        console.warn('Six Hack: autosave failed', e);
    }
}

function restoreFromData(data, codeStyles) {
    if (!data || !data.challenges) return;
    allChallenges = data.challenges;
    if (typeof data.timerSeconds === 'number') {
        timerSeconds = data.timerSeconds;
        updateTimerDisplay();
    }
    // Repaint all hex fills from restored scores
    Object.keys(allChallenges).forEach(id => updateHexFill(id));
    updateHeaderScores();
}

// ── Intro modal ──────────────────────────────────────────────────────────────

function showIntroModal() {
    if (localStorage.getItem('sixhack_intro_seen')) return;
    const overlay = document.createElement('div');
    overlay.id = 'intro-overlay';
    overlay.innerHTML = `
        <div id="intro-modal">
            <h2>Welcome to six(im).possible().things()</h2>
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
            <p>Choose a challenge from the level bar, then use the style tabs to switch between your six versions. Hit <strong>All Tests</strong> to score your code!</p>
            <div class="modal-buttons">
                <label><input type="checkbox" id="intro-dont-show"> Don't show this again</label>
                <button id="intro-close-btn">Let's go! 🚀</button>
            </div>
        </div>`;
    document.body.appendChild(overlay);
    document.getElementById('intro-close-btn').addEventListener('click', () => {
        if (document.getElementById('intro-dont-show').checked)
            localStorage.setItem('sixhack_intro_seen', '1');
        overlay.remove();
    });
}

// ── DOMContentLoaded ─────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    showIntroModal();
    startTimer();

    let originalCode = '';
    const tabCodes = {};   // codes for the currently-active challenge's tabs
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
    codeMirrorEditor.setSize(null, 454);
    codeMirrorEditor.setValue('# Welcome to six(im).possible().things()\n#\n# Select a challenge from the level bar above to begin.');

    // Shared tooltip for style tabs
    const tabTooltip = document.createElement('div');
    tabTooltip.className = 'tab-tooltip';
    document.body.appendChild(tabTooltip);

    // Shared tooltip for level hexagons
    const levelTooltip = document.createElement('div');
    levelTooltip.className = 'level-tooltip';
    document.body.appendChild(levelTooltip);

    // Copy-to popover
    const copyPopover = document.createElement('div');
    copyPopover.id = 'tab-copy-popover';
    document.body.appendChild(copyPopover);

    const dismissPopover = () => { copyPopover.style.display = 'none'; };
    document.addEventListener('click', dismissPopover);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') dismissPopover(); });

    // ── Style tabs ───────────────────────────────────────────────────────────

    fetch('/sandbox/styles')
        .then(r => r.json())
        .then(styles => {
            codeStyles = styles;
            firstStyleKey = styles[0]?.key ?? null;
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
                    renderHints(currentTab);
                    resetStageState();
                    if (!tabCodes[currentTab]) {
                        tabCodes[currentTab] = originalCode ? style.code_version + originalCode : '';
                    }
                    if (tabCodes[currentTab]) codeMirrorEditor.setValue(tabCodes[currentTab]);
                });

                button.addEventListener('contextmenu', e => {
                    e.preventDefault();
                    tabTooltip.style.display = 'none';
                    if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();
                    const sourceKey = style.key;
                    const sourceCode = tabCodes[sourceKey] || '';
                    const targets = styles.filter(s => s.key !== sourceKey);
                    copyPopover.innerHTML = `<div class="popover-title">Copy code to…</div>`;
                    targets.forEach(target => {
                        const btn = document.createElement('button');
                        btn.textContent = target.name;
                        btn.addEventListener('click', () => {
                            tabCodes[target.key] = sourceCode;
                            if (currentTab === target.key) codeMirrorEditor.setValue(sourceCode);
                            dismissPopover();
                        });
                        copyPopover.appendChild(btn);
                    });
                    const allBtn = document.createElement('button');
                    allBtn.textContent = 'All tabs';
                    allBtn.className = 'popover-all';
                    allBtn.addEventListener('click', () => {
                        targets.forEach(target => {
                            tabCodes[target.key] = sourceCode;
                            if (currentTab === target.key) codeMirrorEditor.setValue(sourceCode);
                        });
                        dismissPopover();
                    });
                    copyPopover.appendChild(allBtn);
                    const rect = button.getBoundingClientRect();
                    copyPopover.style.display = 'block';
                    const pw = copyPopover.offsetWidth;
                    const left = Math.min(rect.left, window.innerWidth - pw - 8);
                    copyPopover.style.left = `${left}px`;
                    copyPopover.style.top = `${rect.bottom + 4}px`;
                });
            });
            currentTab = styles[0].key;

            // Restore autosave after styles are ready
            const saved = localStorage.getItem(AUTOSAVE_KEY);
            if (saved) {
                try {
                    const data = JSON.parse(saved);
                    restoreFromData(data, codeStyles);
                    // Load the last active challenge
                    if (data.currentProgramId) {
                        window.pendingRestore = data;
                        // loadPrograms will trigger loadChallenge which picks up pendingRestore
                    }
                } catch (e) {
                    console.warn('Six Hack: could not restore autosave', e);
                }
            }

            loadPrograms(levelTooltip, (programId, programIndex) => {
                loadChallenge(programId, programIndex, tabCodes, originalCode, codeStyles);
            });
        });

    // Style tab tooltips
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

    // ── Instructions panel ───────────────────────────────────────────────────

    const instructionsToggle = document.getElementById('instructions-toggle');
    const instructionsDetail = document.getElementById('instructions-detail');

    instructionsToggle.addEventListener('click', () => {
        const open = instructionsDetail.classList.toggle('open');
        instructionsToggle.textContent = open ? '▲ Hints' : '▼ Hints';
    });

    // ── loadChallenge ────────────────────────────────────────────────────────

    function loadChallenge(programId, programIndex, tabCodes, originalCode, codeStyles) {
        if (!programId) return;

        // Bank current challenge's code before switching
        if (currentProgramId !== null) {
            if (currentTab !== null) tabCodes[currentTab] = codeMirrorEditor.getValue();
            if (!allChallenges[currentProgramId]) allChallenges[currentProgramId] = { tabCodes: {}, styleScores: {} };
            allChallenges[currentProgramId].tabCodes = { ...tabCodes };
            allChallenges[currentProgramId].styleScores = { ...styleScores };
            autoSave();
        }

        currentProgramId = programId;
        currentProgramIndex = programIndex;

        // Highlight active hex wrapper
        document.querySelectorAll('.level-hex-wrap').forEach(h => {
            h.classList.toggle('active', h.dataset.id === String(programId));
        });

        // Restore or reset tab codes and scores for this challenge
        const saved = allChallenges[programId];
        const restoredTabCodes = saved ? { ...saved.tabCodes } : {};
        const restoredScores = saved ? { ...saved.styleScores } : {};

        // Clear current tab codes
        Object.keys(tabCodes).forEach(k => delete tabCodes[k]);
        Object.assign(tabCodes, restoredTabCodes);

        // Zero all scores first (clears previous challenge's tab fills), then restore
        // saved scores on top — order matters here
        Object.keys(styleScores).forEach(key => { styleScores[key] = 0; });
        document.querySelectorAll('#code-tabs .tab-button').forEach(btn => {
            btn.style.background = '';
            btn.removeAttribute('data-feedback');
        });

        Object.entries(restoredScores).forEach(([key, score]) => {
            styleScores[key] = score;
            updateTabProgress(key, score);
        });

        fetch(`/sandbox/original_code/${programId}`)
            .then(r => r.json())
            .then(data => {
                if (!data.original_code) return;
                originalCode = data.original_code;

                // Use saved tab code if available, else prepend style prefix to original
                const activeStyle = codeStyles.find(s => s.key === currentTab);
                if (!tabCodes[currentTab]) {
                    tabCodes[currentTab] = activeStyle ? activeStyle.code_version + originalCode : originalCode;
                }
                codeMirrorEditor.setValue(tabCodes[currentTab]);
                document.getElementById('output').textContent = '';

                // Handle pending restore from file load
                if (window.pendingRestore && window.pendingRestore.currentProgramId == programId) {
                    const restore = window.pendingRestore;
                    window.pendingRestore = null;
                    if (restore.currentTab) {
                        const btn = document.getElementById(`tab-btn-${restore.currentTab}`);
                        if (btn) btn.click();
                    }
                }
            })
            .catch(err => console.error('Error fetching original code:', err));

        fetch(`/sandbox/load?program_id=${programId}`)
            .then(r => r.json())
            .then(data => {
                currentProgramMaxLines = data.max_lines ?? null;
                currentProgramMaxBytes = data.max_bytes ?? null;
                updateInstructions(data);
            })
            .catch(err => console.error('Error fetching program info:', err));

        updateHexFill(programId);
        updateHeaderScores();
        resetStageState();
        applyStyleTabVisibility();
        loadTestCases(programId);
    }

    // ── Instructions update ──────────────────────────────────────────────────

    function updateInstructions(program) {
        window.currentProgram = program;
        document.getElementById('instructions-goal').textContent = program.description || program.name;
        const bodyEl = document.getElementById('instructions-body');
        if (bodyEl) bodyEl.textContent = program.instructions || '';
        const badges = document.getElementById('instructions-badges');
        badges.innerHTML = '';
        if (program.spec_level) {
            const b = document.createElement('span');
            b.className = `badge badge-spec badge-${program.spec_level}`;
            b.textContent = program.spec_level === 'a_level' ? 'A-Level' : 'GCSE';
            badges.appendChild(b);
        }
        if (program.topic) {
            const b = document.createElement('span');
            b.className = 'badge badge-topic';
            b.textContent = program.topic;
            badges.appendChild(b);
        }
        renderHints(currentTab);
    }

    function renderHints(paradigm) {
        const hintsMap = (window.currentProgram && window.currentProgram.hints) || {};
        const hints = (paradigm && hintsMap[paradigm]) || hintsMap['all'] || [];
        const hintsList = document.getElementById('hints-list');
        hintsList.innerHTML = '';
        if (hints.length) {
            hints.forEach(hint => {
                const li = document.createElement('li');
                li.textContent = hint;
                hintsList.appendChild(li);
            });
            instructionsToggle.disabled = false;
        } else {
            instructionsToggle.disabled = true;
            instructionsDetail.classList.remove('open');
            instructionsToggle.textContent = '▼ Hints';
        }
    }

    // ── Stage tab controls ───────────────────────────────────────────────────

    document.getElementById('stage-debug').addEventListener('click', () => {
        skulptInputMode = 'interactive';
        switchStage('debug');
    });
    document.getElementById('stage-unit').addEventListener('click', () => {
        skulptInputMode = 'server';
        switchStage('unit');
    });
    document.getElementById('stage-final').addEventListener('click', () => {
        if (!document.getElementById('stage-final').disabled) {
            skulptInputMode = 'server';
            switchStage('final');
        }
    });

    // ── Debug panel controls ─────────────────────────────────────────────────

    document.getElementById('run-button').addEventListener('click', () => {
        const code = codeMirrorEditor.getValue();
        const styleName = codeStyles.find(s => s.key === currentTab)?.name ?? currentTab;
        runWithSkulpt(code, `▶ Running Python 3 (Skulpt) · ${styleName}`)
            .then(() => runStyleCheck(code));
        stageDebugDone = true;
        checkFinalUnlock();
    });


    document.getElementById('save-game-button').addEventListener('click', () => {
        if (!currentProgramId) { alert('Select a challenge before saving.'); return; }
        const saveData = buildSaveData();
        const url = URL.createObjectURL(new Blob([JSON.stringify(saveData, null, 2)], { type: 'application/json' }));
        const a = document.createElement('a');
        a.href = url; a.download = 'sixhack_save.json';
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
                const data = JSON.parse(e.target.result);
                if (!data.challenges) throw new Error('Invalid save file.');
                restoreFromData(data, codeStyles);
                if (data.currentProgramId) {
                    window.pendingRestore = data;
                    // Find the hex to get the index
                    const hex = document.querySelector(`.level-hex-wrap[data-id="${data.currentProgramId}"]`);
                    const index = hex ? parseInt(hex.dataset.index) : 1;
                    loadChallenge(data.currentProgramId, index, tabCodes, originalCode, codeStyles);
                }
            } catch (err) {
                alert('Failed to load save: ' + err);
            }
        };
        reader.readAsText(file);
    });

    // Expose loadChallenge for use in loadTestCases (All Tests auto-save)
    window._loadChallenge = (id, idx) => loadChallenge(id, idx, tabCodes, originalCode, codeStyles);
    window._autoSave = autoSave;
    window._updateStyleScore = updateStyleScore;
});

// ── Program loading / level bar ──────────────────────────────────────────────

function loadPrograms(levelTooltip, onSelect) {
    fetch('/sandbox/programs')
        .then(r => r.json())
        .then(programs => {
            const levelBar = document.getElementById('level-bar');
            const scoresEl = document.getElementById('header-scores');
            // Insert hexagons before the scores element
            programs.forEach((program, index) => {
                const wrap = document.createElement('div');
                wrap.className = 'level-hex-wrap';
                wrap.dataset.id = program.id;
                wrap.dataset.index = index + 1;

                const diffClass = program.difficulty ? `diff-${program.difficulty}` : '';
                if (diffClass) wrap.classList.add(diffClass);

                const hex = document.createElement('div');
                hex.className = 'level-hex';
                hex.dataset.id = program.id;

                const label = document.createElement('span');
                label.textContent = index + 1;
                hex.appendChild(label);
                wrap.appendChild(hex);

                levelBar.insertBefore(wrap, scoresEl);

                wrap.addEventListener('mouseenter', () => {
                    const diff = program.difficulty ? ` · ${program.difficulty}` : '';
                    const level = program.spec_level
                        ? ` · ${program.spec_level === 'a_level' ? 'A-Level' : 'GCSE'}` : '';
                    levelTooltip.innerHTML = `<strong>${program.description || program.name}</strong>${diff}${level}`;
                    levelTooltip.style.display = 'block';
                    const rect = wrap.getBoundingClientRect();
                    const tw = levelTooltip.offsetWidth;
                    const left = Math.min(rect.left + rect.width / 2 - tw / 2, window.innerWidth - tw - 8);
                    levelTooltip.style.left = `${Math.max(4, left) + window.scrollX}px`;
                    levelTooltip.style.top = `${rect.bottom + window.scrollY + 6}px`;
                });
                wrap.addEventListener('mouseleave', () => { levelTooltip.style.display = 'none'; });
                wrap.addEventListener('click', () => onSelect(program.id, index + 1));
            });

            // Decide which challenge to open: pending restore or first
            const pending = window.pendingRestore;
            if (pending && pending.currentProgramId) {
                const hex = document.querySelector(`.level-hex-wrap[data-id="${pending.currentProgramId}"]`);
                const idx = hex ? parseInt(hex.dataset.index) : 1;
                onSelect(pending.currentProgramId, idx);
            } else if (programs.length > 0) {
                onSelect(programs[0].id, 1);
            }
        })
        .catch(err => console.error('Error loading programs:', err));
}

// ── Test case tabs ───────────────────────────────────────────────────────────

function loadTestCases(programId) {
    fetch(`/sandbox/test_cases/${programId}?style=${currentTab}`)
        .then(r => r.json())
        .then(testCases => {
            const tabButtons = document.getElementById('tab-buttons');
            tabButtons.innerHTML = '';
            totalUnitTests = testCases.length;
            unitTestsViewed.clear();

            testCases.forEach((test, index) => {
                const button = document.createElement('button');
                button.className = 'tab-button';
                button.textContent = `▶ ${index + 1}: ${test.name || ''}`;
                tabButtons.appendChild(button);

                button.addEventListener('click', async () => {
                    document.querySelectorAll('#tab-buttons .tab-button').forEach(b => b.classList.remove('active'));
                    button.classList.add('active');

                    unitTestsViewed.add(index);
                    checkFinalUnlock();

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
                            passed = String(actualOutput).trim() === String(expected).trim();
                        }
                    } catch (err) {
                        errorMsg = err.toString();
                    }

                    const outputWindow = document.getElementById('output-window');
                    clearOutputTerminal();
                    const inputsLine = test.inputs && test.inputs.length
                        ? test.inputs.join(', ')
                        : '(none)';
                    if (errorMsg) {
                        outputWindow.innerHTML = `
                            <div>
                                <div class="test-inputs-line"><strong>Inputs →</strong> ${inputsLine}</div>
                                <hr>
                                <span class="output-error">Error:<br>${errorMsg}</span>
                            </div>`;
                    } else {
                        outputWindow.innerHTML = `
                            <div>
                                <div class="test-inputs-line"><strong>Inputs →</strong> ${inputsLine}</div>
                                <hr>
                                <strong>Output:</strong><br><pre>${actualOutput}</pre>
                                <hr>
                                <strong>Test ${index + 1}: ${test.name || ''}</strong><br>
                                Expected: <code>${test.expected_output ?? '""'}</code><br>
                                Result: <span class="output-result">${passed ? 'PASS ✅' : 'FAIL ❌'}</span>
                                ${!passed ? '<span class="output-penalty"> score -2</span>' : ''}
                            </div>`;
                    }
                });
            });

            // All Tests lives in the Final Test panel
            const finalControls = document.getElementById('final-controls');
            finalControls.innerHTML = '';
            const allTestsButton = document.createElement('button');
            allTestsButton.className = 'all-tests-btn';
            allTestsButton.id = 'all-tests-button';
            allTestsButton.textContent = '▶▶ Run All Tests';
            finalControls.appendChild(allTestsButton);

            allTestsButton.addEventListener('click', () => {
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
                        const outputWindow = document.getElementById('output-window');
                        if (outputWindow) { clearOutputTerminal(); outputWindow.innerHTML = renderFeedback(data); }
                        if (window._updateStyleScore) window._updateStyleScore(currentTab, data.score, data.feedback);
                        if (window._autoSave) window._autoSave();
                        // Reveal all style tabs once Structured scores 8+
                        if (currentTab === firstStyleKey && typeof data.score === 'number' && data.score >= 8) {
                            showStyleTabs();
                            const nudge = document.createElement('div');
                            nudge.className = 'fb-nudge';
                            nudge.textContent = '🎉 All six style tabs are now unlocked — pick your next style and keep going!';
                            const ow = document.getElementById('output-window');
                            if (ow) ow.appendChild(nudge);
                        }
                    })
                    .catch(err => {
                        const outputWindow = document.getElementById('output-window');
                        if (outputWindow) outputWindow.textContent = 'Error running tests: ' + err;
                    });
            });
        })
        .catch(err => console.error('Error loading test cases:', err));
}

// ── Feedback renderer ────────────────────────────────────────────────────────

function renderFeedback(data) {
    const score = typeof data.score === 'number' ? data.score : null;
    const detail = data.feedback_detail;

    if (!detail) {
        return score !== null ? `<div><strong>Score: ${score}/10</strong></div>` : '<div>No results.</div>';
    }

    const { passed, total, tests, style_messages } = detail;
    const failed = total - passed;
    const allPassed = failed === 0;
    const nonePassed = passed === 0;

    let html = '<div class="fb-block">';

    // ── Summary line ──
    if (allPassed) {
        html += `<div class="fb-summary fb-pass">✅ All ${total} test${total !== 1 ? 's' : ''} passed — nice work!</div>`;
    } else if (nonePassed) {
        html += `<div class="fb-summary fb-fail">❌ No tests passed yet — but let's figure out why.</div>`;
    } else {
        html += `<div class="fb-summary fb-partial">⚠️ ${passed} of ${total} tests passed — you're nearly there!</div>`;
    }

    // ── Per-test rows ──
    html += '<div class="fb-tests">';
    tests.forEach((t, idx) => {
        const icon = t.passed ? '✅' : '❌';
        const label = t.name ? `Test ${idx + 1} — ${t.name}` : `Test ${idx + 1}`;
        html += `<div class="fb-test ${t.passed ? 'fb-test-pass' : 'fb-test-fail'}">`;
        html += `<span class="fb-test-icon">${icon}</span> <strong>${label}</strong>`;
        if (!t.passed) {
            html += ` <span class="fb-deduction">−2 pts</span>`;
            if (t.error) {
                html += `<br><span class="fb-hint">Error: ${t.error}</span>`;
            } else {
                const actual = t.actual == null || t.actual === '' ? '""' : t.actual;
                const expected = t.expected == null || t.expected === '' ? '""' : t.expected;
                html += `<br><span class="fb-hint">Expected <code>${expected}</code>, got <code>${actual}</code></span>`;
            }
        }
        html += '</div>';
    });
    html += '</div>';

    // ── Style feedback ──
    if (style_messages && style_messages.length) {
        html += '<hr class="fb-divider"><div class="fb-style">';
        html += '<div class="fb-style-label">Style</div>';
        style_messages.forEach(msg => {
            html += `<div class="fb-style-msg">💡 ${msg}</div>`;
        });
        html += '</div>';
    } else if (allPassed) {
        html += '<hr class="fb-divider"><div class="fb-style"><div class="fb-style-label">Style</div>';
        html += '<div class="fb-style-msg fb-style-ok">✔ No style issues detected.</div></div>';
    }

    // ── Score line ──
    if (score !== null) {
        html += '<hr class="fb-divider">';
        if (allPassed && !style_messages?.length) {
            html += `<div class="fb-score fb-score-full"><strong>Score: ${score}/10</strong> — ready to try the next style?</div>`;
        } else if (nonePassed) {
            html += `<div class="fb-score fb-score-zero"><strong>Score: ${score}/10</strong> — don't worry, have another look and try again.</div>`;
        } else {
            html += `<div class="fb-score"><strong>Score: ${score}/10</strong></div>`;
        }
        // ── Style unlock message (only shown when not yet unlocking, i.e. score < 8) ──
        if (score < 8) {
            html += `<div class="fb-unlock fb-unlock-no">💪 Nearly there — aim for 8/10 or above before moving on to other styles.</div>`;
        }
    }

    html += '</div>';
    return html;
}

// ── Skulpt / Try It ──────────────────────────────────────────────────────────

function clearOutputTerminal() {
    document.getElementById('output-window').classList.remove('skulpt-terminal');
}

function runWithSkulpt(code, headerMsg) {
    const outputWindow = document.getElementById('output-window');
    outputWindow.innerHTML = '';
    outputWindow.classList.add('skulpt-terminal');
    if (headerMsg) {
        const hdr = document.createElement('div');
        hdr.className = 'skulkt-header';
        hdr.textContent = headerMsg;
        outputWindow.appendChild(hdr);
    }

    let currentPre = document.createElement('pre');
    currentPre.className = 'skulpt-out';
    outputWindow.appendChild(currentPre);

    function outf(text) {
        currentPre.textContent += text;
        outputWindow.scrollTop = outputWindow.scrollHeight;
    }

    function inputfun(prompt) {
        return new Promise((resolve) => {
            // Append prompt text to current output block
            currentPre.textContent += prompt;

            // Create interactive input line
            const line = document.createElement('div');
            line.className = 'skulpt-input-line';
            const inp = document.createElement('input');
            inp.type = 'text';
            inp.className = 'skulpt-input';
            inp.setAttribute('autocomplete', 'off');
            line.appendChild(inp);
            outputWindow.appendChild(line);

            // New pre for output after this input
            currentPre = document.createElement('pre');
            currentPre.className = 'skulpt-out';
            outputWindow.appendChild(currentPre);

            outputWindow.scrollTop = outputWindow.scrollHeight;
            inp.focus();

            inp.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    const val = inp.value;
                    // Replace input widget with plain echoed text
                    const echo = document.createElement('span');
                    echo.className = 'skulpt-echo';
                    echo.textContent = val + '\n';
                    line.replaceWith(echo);
                    // Move echo before the new currentPre
                    outputWindow.insertBefore(echo, currentPre);
                    resolve(val);
                }
            });
        });
    }

    Sk.configure({
        output: outf,
        read: (filename) => {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles.files[filename] === undefined)
                throw new Error(`File not found: '${filename}'`);
            return Sk.builtinFiles.files[filename];
        },
        inputfun: inputfun,
        inputfunTakesPrompt: true,
    });

    return Sk.misceval.asyncToPromise(() =>
        Sk.importMainWithBody('<stdin>', false, code, true)
    ).then(() => {
        const done = document.createElement('div');
        done.className = 'skulpt-done';
        done.textContent = '[Program finished]';
        outputWindow.appendChild(done);
        outputWindow.scrollTop = outputWindow.scrollHeight;
    }).catch((err) => {
        const errEl = document.createElement('div');
        errEl.className = 'skulpt-error';
        errEl.textContent = err.toString();
        outputWindow.appendChild(errEl);
        outputWindow.scrollTop = outputWindow.scrollHeight;
    });
}

