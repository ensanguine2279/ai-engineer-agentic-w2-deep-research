EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Most commercially successful Agentic AI implementations in 2026",
    "Celebrities who don't like cheese",
]

HEADER_HTML = """
<div class="dr-brand">
    <div class="dr-mark" aria-hidden="true">
        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="1" y="1" width="30" height="30" rx="7" stroke="currentColor" stroke-width="1.5"/>
            <text x="16" y="21.5" text-anchor="middle" fill="currentColor" font-size="11" font-weight="600" font-family="IBM Plex Sans, Segoe UI, sans-serif">DR</text>
        </svg>
    </div>
    <div class="dr-titles">
        <p class="dr-kicker">Research console</p>
        <h1>Deep Research</h1>
        <p class="dr-sub">Structured web investigation across multiple sources</p>
    </div>
</div>
"""

CSS = """
.gradio-container {
    --dr-bg: #f4f6f8;
    --dr-surface: #ffffff;
    --dr-elevated: #f8fafc;
    --dr-line: #d8dee6;
    --dr-line-strong: #c5ced8;
    --dr-text: #1b2430;
    --dr-muted: #5c6b7a;
    --dr-accent: #1d4ed8;
    --dr-accent-hover: #1e40af;
    --dr-accent-soft: #eff4ff;
    --dr-shadow: 0 1px 2px rgba(27, 36, 48, 0.06), 0 8px 24px rgba(27, 36, 48, 0.04);
    --dr-radius: 10px;
    --dr-font: "IBM Plex Sans", "Segoe UI", Helvetica, Arial, sans-serif;
    --dr-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;

    max-width: 860px !important;
    margin: 0 auto !important;
    padding: 2.75rem 1.5rem 4.5rem !important;
    background: var(--dr-bg) !important;
    color: var(--dr-text) !important;
    font-family: var(--dr-font) !important;
}

.gradio-container.dark,
.dark .gradio-container,
body.dark .gradio-container,
html.dark .gradio-container {
    --dr-bg: #0f1419;
    --dr-surface: #171e26;
    --dr-elevated: #1c2530;
    --dr-line: #2c3845;
    --dr-line-strong: #3d4b5a;
    --dr-text: #e8eef4;
    --dr-muted: #93a1b0;
    --dr-accent: #60a5fa;
    --dr-accent-hover: #93c5fd;
    --dr-accent-soft: #1a2740;
    --dr-shadow: 0 1px 2px rgba(0, 0, 0, 0.35), 0 12px 28px rgba(0, 0, 0, 0.22);
}

body {
    background: var(--dr-bg, #f4f6f8);
}

/* === HEADER === */
.dr-brand {
    display: flex;
    align-items: flex-start;
    gap: 1.15rem;
    padding: 0 0 1.75rem;
    margin-bottom: 1.75rem;
    border-bottom: 1px solid var(--dr-line);
}

.dr-mark {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    color: var(--dr-accent);
    margin-top: 0.15rem;
}

.dr-mark svg {
    display: block;
    width: 100%;
    height: 100%;
}

.dr-kicker {
    font-family: var(--dr-mono);
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--dr-muted);
    margin: 0 0 0.35rem;
}

.dr-titles h1 {
    font-size: 1.65rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.2;
    color: var(--dr-text);
}

.dr-sub {
    font-size: 0.92rem;
    color: var(--dr-muted);
    margin: 0.4rem 0 0;
    line-height: 1.45;
}

/* === QUERY ROW === */
.dr-query-row {
    gap: 0.75rem !important;
    align-items: stretch !important;
}

#dr-query, #dr-query > div, #dr-query .wrap, #dr-query .form, #dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

#dr-query textarea, #dr-query input {
    background: var(--dr-surface) !important;
    color: var(--dr-text) !important;
    border: 1px solid var(--dr-line-strong) !important;
    border-radius: var(--dr-radius) !important;
    padding: 0.95rem 1.1rem !important;
    font-size: 0.98rem !important;
    font-family: inherit !important;
    box-shadow: var(--dr-shadow) !important;
    line-height: 1.5 !important;
    resize: none !important;
    min-height: 52px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}

#dr-query textarea:focus, #dr-query input:focus {
    outline: none !important;
    border-color: var(--dr-accent) !important;
    box-shadow: 0 0 0 3px var(--dr-accent-soft), var(--dr-shadow) !important;
}

#dr-query textarea::placeholder, #dr-query input::placeholder {
    color: var(--dr-muted) !important;
    opacity: 0.85 !important;
}

#dr-run {
    background: var(--dr-accent) !important;
    color: #ffffff !important;
    border: 1px solid transparent !important;
    border-radius: var(--dr-radius) !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    font-size: 0.92rem !important;
    box-shadow: 0 1px 2px rgba(29, 78, 216, 0.25) !important;
    transition: background 0.15s ease, transform 0.08s ease !important;
    min-width: 132px !important;
    padding: 0.9rem 1.25rem !important;
}

.dark #dr-run, html.dark #dr-run {
    color: #0f1419 !important;
    box-shadow: none !important;
}

#dr-run:hover {
    background: var(--dr-accent-hover) !important;
}

#dr-run:active {
    transform: translateY(1px) !important;
}

/* === EXAMPLES === */
.dr-examples-label {
    font-family: var(--dr-mono);
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    color: var(--dr-muted);
    text-transform: uppercase;
    margin: 1.75rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.dr-examples-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--dr-line);
}

#dr-examples, #dr-examples > div, #dr-examples .wrap, #dr-examples .block {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

#dr-examples label, #dr-examples .label-wrap, #dr-examples > div > .label-wrap {
    display: none !important;
}

#dr-examples table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: auto !important;
    background: transparent !important;
    border: none !important;
}

#dr-examples thead { display: none !important; }
#dr-examples tbody { background: transparent !important; }

#dr-examples tr {
    background: transparent !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    border: none !important;
}

#dr-examples td, #dr-examples button {
    background: var(--dr-surface) !important;
    border: 1px solid var(--dr-line) !important;
    padding: 0.55rem 0.9rem !important;
    cursor: pointer !important;
    transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease !important;
    font-size: 0.84rem !important;
    color: var(--dr-muted) !important;
    border-radius: 999px !important;
    margin: 0 !important;
    text-align: left !important;
    box-shadow: none !important;
    line-height: 1.35 !important;
}

#dr-examples td:hover, #dr-examples button:hover {
    border-color: var(--dr-accent) !important;
    background: var(--dr-accent-soft) !important;
    color: var(--dr-accent) !important;
}

/* === REPORT === */
#dr-report {
    margin-top: 2rem !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--dr-text) !important;
}

#dr-report > div, #dr-report .prose {
    background: transparent !important;
    color: var(--dr-text) !important;
}

/* Only apply the card treatment once Gradio has actually rendered markdown
   content inside .prose. Gradio's Markdown component always leaves an empty
   .prose wrapper in the DOM, so :not(:empty) matched immediately on page
   load and produced an empty white box. :has() checks for real content
   elements instead. */
#dr-report:has(.prose :is(h1, h2, h3, h4, p, ul, ol, table, blockquote, pre)) {
    background: var(--dr-surface) !important;
    border: 1px solid var(--dr-line) !important;
    border-radius: 12px !important;
    box-shadow: var(--dr-shadow) !important;
    padding: 1.5rem 1.6rem 1.7rem !important;
}

#dr-report h1 {
    font-size: 1.45rem;
    font-weight: 650;
    color: var(--dr-text);
    border-bottom: 1px solid var(--dr-line);
    padding-bottom: 0.6rem;
    margin: 0 0 1.1rem;
    letter-spacing: -0.02em;
}

#dr-report h2 {
    font-size: 1.12rem;
    color: var(--dr-text);
    font-weight: 650;
    margin-top: 1.6rem;
    letter-spacing: -0.015em;
}

#dr-report h3 {
    font-size: 1rem;
    color: var(--dr-text);
    font-weight: 600;
    margin-top: 1.3rem;
}

#dr-report p {
    line-height: 1.7;
    color: var(--dr-text);
}

#dr-report a {
    color: var(--dr-accent);
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
}

#dr-report a:hover {
    color: var(--dr-accent-hover);
}

#dr-report code {
    background: var(--dr-elevated);
    border: 1px solid var(--dr-line);
    padding: 0.12rem 0.38rem;
    font-size: 0.88em;
    border-radius: 5px;
    font-family: var(--dr-mono);
}

#dr-report pre {
    background: var(--dr-elevated);
    border: 1px solid var(--dr-line);
    border-radius: 8px;
    padding: 1rem 1.15rem;
}

#dr-report blockquote {
    border-left: 3px solid var(--dr-accent) !important;
    background: var(--dr-accent-soft);
    padding: 0.85rem 1.1rem;
    margin: 1rem 0;
    color: var(--dr-text);
    border-radius: 0 8px 8px 0;
}

#dr-report ul, #dr-report ol { padding-left: 1.35rem; }
#dr-report li { margin: 0.28rem 0; line-height: 1.65; }

#dr-report table {
    border-collapse: collapse;
    width: 100%;
    border: 1px solid var(--dr-line);
    border-radius: 8px;
    overflow: hidden;
}

#dr-report th, #dr-report td {
    border: 1px solid var(--dr-line);
    padding: 0.5rem 0.75rem;
    text-align: left;
}

#dr-report th {
    background: var(--dr-elevated);
    font-weight: 600;
    color: var(--dr-text);
    font-size: 0.86rem;
}

footer { display: none !important; }

@media (max-width: 700px) {
    .gradio-container { padding: 1.5rem 1rem 3rem !important; }
    .dr-brand { gap: 0.9rem; }
    .dr-titles h1 { font-size: 1.4rem; }
    .dr-query-row { flex-direction: column !important; }
    #dr-run { width: 100% !important; }
}
"""

JS = """
() => {
    const font = document.createElement("link");
    font.rel = "stylesheet";
    font.href = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap";
    document.head.appendChild(font);

    const focus = () => {
        const el = document.querySelector("#dr-query textarea, #dr-query input");
        if (el) { el.focus(); return true; }
        return false;
    };
    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => {
            if (focus() || ++tries > 20) clearInterval(i);
        }, 100);
    }
}
"""