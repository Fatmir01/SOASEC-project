"""
Generate ge_qa_eval_helper.html — a self-contained, single-file UI
for the manual inference workflow on FineTuneDB.
 
Aesthetic: editorial / research-paper. Deep ink on warm off-white, single
amber accent. Display serif (Cormorant Garamond) + body sans (IBM Plex Sans)
+ monospace (IBM Plex Mono). The copy actions are the visual centre of the page.
"""
import json
import html as htmllib
 
FACT = [json.loads(l) for l in open('./benchmark/task_pool/ge_qa/ge_qa_factoid.jsonl', encoding='utf-8')]
BOOL = [json.loads(l) for l in open('./benchmark/task_pool/ge_qa/ge_qa_bool.jsonl', encoding='utf-8')]
 
SYSTEM_PROMPT = (
    "You are an expert assistant on the EU Gender Equality Strategy 2020-2025. "
    "Answer questions about the strategy's policy objectives, instruments, and "
    "concrete examples of compliance accurately and concisely, grounded in the "
    "Strategy's text and its illustrative legends."
)
 
# Embed JSONL as JS arrays. JSON is valid JS, so json.dumps works directly.
fact_js = json.dumps(FACT, ensure_ascii=False)
bool_js = json.dumps(BOOL, ensure_ascii=False)
sys_js  = json.dumps(SYSTEM_PROMPT, ensure_ascii=False)
 
# Pillars present in the data
pillars_fact = sorted({it['pillar'] for it in FACT})
pillars_bool = sorted({it['pillar'] for it in BOOL})
 
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GE-QA Eval Helper · GenderEqGLUE</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --paper:    #f5f1e8;
  --paper-2:  #ede7d7;
  --paper-3:  #e2dac4;
  --ink:      #1a1612;
  --ink-soft: #4a3f33;
  --ink-mute: #8a7d6b;
  --rule:     #cabe9f;
  --accent:   #8a3024;          /* oxblood */
  --accent-2: #b8742d;          /* amber */
  --ok:       #2f6b3e;
  --shadow:   0 1px 0 rgba(26,22,18,.04), 0 4px 14px rgba(26,22,18,.06);
}
 
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 400;
  font-size: 15px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  background-image:
    radial-gradient(circle at 0% 0%, rgba(184,116,45,.04) 0, transparent 40%),
    radial-gradient(circle at 100% 100%, rgba(138,48,36,.03) 0, transparent 40%);
  background-attachment: fixed;
}
 
/* ---------- masthead --------------------------------------------------- */
.masthead {
  border-bottom: 1px solid var(--rule);
  padding: 28px 48px 22px;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 32px;
  flex-wrap: wrap;
}
.masthead .title {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  font-size: 36px;
  letter-spacing: -0.01em;
  line-height: 1;
}
.masthead .title em { font-style: italic; color: var(--accent); font-weight: 500; }
.masthead .strap {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-mute);
}
.masthead .meta {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-mute);
  text-align: right;
}
.masthead .meta b { color: var(--ink); font-weight: 600; }
 
/* ---------- tab switcher ----------------------------------------------- */
.tabbar {
  display: flex;
  gap: 0;
  padding: 0 48px;
  border-bottom: 1px solid var(--rule);
  background: var(--paper-2);
}
.tab {
  padding: 14px 24px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 500;
  font-size: 13px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  background: transparent;
  border: none;
  color: var(--ink-mute);
  cursor: pointer;
  position: relative;
  transition: color .14s;
}
.tab:hover { color: var(--ink); }
.tab.active {
  color: var(--ink);
  background: var(--paper);
}
.tab.active::after {
  content: '';
  position: absolute;
  left: 0; right: 0; bottom: -1px;
  height: 2px;
  background: var(--accent);
}
.tab .count {
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 400;
  font-size: 11px;
  margin-left: 8px;
  color: var(--ink-mute);
}
 
/* ---------- two-column layout ------------------------------------------ */
.workspace {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 0;
  min-height: calc(100vh - 132px);
}
 
