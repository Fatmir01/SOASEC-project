
# Build the GE-STANCE HTML console + CSV template.
import json

with open("./benchmark/task_pool/ge-stance/ge_stance.jsonl") as f:
    records = [json.loads(line) for line in f]

print(f"Loaded {len(records)} records")

SYSTEM_PROMPT = (
    "You are a careful stance classifier. For each statement, determine "
    "whether the position it expresses is supportive of, neutral toward, or "
    "against gender equality as articulated in the EU Gender Equality "
    "Strategy 2020-2025. Respond with only one of these three exact labels "
    "in lowercase\u2014supportive, neutral, or against\u2014and nothing else. "
    "Do not add explanations, articles, punctuation, or quotation marks."
)

# JSON-safe embedding
data_js = json.dumps(records, ensure_ascii=False)
sys_js = json.dumps(SYSTEM_PROMPT)

html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>GE-STANCE Prompt Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,700;9..144,900&family=Inter+Tight:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
<style>
  :root {
    --paper: #eef0e9;            /* cooler cream — distinguishes from GE-WSC */
    --paper-2: #e2e7dc;
    --rule: #c8d0bf;
    --ink: #16201a;
    --ink-soft: #3e4a42;
    --ink-faint: #7a857d;
    --accent: #1f5d4a;            /* deep forest teal */
    --accent-soft: #5e9882;
    --gold-tag: #6c5a1f;
    --supportive: #1f5d4a;
    --neutral: #5d5a3a;
    --against: #8a3a2a;
    --shadow: 0 1px 0 rgba(22,32,26,.04), 0 6px 22px -12px rgba(22,32,26,.18);
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: "Inter Tight", system-ui, sans-serif;
    background: var(--paper);
    color: var(--ink);
    -webkit-font-smoothing: antialiased;
    background-image:
      radial-gradient(circle at 12% 8%, rgba(31,93,74,.05), transparent 40%),
      radial-gradient(circle at 92% 92%, rgba(31,93,74,.05), transparent 40%);
    min-height: 100vh;
  }

  .grain {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    opacity: .35; mix-blend-mode: multiply;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.10 0 0 0 0 0.11 0 0 0 0 0.10 0 0 0 0.18 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
  }

  .wrap {
    position: relative; z-index: 1;
    max-width: 1180px; margin: 0 auto; padding: 36px 28px 80px;
  }

  /* Header */
  header.masthead {
    border-top: 2px solid var(--ink);
    border-bottom: 1px solid var(--ink);
    padding: 14px 0 10px;
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 24px; flex-wrap: wrap;
  }
  .masthead .brand {
    font-family: "Fraunces", serif;
    font-weight: 900;
    font-size: clamp(28px, 4.2vw, 46px);
    letter-spacing: -.015em;
    line-height: .95;
  }
  .masthead .brand em { color: var(--accent); font-style: italic; font-weight: 400; }
  .masthead .meta {
    font-family: "JetBrains Mono", monospace;
    font-size: 11px; letter-spacing: .14em; text-transform: uppercase;
    color: var(--ink-faint);
    display: flex; gap: 18px; flex-wrap: wrap;
  }
  .masthead .meta b { color: var(--ink); font-weight: 700; }

  .deck {
    font-family: "Fraunces", serif;
    font-style: italic; font-weight: 400;
    font-size: 15px; color: var(--ink-soft);
    margin: 14px 0 28px;
    border-bottom: 1px dashed var(--rule);
    padding-bottom: 18px;
    max-width: 760px;
  }

  /* Cards */
  .card {
    background: #f7f9f3;
    border: 1px solid var(--rule);
    box-shadow: var(--shadow);
    border-radius: 4px;
  }
  .card .card-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 18px; border-bottom: 1px solid var(--rule);
    gap: 16px; flex-wrap: wrap;
  }
  .card .card-head h2 {
    margin: 0; font-family: "Fraunces", serif; font-weight: 700;
    font-size: 18px; letter-spacing: -.005em;
  }
  .card .card-head .label {
    font-family: "JetBrains Mono", monospace; font-size: 10px;
    letter-spacing: .2em; text-transform: uppercase; color: var(--ink-faint);
  }

  /* System prompt card */
  .system-card { margin-bottom: 26px; }
  .system-card .body { padding: 16px 18px; }
  pre.prompt {
    font-family: "JetBrains Mono", monospace;
    font-size: 13px; line-height: 1.55;
    background: var(--paper-2);
    border: 1px solid var(--rule);
    border-radius: 3px;
    padding: 14px 16px; margin: 0;
    white-space: pre-wrap; word-wrap: break-word;
    color: var(--ink);
    max-height: 280px; overflow: auto;
  }

  /* Navigator */
  .navbar {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center; gap: 16px;
    padding: 12px 16px;
    background: var(--ink); color: var(--paper);
    border-radius: 4px;
    margin-bottom: 18px;
  }
  .navbar .counter {
    font-family: "Fraunces", serif; font-size: 22px; font-weight: 700;
    letter-spacing: -.01em;
  }
  .navbar .counter .total { color: rgba(238,240,233,.55); font-weight: 400; }
  .navbar .progress {
    height: 4px; background: rgba(238,240,233,.15); border-radius: 2px;
    overflow: hidden; position: relative;
  }
  .navbar .progress > span {
    position: absolute; inset: 0 auto 0 0;
    background: var(--accent-soft);
    transition: width .25s ease;
  }
  .navbar .progress-label {
    font-family: "JetBrains Mono", monospace; font-size: 10px;
    letter-spacing: .2em; text-transform: uppercase;
    color: rgba(238,240,233,.7); margin-top: 4px;
  }
  .navbar .nav-actions { display: flex; gap: 8px; }

  /* Buttons */
  button.btn {
    font-family: "Inter Tight", system-ui, sans-serif;
    font-size: 13px; font-weight: 600;
    letter-spacing: .02em;
    padding: 8px 14px;
    border: 1px solid var(--ink);
    background: var(--paper);
    color: var(--ink);
    border-radius: 2px;
    cursor: pointer;
    transition: transform .08s ease, background .15s ease, color .15s ease;
  }
  button.btn:hover { background: var(--ink); color: var(--paper); }
  button.btn:active { transform: translateY(1px); }
  button.btn.primary {
    background: var(--accent); border-color: var(--accent); color: #f7f9f3;
  }
  button.btn.primary:hover { background: #143d31; border-color: #143d31; }
  button.btn.ghost-on-dark {
    background: transparent; border-color: rgba(238,240,233,.4);
    color: var(--paper);
  }
  button.btn.ghost-on-dark:hover {
    background: var(--paper); color: var(--ink); border-color: var(--paper);
  }
  button.btn .kbd {
    display: inline-block;
    margin-left: 6px;
    font-family: "JetBrains Mono", monospace;
    font-size: 10px;
    padding: 1px 5px;
    border: 1px solid currentColor;
    border-radius: 2px;
    opacity: .55;
  }

  /* Item layout */
  .item-grid {
    display: grid;
    grid-template-columns: minmax(280px, 360px) 1fr;
    gap: 18px;
  }
  @media (max-width: 820px) {
    .item-grid { grid-template-columns: 1fr; }
  }

  /* Sidebar */
  .sidebar { display: flex; flex-direction: column; gap: 14px; }
  .sidebar .card .body { padding: 14px 16px; }

  .id-line {
    font-family: "JetBrains Mono", monospace;
    font-size: 12px;
    color: var(--ink-soft);
    word-break: break-all;
    margin-bottom: 10px;
  }

  .badge {
    display: inline-block;
    font-family: "JetBrains Mono", monospace;
    font-size: 10px; letter-spacing: .15em; text-transform: uppercase;
    padding: 4px 8px; border-radius: 2px;
    margin: 0 4px 4px 0;
  }
  .badge-supportive { background: rgba(31,93,74,.18); color: var(--supportive); border: 1px solid rgba(31,93,74,.4); }
  .badge-neutral { background: rgba(93,90,58,.15); color: var(--neutral); border: 1px solid rgba(93,90,58,.4); }
  .badge-against { background: rgba(138,58,42,.16); color: var(--against); border: 1px solid rgba(138,58,42,.4); }
  .badge-source { background: var(--paper-2); color: var(--ink-soft); border: 1px solid var(--rule); }
  .badge-pillar { background: transparent; color: var(--ink-faint); border: 1px dashed var(--rule); }
  .badge-done { background: var(--accent); color: #fff; }

  .field { margin-top: 10px; }
  .field .k {
    font-family: "JetBrains Mono", monospace;
    font-size: 10px; letter-spacing: .2em; text-transform: uppercase;
    color: var(--ink-faint); margin-bottom: 3px;
  }
  .field .v {
    font-family: "Fraunces", serif;
    font-size: 17px; line-height: 1.4;
  }
  .gold {
    background: rgba(108, 90, 31, .08);
    border-left: 3px solid var(--gold-tag);
    padding: 8px 12px;
    font-family: "Fraunces", serif;
    font-size: 16px;
    color: var(--ink);
  }
  .gold .marker {
    font-family: "JetBrains Mono", monospace;
    font-size: 9px; letter-spacing: .2em; text-transform: uppercase;
    color: var(--gold-tag); display: block; margin-bottom: 2px;
  }

  /* Class legend */
  .class-legend {
    display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px;
  }
  .legend-chip {
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    padding: 4px 9px;
    border-radius: 2px;
    border: 1px solid var(--rule);
    background: var(--paper-2);
  }
  .legend-chip.supportive { color: var(--supportive); border-color: rgba(31,93,74,.4); }
  .legend-chip.neutral { color: var(--neutral); border-color: rgba(93,90,58,.4); }
  .legend-chip.against { color: var(--against); border-color: rgba(138,58,42,.4); }

  /* Toast */
  .toast {
    position: fixed; bottom: 22px; left: 50%; transform: translateX(-50%);
    background: var(--ink); color: var(--paper);
    padding: 10px 18px; border-radius: 2px;
    font-family: "JetBrains Mono", monospace;
    font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
    opacity: 0; pointer-events: none;
    transition: opacity .2s ease, transform .2s ease;
    z-index: 100;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(-4px); }

  /* Filter strip */
  .filters {
    display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
    margin: 0 0 14px; padding: 10px 14px;
    border: 1px dashed var(--rule); border-radius: 3px;
    font-size: 12px;
  }
  .filters .label {
    font-family: "JetBrains Mono", monospace; font-size: 10px;
    letter-spacing: .2em; text-transform: uppercase; color: var(--ink-faint);
  }
  .filters select, .filters input[type=number] {
    font-family: "JetBrains Mono", monospace;
    font-size: 12px; padding: 4px 8px;
    background: var(--paper-2); border: 1px solid var(--rule);
    border-radius: 2px; color: var(--ink);
  }
  .filters .reset-prog {
    margin-left: auto; font-size: 11px; color: var(--ink-faint);
    background: transparent; border: 0; cursor: pointer; text-decoration: underline;
  }
  .filters .reset-prog:hover { color: var(--accent); }

  /* footer */
  footer.foot {
    margin-top: 40px; padding-top: 18px;
    border-top: 1px solid var(--rule);
    font-family: "JetBrains Mono", monospace;
    font-size: 10px; letter-spacing: .15em;
    text-transform: uppercase; color: var(--ink-faint);
    display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap;
  }
</style>
</head>
<body>
<div class="grain" aria-hidden="true"></div>

<div class="wrap">

  <header class="masthead">
    <div class="brand">GE&middot;STANCE <em>Prompt Console</em></div>
    <div class="meta">
      <span><b>Task</b> 3-class stance</span>
      <span><b>N</b> <span id="n-total">120</span></span>
      <span><b>Source</b> CIVICS + curated</span>
      <span><b>For</b> FineTuneDB</span>
    </div>
  </header>

  <p class="deck">A clipboard companion for manual stance classification on the GE-STANCE evaluation set.
  Copy the standardized system prompt once, then advance through items, copying each formatted user
  prompt into FineTuneDB. Filter by pillar, source, or gold label; track progress.</p>

  <!-- System prompt -->
  <section class="card system-card">
    <div class="card-head">
      <h2>System Prompt</h2>
      <span class="label">Paste once into FineTuneDB &mdash; system field</span>
      <button class="btn primary" id="copy-system">Copy system <span class="kbd">S</span></button>
    </div>
    <div class="body">
      <pre class="prompt" id="system-prompt-text"></pre>
      <div class="class-legend" style="margin-top:10px">
        <span class="legend-chip supportive">supportive</span>
        <span class="legend-chip neutral">neutral</span>
        <span class="legend-chip against">against</span>
      </div>
    </div>
  </section>

  <!-- Filters -->
  <div class="filters">
    <span class="label">Pillar</span>
    <select id="filter-pillar">
      <option value="">All pillars</option>
      <option value="violence_stereotypes">violence_stereotypes</option>
      <option value="equal_economy">equal_economy</option>
      <option value="leadership_participation">leadership_participation</option>
      <option value="mainstreaming_intersectionality">mainstreaming_intersectionality</option>
      <option value="funding_global_action">funding_global_action</option>
      <option value="general_equality">general_equality</option>
    </select>
    <span class="label">Label</span>
    <select id="filter-label">
      <option value="">All labels</option>
      <option value="supportive">supportive</option>
      <option value="neutral">neutral</option>
      <option value="against">against</option>
    </select>
    <span class="label">Source</span>
    <select id="filter-source">
      <option value="">All sources</option>
      <option value="civics_filtered">civics_filtered</option>
      <option value="curated">curated</option>
    </select>
    <span class="label">Jump #</span>
    <input type="number" id="jump" min="1" placeholder="1" style="width: 80px" />
    <button class="reset-prog" id="reset-progress">Reset progress</button>
  </div>

  <!-- Navigator -->
  <div class="navbar">
    <div>
      <div class="counter"><span id="cur-num">1</span><span class="total"> / <span id="tot-num">120</span></span></div>
      <div class="progress-label" id="progress-label">0 of 120 complete</div>
    </div>
    <div>
      <div class="progress"><span id="progress-bar" style="width: 0%"></span></div>
    </div>
    <div class="nav-actions">
      <button class="btn ghost-on-dark" id="prev-btn">&larr; Prev <span class="kbd">&larr;</span></button>
      <button class="btn ghost-on-dark" id="mark-btn">Mark done <span class="kbd">M</span></button>
      <button class="btn ghost-on-dark" id="next-btn">Next &rarr; <span class="kbd">&rarr;</span></button>
    </div>
  </div>

  <!-- Item -->
  <div class="item-grid">
    <aside class="sidebar">
      <section class="card">
        <div class="card-head">
          <h2>Item Metadata</h2>
          <span class="label">Reference only &mdash; do not paste</span>
        </div>
        <div class="body">
          <div class="id-line" id="item-id">&mdash;</div>
          <div id="badges"></div>
          <div class="field">
            <div class="k">Statement</div>
            <div class="v" id="m-statement">&mdash;</div>
          </div>
          <div class="field">
            <div class="k">Gold label</div>
            <div class="gold" id="m-gold">
              <span class="marker">Stance toward gender equality</span>
              <span id="m-gold-text">&mdash;</span>
            </div>
          </div>
        </div>
      </section>
    </aside>

    <section class="card prompt-card">
      <div class="card-head">
        <h2>User Prompt</h2>
        <span class="label">Paste into FineTuneDB &mdash; user field</span>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn primary" id="copy-user">Copy user prompt <span class="kbd">C</span></button>
        </div>
      </div>
      <div class="body">
        <pre class="prompt" id="user-prompt-text"></pre>
      </div>
    </section>
  </div>

  <footer class="foot">
    <span>GE-STANCE Prompt Console &middot; companion to ge_wsc_console.html</span>
    <span>Shortcuts &middot; &larr; / &rarr; nav &middot; C copy user &middot; S copy system &middot; M mark done</span>
  </footer>

</div>

<div class="toast" id="toast">Copied</div>

<script>
  const SYSTEM_PROMPT = __SYSTEM_PROMPT__;
  const ALL_RECORDS = __DATA__;

  document.getElementById("n-total").textContent = ALL_RECORDS.length;
  document.getElementById("jump").max = ALL_RECORDS.length;

  // ---- state ----
  const STORAGE_KEY = "ge_stance_console_v1";
  let state = {
    cursor: 0,
    pillarFilter: "",
    labelFilter: "",
    sourceFilter: "",
    done: {},
  };
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) Object.assign(state, JSON.parse(saved));
  } catch (e) {}

  function persist() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
    catch (e) {}
  }

  function filteredRecords() {
    return ALL_RECORDS.filter(r =>
      (!state.pillarFilter || r.pillar === state.pillarFilter) &&
      (!state.labelFilter  || r.label  === state.labelFilter) &&
      (!state.sourceFilter || r.source === state.sourceFilter)
    );
  }

  function clamp(i, n) { return Math.max(0, Math.min(n - 1, i)); }

  // ---- prompt builder ----
  function buildUserPrompt(rec) {
    return [
      "Statement: " + rec.statement,
      "",
      "Classify the stance toward gender equality.",
      "Respond with exactly one of: supportive, neutral, against.",
      "",
      "Stance:"
    ].join("\n");
  }

  // ---- DOM refs ----
  const $ = id => document.getElementById(id);
  const sysText = $("system-prompt-text");
  const userText = $("user-prompt-text");
  const itemId = $("item-id");
  const badges = $("badges");
  const mStmt = $("m-statement");
  const mGold = $("m-gold-text");
  const cur = $("cur-num");
  const tot = $("tot-num");
  const progBar = $("progress-bar");
  const progLabel = $("progress-label");
  const filterPillar = $("filter-pillar");
  const filterLabel = $("filter-label");
  const filterSource = $("filter-source");
  const jumpInp = $("jump");

  // ---- render ----
  function render() {
    sysText.textContent = SYSTEM_PROMPT;
    const list = filteredRecords();
    state.cursor = clamp(state.cursor, list.length);
    const rec = list[state.cursor];
    if (!rec) {
      userText.textContent = "(no records match the current filter combination)";
      itemId.textContent = "—";
      badges.innerHTML = "";
      mStmt.textContent = mGold.textContent = "—";
      cur.textContent = "0";
      tot.textContent = "0";
      return;
    }
    cur.textContent = String(state.cursor + 1);
    tot.textContent = String(list.length);
    itemId.textContent = rec.id;

    const b = [];
    b.push(`<span class="badge badge-${rec.label}">${rec.label}</span>`);
    b.push(`<span class="badge badge-source">${rec.source}</span>`);
    b.push(`<span class="badge badge-pillar">${rec.pillar}</span>`);
    if (state.done[rec.id]) {
      b.push(`<span class="badge badge-done">done</span>`);
    }
    badges.innerHTML = b.join("");

    mStmt.textContent = rec.statement;
    mGold.textContent = rec.label;

    userText.textContent = buildUserPrompt(rec);

    const doneCount = ALL_RECORDS.reduce((n, r) => n + (state.done[r.id] ? 1 : 0), 0);
    const pct = (doneCount / ALL_RECORDS.length) * 100;
    progBar.style.width = pct + "%";
    progLabel.textContent = `${doneCount} of ${ALL_RECORDS.length} complete`;

    filterPillar.value = state.pillarFilter;
    filterLabel.value = state.labelFilter;
    filterSource.value = state.sourceFilter;
  }

  // ---- copy ----
  async function copyText(text, label) {
    try {
      await navigator.clipboard.writeText(text);
      showToast(label + " copied");
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta);
      ta.select(); document.execCommand("copy");
      document.body.removeChild(ta);
      showToast(label + " copied");
    }
  }

  let toastTimer;
  function showToast(msg) {
    const t = $("toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove("show"), 1400);
  }

  // ---- nav ----
  function move(delta) {
    const list = filteredRecords();
    if (!list.length) return;
    state.cursor = (state.cursor + delta + list.length) % list.length;
    persist(); render();
  }
  function setCursor(i) {
    const list = filteredRecords();
    state.cursor = clamp(i, list.length);
    persist(); render();
  }
  function toggleDone() {
    const list = filteredRecords();
    const rec = list[state.cursor];
    if (!rec) return;
    state.done[rec.id] = !state.done[rec.id];
    if (!state.done[rec.id]) delete state.done[rec.id];
    persist(); render();
  }

  // ---- listeners ----
  $("copy-system").addEventListener("click", () => copyText(SYSTEM_PROMPT, "System prompt"));
  $("copy-user").addEventListener("click", () => {
    const list = filteredRecords();
    const rec = list[state.cursor];
    if (!rec) return;
    copyText(buildUserPrompt(rec), "Item " + (state.cursor + 1));
  });
  $("prev-btn").addEventListener("click", () => move(-1));
  $("next-btn").addEventListener("click", () => move(1));
  $("mark-btn").addEventListener("click", toggleDone);
  filterPillar.addEventListener("change", () => {
    state.pillarFilter = filterPillar.value;
    state.cursor = 0; persist(); render();
  });
  filterLabel.addEventListener("change", () => {
    state.labelFilter = filterLabel.value;
    state.cursor = 0; persist(); render();
  });
  filterSource.addEventListener("change", () => {
    state.sourceFilter = filterSource.value;
    state.cursor = 0; persist(); render();
  });
  jumpInp.addEventListener("change", () => {
    const v = parseInt(jumpInp.value, 10);
    if (!isNaN(v)) setCursor(v - 1);
  });
  $("reset-progress").addEventListener("click", () => {
    if (confirm("Reset all progress markers?")) {
      state.done = {}; persist(); render();
    }
  });

  document.addEventListener("keydown", (e) => {
    const tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") return;
    if (e.key === "ArrowLeft") { e.preventDefault(); move(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); move(1); }
    else if (e.key === "c" || e.key === "C") { e.preventDefault(); $("copy-user").click(); }
    else if (e.key === "s" || e.key === "S") { e.preventDefault(); $("copy-system").click(); }
    else if (e.key === "m" || e.key === "M") { e.preventDefault(); toggleDone(); }
  });

  render();
</script>
</body>
</html>"""

html = html.replace("__SYSTEM_PROMPT__", sys_js)
html = html.replace("__DATA__", data_js)

out_html = "./benchmark/task_pool/ge-stance/ge_stance_console.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote {out_html} ({len(html)} bytes)")

# ---- CSV template ----
import csv

fieldnames = [
    "id",
    "source",
    "pillar",
    "statement",
    "gold_label",
    "prediction_base",
    "prediction_tuned_legends",
    "prediction_tuned_regulation",
    "notes",
]

out_csv = "./benchmark/task_pool/ge-stance/ge_stance_predictions_template.csv"
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in records:
        w.writerow({
            "id": r["id"],
            "source": r["source"],
            "pillar": r["pillar"],
            "statement": r["statement"],
            "gold_label": r["label"],
            "prediction_base": "",
            "prediction_tuned_legends": "",
            "prediction_tuned_regulation": "",
            "notes": "",
        })
print(f"Wrote {out_csv}")

# Quick verification
with open(out_csv) as f:
    lines = f.readlines()
print(f"CSV has {len(lines)} lines (1 header + {len(lines)-1} data)")