/* ---------- side rail -------------------------------------------------- */
.rail {
  border-right: 1px solid var(--rule);
  padding: 28px 28px 28px 48px;
  background: var(--paper);
}
.rail .group {
  margin-bottom: 28px;
}
.rail .group h3 {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink-mute);
  margin-bottom: 10px;
  padding-bottom: 4px;
  border-bottom: 1px solid var(--rule);
}
 
/* nav arrows + counter */
.nav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
.nav button {
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 500;
  font-size: 13px;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  color: var(--ink);
  padding: 10px 12px;
  cursor: pointer;
  transition: all .14s;
  letter-spacing: 0.04em;
}
.nav button:hover:not(:disabled) {
  background: var(--ink);
  color: var(--paper);
  border-color: var(--ink);
}
.nav button:disabled { opacity: .35; cursor: not-allowed; }
 
.counter {
  margin-top: 14px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 28px;
  font-weight: 500;
  line-height: 1;
  color: var(--ink);
}
.counter .of { color: var(--ink-mute); }
.counter .total { font-style: italic; color: var(--accent); }
 
/* jump-to */
.jump {
  display: flex;
  gap: 6px;
  margin-top: 12px;
}
.jump input {
  flex: 1;
  min-width: 0;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  padding: 8px 10px;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  color: var(--ink);
  border-radius: 0;
}
.jump input:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--paper);
}
.jump button {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.12em;
  padding: 8px 10px;
  background: var(--ink);
  color: var(--paper);
  border: 1px solid var(--ink);
  cursor: pointer;
}
.jump button:hover { background: var(--accent); border-color: var(--accent); }
 
/* filters */
.filter {
  margin-top: 6px;
}
.filter label {
  display: block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-mute);
  margin-bottom: 5px;
  margin-top: 10px;
}
.filter select {
  width: 100%;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 13px;
  padding: 7px 10px;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  color: var(--ink);
  border-radius: 0;
}
.filter select:focus { outline: none; border-color: var(--accent); }
 
/* inference settings reminder */
.infsettings {
  background: var(--paper-2);
  border: 1px dashed var(--rule);
  padding: 12px 14px;
  font-size: 12px;
  line-height: 1.5;
}
.infsettings b {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  color: var(--accent);
}
.infsettings .row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 3px 0;
  border-bottom: 1px dotted var(--rule);
}
.infsettings .row:last-child { border-bottom: 0; }
.infsettings .key { color: var(--ink-mute); font-size: 11px; letter-spacing: .04em; }
.infsettings .val { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--ink); }
 
/* keyboard hints */
.kbd {
  font-size: 11px;
  color: var(--ink-mute);
  line-height: 1.7;
}
.kbd kbd {
  display: inline-block;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  border-bottom-width: 2px;
  padding: 1px 6px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  color: var(--ink);
  margin-right: 4px;
}
 
/* ---------- main panel ------------------------------------------------- */
.main {
  padding: 36px 56px 56px;
  max-width: 1100px;
}
 
.itemheader {
  display: flex;
  align-items: baseline;
  gap: 18px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}
.itemheader .id {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--accent);
  background: var(--paper-2);
  padding: 3px 9px;
  border-radius: 0;
  border: 1px solid var(--rule);
}
.itemheader .pid {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  color: var(--ink-soft);
}
.itemheader .pillar,
.itemheader .method,
.itemheader .atype {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  padding: 3px 8px;
  border: 1px solid var(--rule);
  background: var(--paper);
}
.itemheader .pillar { color: var(--ink); }
.itemheader .method.direct_paraphrase { color: var(--ok); border-color: var(--ok); }
.itemheader .method.perturbed_claim   { color: var(--accent); border-color: var(--accent); }
.itemheader .atype.group { color: var(--accent-2); border-color: var(--accent-2); }
 
/* primary copy actions */
.actions {
  margin: 28px 0 32px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.btn-copy {
  border: none;
  background: var(--ink);
  color: var(--paper);
  padding: 22px 24px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  cursor: pointer;
  text-align: left;
  transition: all .15s;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
}
.btn-copy:hover { background: var(--accent); }
.btn-copy:active { transform: translateY(1px); }
.btn-copy .label {
  display: block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.22em;
  color: rgba(245,241,232,.55);
  margin-bottom: 6px;
}
.btn-copy .text {
  display: block;
  font-family: 'Cormorant Garamond', serif;
  font-size: 26px;
  font-weight: 500;
  letter-spacing: -0.01em;
  text-transform: none;
  line-height: 1.1;
}
.btn-copy.copied { background: var(--ok); }
.btn-copy.copied .text::before {
  content: '✓ ';
  font-family: 'IBM Plex Sans', sans-serif;
}
 
/* sections */
.section {
  margin-bottom: 26px;
}
.section h4 {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink-mute);
  margin-bottom: 10px;
  padding-bottom: 4px;
  border-bottom: 1px solid var(--rule);
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.section h4 .extra {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 11px;
  text-transform: none;
  letter-spacing: 0;
  color: var(--ink-mute);
}
 
.context-box {
  background: var(--paper-2);
  border-left: 3px solid var(--ink);
  padding: 18px 22px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--ink-soft);
  white-space: pre-wrap;
  max-height: 260px;
  overflow-y: auto;
  font-feature-settings: "ss01";
}
.context-box.expanded { max-height: none; }
 
.toggle-ctx {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  background: transparent;
  border: 1px solid var(--rule);
  color: var(--ink-mute);
  padding: 3px 9px;
  cursor: pointer;
  transition: all .14s;
}
.toggle-ctx:hover { background: var(--ink); color: var(--paper); border-color: var(--ink); }
 
.question-box {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  line-height: 1.4;
  font-weight: 500;
  color: var(--ink);
  padding: 6px 0;
  font-feature-settings: "lnum";
}
 
.gold-box {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-top: 3px solid var(--accent);
  padding: 14px 18px;
  display: flex;
  align-items: baseline;
  gap: 14px;
  flex-wrap: wrap;
}
.gold-box .gold {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.01em;
}
.gold-box .gold::before { content: '«'; color: var(--ink-mute); margin-right: 4px; }
.gold-box .gold::after  { content: '»'; color: var(--ink-mute); margin-left: 4px; }
.gold-box .aliases {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  color: var(--ink-mute);
}
.gold-box .aliases::before {
  content: 'aliases';
  font-size: 9px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-right: 8px;
  color: var(--ink-mute);
  border: 1px solid var(--rule);
  padding: 1px 5px;
}
 
.bool-gold .gold { color: var(--ok); }
.bool-gold[data-answer="no"] .gold { color: var(--accent); }
 
/* preview pane (folded prompt that the COPY button copies) */
.preview {
  margin-top: 12px;
  display: none;
}
.preview.show { display: block; }
.preview pre {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  line-height: 1.55;
  background: var(--paper-2);
  border: 1px solid var(--rule);
  color: var(--ink-soft);
  padding: 14px 16px;
  white-space: pre-wrap;
  max-height: 220px;
  overflow-y: auto;
}
 
.peek-toggles {
  display: flex;
  gap: 12px;
  margin-top: 14px;
}
.peek-toggle {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  background: transparent;
  border: 1px solid var(--rule);
  color: var(--ink-mute);
  padding: 5px 10px;
  cursor: pointer;
}
.peek-toggle.active, .peek-toggle:hover {
  background: var(--ink); color: var(--paper); border-color: var(--ink);
}
 
/* footer */
.footer {
  border-top: 1px solid var(--rule);
  padding: 18px 48px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  color: var(--ink-mute);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
 
/* responsive */
@media (max-width: 900px) {
  .workspace { grid-template-columns: 1fr; }
  .rail { border-right: 0; border-bottom: 1px solid var(--rule); padding: 24px 24px 16px; }
  .main { padding: 24px; }
  .masthead { padding: 20px 24px 14px; }
  .tabbar { padding: 0 24px; }
  .footer { padding: 14px 24px; }
  .actions { grid-template-columns: 1fr; }
}
 
/* tiny separator dots */
.sep { color: var(--rule); margin: 0 8px; }
 
/* hidden helper textarea (for copy fallback) */
#copyhelper { position: fixed; left: -9999px; top: -9999px; }
</style>
</head>
<body>
<header class="masthead">
  <div>
    <div class="strap">GenderEqGLUE · Task 3 · §6.6</div>
    <h1 class="title">GE-QA <em>Eval Helper</em></h1>
  </div>
  <div class="meta">
    <div>FineTuneDB Manual Inference</div>
    <div><b id="m-fact">__FACT_N__</b> factoid <span class="sep">·</span> <b id="m-bool">__BOOL_N__</b> bool</div>
  </div>
</header>
 
<nav class="tabbar">
  <button class="tab active" data-task="factoid">GE-QA-Factoid <span class="count">__FACT_N__</span></button>
  <button class="tab" data-task="bool">GE-QA-Bool <span class="count">__BOOL_N__</span></button>
</nav>
 
<div class="workspace">
  <aside class="rail">
    <div class="group">
      <h3>Navigation</h3>
      <div class="nav">
        <button id="prev-btn" title="Previous (←)">◀  PREV</button>
        <button id="next-btn" title="Next (→)">NEXT  ▶</button>
      </div>
      <div class="counter">
        <span id="cur-idx">1</span><span class="of"> / </span><span class="total" id="cur-total">0</span>
      </div>
      <div class="jump">
        <input type="text" id="jump-input" placeholder="ge_qa_f_001 or 1" autocomplete="off">
        <button id="jump-btn">GO</button>
      </div>
    </div>
 
    <div class="group">
      <h3>Filter</h3>
      <div class="filter">
        <label for="pillar-filter">Pillar</label>
        <select id="pillar-filter"><option value="">— all pillars —</option></select>
        <label for="method-filter" id="method-filter-label" style="display:none">Construction</label>
        <select id="method-filter" style="display:none">
          <option value="">— both methods —</option>
          <option value="direct_paraphrase">direct_paraphrase</option>
          <option value="perturbed_claim">perturbed_claim</option>
        </select>
        <label for="atype-filter" id="atype-filter-label">Answer type</label>
        <select id="atype-filter">
          <option value="">— both types —</option>
          <option value="single_span">single_span</option>
          <option value="group">group</option>
        </select>
      </div>
    </div>
 
    <div class="group">
      <h3>Inference Settings</h3>
      <div class="infsettings">
        <div class="row"><span class="key">temperature</span><span class="val">0</span></div>
        <div class="row"><span class="key">max_tokens</span><span class="val" id="mt-val">60</span></div>
        <div class="row"><span class="key">model</span><span class="val">×3</span></div>
        <div style="margin-top:10px;font-size:11px;color:var(--ink-mute);line-height:1.5;">
          Run base, tuned-legends, tuned-regulation under the <b>same</b> system prompt for each item.
        </div>
      </div>
    </div>
 
    <div class="group">
      <h3>Keyboard</h3>
      <div class="kbd">
        <kbd>←</kbd><kbd>→</kbd> navigate<br>
        <kbd>S</kbd> copy system<br>
        <kbd>U</kbd> copy user<br>
        <kbd>P</kbd> peek user prompt<br>
        <kbd>C</kbd> toggle context
      </div>
    </div>
  </aside>
 
  <main class="main">
    <div class="itemheader" id="item-header"></div>
 
    <div class="actions">
      <button class="btn-copy" id="copy-system" title="Copy system prompt (S)">
        <span class="label">SYSTEM PROMPT · §5.1</span>
        <span class="text">Copy system</span>
      </button>
      <button class="btn-copy" id="copy-user" title="Copy user prompt (U)">
        <span class="label">USER PROMPT · §6.6.4</span>
        <span class="text">Copy user</span>
      </button>
    </div>
 
    <div class="peek-toggles">
      <button class="peek-toggle" id="peek-system">peek system</button>
      <button class="peek-toggle" id="peek-user">peek user</button>
    </div>
    <div class="preview" id="preview-system"><pre id="preview-system-text"></pre></div>
    <div class="preview" id="preview-user"><pre id="preview-user-text"></pre></div>
 
    <div class="section">
      <h4>
        <span>Question</span>
        <span class="extra" id="q-extra"></span>
      </h4>
      <div class="question-box" id="question-text"></div>
    </div>
 
    <div class="section">
      <h4>
        <span>Gold Answer</span>
        <span class="extra" id="gold-extra"></span>
      </h4>
      <div class="gold-box" id="gold-box"></div>
    </div>
 
    <div class="section">
      <h4>
        <span>Context · <span id="ctx-pid" style="text-transform:none;letter-spacing:0;color:var(--ink);font-family:'IBM Plex Mono',monospace;font-size:11px;"></span></span>
        <button class="toggle-ctx" id="toggle-ctx">expand · C</button>
      </h4>
      <div class="context-box" id="context-text"></div>
    </div>
  </main>
</div>
 
<footer class="footer">
  <div>GE-QA score = (factoid_F1 + bool_accuracy_all) / 2 &nbsp;·&nbsp; SQuAD normalisation per §6.6.5</div>
  <div id="footer-active">factoid · 1 / 0</div>
</footer>
 
<textarea id="copyhelper"></textarea>
 
<script>
// ====== Embedded data =====================================================
const SYSTEM_PROMPT = __SYSTEM_JSON__;
const FACTOID = __FACTOID_JSON__;
const BOOLQ   = __BOOLQ_JSON__;
 
// User-prompt templates from §6.6.4
const FACTOID_USER_TPL = `Read the following passage from an EU regulatory document and answer the question.
 
PASSAGE:
{context}
 
QUESTION:
{question}
 
Answer with the shortest exact phrase from the passage that answers the question. Do not add explanations.`;
 
const BOOL_USER_TPL = `Read the following passage from an EU regulatory document and answer the question.
 
PASSAGE:
{context}
 
QUESTION:
{question}
 
Answer with exactly one word: yes or no.`;
 
function buildUserPrompt(task, item) {
  const tpl = task === 'factoid' ? FACTOID_USER_TPL : BOOL_USER_TPL;
  return tpl.replace('{context}', item.context).replace('{question}', item.question);
}
 
// ====== State =============================================================
const state = {
  task: 'factoid',     // 'factoid' | 'bool'
  filtered: [],        // current visible list
  cursor: 0,           // index into filtered
  filters: { pillar: '', method: '', atype: '' },
};
 
function activeData() { return state.task === 'factoid' ? FACTOID : BOOLQ; }
 
function applyFilters() {
  const data = activeData();
  state.filtered = data.filter(it => {
    if (state.filters.pillar && it.pillar !== state.filters.pillar) return false;
    if (state.task === 'bool' && state.filters.method && it.construction_method !== state.filters.method) return false;
    if (state.task === 'factoid' && state.filters.atype && it.answer_type !== state.filters.atype) return false;
    return true;
  });
  if (state.cursor >= state.filtered.length) state.cursor = 0;
  if (state.filtered.length === 0) state.cursor = -1;
  render();
}
 
function setTask(task) {
  state.task = task;
  state.cursor = 0;
  state.filters = { pillar: '', method: '', atype: '' };
 
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.task === task));
  document.getElementById('mt-val').textContent = (task === 'factoid' ? '60' : '5');
 
  // populate pillar filter from data
  const pillars = [...new Set(activeData().map(it => it.pillar))].sort();
  const pf = document.getElementById('pillar-filter');
  pf.innerHTML = '<option value="">— all pillars —</option>' +
    pillars.map(p => `<option value="${p}">${p}</option>`).join('');
  pf.value = '';
 
  // toggle method-filter visibility (bool only) and atype-filter (factoid only)
  document.getElementById('method-filter').style.display       = (task === 'bool')    ? '' : 'none';
  document.getElementById('method-filter-label').style.display = (task === 'bool')    ? '' : 'none';
  document.getElementById('atype-filter').style.display        = (task === 'factoid') ? '' : 'none';
  document.getElementById('atype-filter-label').style.display  = (task === 'factoid') ? '' : 'none';
  document.getElementById('method-filter').value = '';
  document.getElementById('atype-filter').value  = '';
 
  applyFilters();
}
 
// ====== Rendering =========================================================
function escape(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c]));
}
 
function render() {
  const empty = state.cursor < 0 || state.filtered.length === 0;
  const ih = document.getElementById('item-header');
  document.getElementById('cur-total').textContent = state.filtered.length;
  document.getElementById('cur-idx').textContent = empty ? '0' : (state.cursor + 1);
  document.getElementById('footer-active').textContent =
    `${state.task} · ${empty ? 0 : (state.cursor+1)} / ${state.filtered.length}`;
 
  if (empty) {
    ih.innerHTML = '<span class="pid">No items match the active filters.</span>';
    ['question-text','gold-box','context-text','preview-system-text','preview-user-text']
      .forEach(id => document.getElementById(id).textContent = '');
    document.getElementById('q-extra').textContent = '';
    document.getElementById('gold-extra').textContent = '';
    document.getElementById('ctx-pid').textContent = '';
    document.getElementById('prev-btn').disabled = true;
    document.getElementById('next-btn').disabled = true;
    return;
  }
 
  const item = state.filtered[state.cursor];
 
  // header chips
  let chips = `<span class="id">${escape(item.id)}</span>`
            + `<span class="pid">${escape(item.passage_id)}</span>`
            + `<span class="pillar">${escape(item.pillar)}</span>`;
  if (state.task === 'factoid') {
    chips += `<span class="atype ${escape(item.answer_type)}">${escape(item.answer_type)}</span>`;
  } else {
    chips += `<span class="method ${escape(item.construction_method)}">${escape(item.construction_method)}</span>`;
  }
  ih.innerHTML = chips;
 
  // question
  document.getElementById('question-text').textContent = item.question;
  const qWords = item.question.trim().split(/\s+/).length;
  document.getElementById('q-extra').textContent = `${qWords} words`;
 
  // gold answer
  const gb = document.getElementById('gold-box');
  if (state.task === 'factoid') {
    gb.classList.remove('bool-gold');
    gb.removeAttribute('data-answer');
    let html = `<span class="gold">${escape(item.answer)}</span>`;
    const aliases = (item.answer_aliases || []).filter(Boolean);
    if (aliases.length) {
      html += `<span class="aliases">${aliases.map(a => escape(a)).join(' · ')}</span>`;
    }
    gb.innerHTML = html;
    document.getElementById('gold-extra').textContent =
      `${item.answer.split(/\s+/).length} words` +
      (aliases.length ? ` · ${aliases.length} alias${aliases.length>1?'es':''}` : '');
  } else {
    gb.classList.add('bool-gold');
    gb.setAttribute('data-answer', item.answer);
    gb.innerHTML = `<span class="gold">${escape(item.answer)}</span>`;
    document.getElementById('gold-extra').textContent = item.construction_method;
  }
 
  // context
  document.getElementById('context-text').textContent = item.context;
  document.getElementById('ctx-pid').textContent = item.passage_id;
 
  // peek panes
  document.getElementById('preview-system-text').textContent = SYSTEM_PROMPT;
  document.getElementById('preview-user-text').textContent   = buildUserPrompt(state.task, item);
 
  // nav button states
  document.getElementById('prev-btn').disabled = (state.cursor <= 0);
  document.getElementById('next-btn').disabled = (state.cursor >= state.filtered.length - 1);
}
 
// ====== Copy actions ======================================================
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (_e) {
    // fallback for clipboards locked down without https
    const ta = document.getElementById('copyhelper');
    ta.value = text;
    ta.select();
    try {
      document.execCommand('copy');
      return true;
    } catch (_e2) { return false; }
  }
}
 
async function flashCopied(btn) {
  btn.classList.add('copied');
  setTimeout(() => btn.classList.remove('copied'), 1200);
}
 
document.getElementById('copy-system').addEventListener('click', async () => {
  const ok = await copyToClipboard(SYSTEM_PROMPT);
  if (ok) flashCopied(document.getElementById('copy-system'));
});
 
document.getElementById('copy-user').addEventListener('click', async () => {
  if (state.cursor < 0) return;
  const item = state.filtered[state.cursor];
  const text = buildUserPrompt(state.task, item);
  const ok = await copyToClipboard(text);
  if (ok) flashCopied(document.getElementById('copy-user'));
});
 
// ====== Navigation ========================================================
document.getElementById('prev-btn').addEventListener('click', () => {
  if (state.cursor > 0) { state.cursor--; render(); }
});
document.getElementById('next-btn').addEventListener('click', () => {
  if (state.cursor < state.filtered.length - 1) { state.cursor++; render(); }
});
 
document.getElementById('jump-btn').addEventListener('click', jumpToInput);
document.getElementById('jump-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') jumpToInput();
});
function jumpToInput() {
  const raw = document.getElementById('jump-input').value.trim();
  if (!raw) return;
  // accept either "ge_qa_f_042" or a 1-based index
  let idx = state.filtered.findIndex(it => it.id === raw);
  if (idx < 0) {
    const n = parseInt(raw, 10);
    if (!isNaN(n) && n >= 1 && n <= state.filtered.length) idx = n - 1;
  }
  if (idx >= 0) {
    state.cursor = idx;
    render();
    document.getElementById('jump-input').value = '';
  } else {
    document.getElementById('jump-input').style.borderColor = 'var(--accent)';
    setTimeout(() => document.getElementById('jump-input').style.borderColor = '', 600);
  }
}
 
// ====== Tab + filter wiring ==============================================
document.querySelectorAll('.tab').forEach(t => {
  t.addEventListener('click', () => setTask(t.dataset.task));
});
document.getElementById('pillar-filter').addEventListener('change', e => {
  state.filters.pillar = e.target.value; state.cursor = 0; applyFilters();
});
document.getElementById('method-filter').addEventListener('change', e => {
  state.filters.method = e.target.value; state.cursor = 0; applyFilters();
});
document.getElementById('atype-filter').addEventListener('change', e => {
  state.filters.atype = e.target.value; state.cursor = 0; applyFilters();
});
 
// context expand toggle
document.getElementById('toggle-ctx').addEventListener('click', () => {
  const box = document.getElementById('context-text');
  const btn = document.getElementById('toggle-ctx');
  box.classList.toggle('expanded');
  btn.textContent = box.classList.contains('expanded') ? 'collapse · C' : 'expand · C';
});
 
// peek toggles
document.getElementById('peek-system').addEventListener('click', () => {
  const p = document.getElementById('preview-system');
  const t = document.getElementById('peek-system');
  p.classList.toggle('show'); t.classList.toggle('active');
});
document.getElementById('peek-user').addEventListener('click', () => {
  const p = document.getElementById('preview-user');
  const t = document.getElementById('peek-user');
  p.classList.toggle('show'); t.classList.toggle('active');
});
 
// keyboard shortcuts
document.addEventListener('keydown', e => {
  // ignore when typing in input/textarea
  const tag = (e.target.tagName || '').toLowerCase();
  if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
  if (e.key === 'ArrowLeft')  { document.getElementById('prev-btn').click(); }
  else if (e.key === 'ArrowRight') { document.getElementById('next-btn').click(); }
  else if (e.key === 's' || e.key === 'S') { document.getElementById('copy-system').click(); }
  else if (e.key === 'u' || e.key === 'U') { document.getElementById('copy-user').click(); }
  else if (e.key === 'p' || e.key === 'P') { document.getElementById('peek-user').click(); }
  else if (e.key === 'c' || e.key === 'C') { document.getElementById('toggle-ctx').click(); }
});
 
// boot
setTask('factoid');
</script>
</body>
</html>
"""
 
# ----- substitute placeholders ----------------------------------------
out = (HTML_TEMPLATE
       .replace('__FACTOID_JSON__', fact_js)
       .replace('__BOOLQ_JSON__', bool_js)
       .replace('__SYSTEM_JSON__', sys_js)
       .replace('__FACT_N__', str(len(FACT)))
       .replace('__BOOL_N__', str(len(BOOL))))
 
out_path = './benchmark/task_pool/ge_qa/ge_qa_eval_helper.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(out)
 
# size sanity
import os
size_kb = os.path.getsize(out_path) / 1024
print(f"Wrote {out_path}: {size_kb:.1f} KB ({len(FACT)} factoid + {len(BOOL)} bool)")