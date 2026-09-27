# Deep Research Assistant

Deep Research is a multi-agent research assistant. Give it a query through a
web UI, and it plans a set of web searches, runs them, synthesizes the
results into a long-form written report, and emails (or pushes) the report
to you — all orchestrated by a small pipeline of specialized AI agents built
on the OpenAI Agents SDK.

## What it does

1. You type a research question into the Gradio web interface.
2. A **planner** agent breaks the question down into several targeted web
   search queries.
3. A **search** agent runs each of those queries in parallel and summarizes
   the results.
4. A **writer** agent synthesizes all the search summaries into a cohesive,
   long-form markdown report (1000+ words).
5. An **email** agent converts that report into a clean HTML email and sends
   it (or pushes a notification instead, depending on configuration).
6. The UI streams status updates at each stage, then displays the final
   report inline.

## Architecture

The project is a thin Gradio front end wrapping a small pipeline of agents,
each with one clearly scoped job. Nothing here does its own orchestration
logic inside the agents themselves — that's centralized in one place
(`research_manager.py`), which keeps each agent simple and independently
testable.

```
┌─────────────┐      ┌────────────────────┐
│   app.py    │◄────►│  research_manager  │
│ (Gradio UI) │      │      .py           │
└─────────────┘      └─────────┬──────────┘
                                │ orchestrates, in order
                ┌───────────────┼───────────────┬───────────────┐
                ▼               ▼               ▼               ▼
        planner_agent    search_agent     writer_agent     email_agent
         .py                .py             .py              .py
                                                                │
                                                                ▼
                                                          messenger.py
                                                     (SMTP email / Pushover)
```

### `app.py` — UI layer

A single-page Gradio app: a query box, a submit button, a row of example
queries, and a Markdown output area that the report streams into. It calls
`ResearchManager().run(query)` as an async generator and re-renders the
output on every yielded status update, so the user sees live progress
("Searches planned...", "Writing report...", etc.) rather than a blank
screen until the whole pipeline finishes.

### `styles.py` — presentation

Pure CSS/HTML/JS injected into the Gradio app: custom branding header,
color tokens (with a dark-mode variant via `prefers-color-scheme`), styled
query input and buttons, and markdown-report styling (headings, code
blocks, tables, blockquotes). Also defines the example queries shown under
the search box. Kept separate from `app.py` so layout/logic and visual
styling don't get tangled together.

### `research_manager.py` — orchestration

The coordination layer. `ResearchManager.run()` is an async generator that
drives the whole pipeline step by step and yields a human-readable status
string after each stage:

1. `plan_searches()` — runs the planner agent once, gets back a structured
   `WebSearchPlan` (a list of `WebSearchItem`, each with a search query and
   a reason).
2. `perform_searches()` — runs the search agent **concurrently** for every
   planned search via `asyncio.gather`, since each search is independent
   and there's no reason to run them one at a time.
3. `write_report()` — runs the writer agent once, feeding it the original
   query plus every search summary, and gets back a structured `ReportData`
   (short summary, full markdown report, follow-up questions).
4. `send_email()` — hands the finished report to the email agent, which
   sends it out.

Every stage's result is validated Pydantic data (`WebSearchPlan`,
`ReportData`), not free-form text, which is what lets each agent's output
be fed reliably into the next stage.

The whole run is wrapped in an `agents.trace(...)` context, and the very
first status update includes a link to the OpenAI trace viewer — useful
for debugging exactly what each agent saw and produced at every step.

### The four agents

Each agent is defined identically: an `Agent(...)` instance from the
OpenAI Agents SDK, with its own instructions, model, and (where relevant)
tools or a structured output type. They share a `DEFAULT_MODEL_NAME` env
var (default `gpt-5.4-mini`) so the whole pipeline's model choice can be
swapped in one place.

- **`planner_agent.py`** — takes a query, no tools, and returns a
  structured `WebSearchPlan`. The number of searches it plans
  (`HOW_MANY_SEARCHES`, default 5) is configurable via env var and baked
  directly into its instructions.
- **`search_agent.py`** — takes one search term + reason, uses the Agents
  SDK's built-in `WebSearchTool`, and is forced to actually use it
  (`tool_choice="required"`) rather than answering from memory. Returns a
  short plain-text summary (2–3 paragraphs, <300 words) — deliberately
  concise, since the writer agent will receive several of these at once.
- **`writer_agent.py`** — takes the original query plus every search
  summary, no tools, and returns a structured `ReportData` (short summary,
  full markdown report of 1000+ words, and a list of suggested follow-up
  questions).
- **`email_agent.py`** — takes the finished report, has one custom tool
  (`send_email_tool`), and is forced to use it. It converts the markdown
  report into a subject line + HTML/plain-text email body and hands it to
  `messenger.py`. If `USE_EMAIL=false`, it calls `push()` (Pushover
  notification) instead of sending an actual email — useful for local
  testing without touching a real inbox.

### `messenger.py` — delivery mechanism

The only module with no agent logic at all — just two plain functions:

- `send_email()` — sends an HTML + plain-text email via SMTP
  (`smtplib`/`EmailMessage`), using `EMAIL_ADDRESS` /
  `EMAIL_SMTP_SERVER` / `EMAIL_APP_PASSWORD` from the environment. Note
  that as written, it sends **from and to the same address** — intended
  for "email the report to myself" use, not third-party recipients.
- `push()` — posts a plain-text notification to the Pushover API using
  `PUSHOVER_USER` / `PUSHOVER_TOKEN`.

Kept separate from `email_agent.py` so the agent only deals with
*composing* the message, while this module deals with actually *sending*
it — the agent doesn't need to know or care whether delivery happens via
SMTP or Pushover.

## Configuration (environment variables)

Loaded via `.env` locally (`load_dotenv(override=True)` in every module)
or via the deployment platform's env vars/secrets in production.

| Variable             | Default        | Required             | Purpose                                                      |
| -------------------- | -------------- | -------------------- | ------------------------------------------------------------ |
| `OPENAI_API_KEY`     | —              | **Yes**              | Used implicitly by the Agents SDK for every agent call       |
| `DEFAULT_MODEL_NAME` | `gpt-5.4-mini` | No                   | Model used by all four agents                                |
| `HOW_MANY_SEARCHES`  | `5`            | No                   | Number of searches the planner agent plans                   |
| `USE_EMAIL`          | `true`         | No                   | `true` sends an email; `false` sends a Pushover push instead |
| `EMAIL_ADDRESS`      | —              | If `USE_EMAIL=true`  | From/to address for the report email                         |
| `EMAIL_SMTP_SERVER`  | —              | If `USE_EMAIL=true`  | SMTP host used to send the email                             |
| `EMAIL_APP_PASSWORD` | —              | If `USE_EMAIL=true`  | App password for SMTP auth (not your main account password)  |
| `PUSHOVER_USER`      | —              | If `USE_EMAIL=false` | Pushover user key                                            |
| `PUSHOVER_TOKEN`     | —              | If `USE_EMAIL=false` | Pushover application token                                   |

## Running locally

```bash
pip install -r requirements.txt
# create a .env file with at least OPENAI_API_KEY set
python app.py
```

This launches Gradio locally (default `http://127.0.0.1:7860`).

## Development notebook

`deep_research.ipynb` is a step-by-step walkthrough of how the agent
pipeline was built and validated locally, before it was factored out into
the standalone modules described above. It's useful as a reference for how
each piece works in isolation, or as a starting point if you want to
experiment with the pipeline interactively rather than through the Gradio
UI. It builds up the same four agents in order:

1. **The Search Agent** — introduces the Agents SDK's hosted `WebSearchTool`
   and shows a single search running end-to-end, with a note on the
   trade-off of using OpenAI's hosted tools (convenient, but paid and
   ties you to their ecosystem).
2. **The Planner Agent** — introduces the `WebSearchItem` /
   `WebSearchPlan` Pydantic models and explains why forcing a structured
   output (rather than free-form text) makes the model plan its search
   strategy explicitly before executing any queries.
3. **The Writer Agent** — builds the report-writing agent from the search
   summaries.
4. **The Email Agent** — builds the `send_email_tool` function tool and the
   agent that uses it to turn a report into a formatted email.

It finishes with an **"Orchestration by Code"** section that manually
wires the four agents together with plain `async`/`await` and
`asyncio.gather` — the same pattern later formalized into
`ResearchManager` — and runs one full query end-to-end inside a
`trace(...)` block, with screenshots of the resulting OpenAI trace views
showing each agent's tool calls and the planner's structured
chain-of-thought output.

If you're new to the codebase, reading the notebook top to bottom before
diving into the module-by-module breakdown above is a good way to see
*why* each piece exists, not just what it does.

## Deploying to Google Cloud Run

The app is containerized and deployed with a source-based Cloud Run
deploy — no manual Docker build/push required.

### 1. Prerequisites

- A GCP project with billing enabled (required even for free-tier usage).

- `gcloud` CLI installed and authenticated (`gcloud auth login`,
  `gcloud config set project YOUR_PROJECT_ID`).

- Required APIs enabled once per project:
  
  ```bash
  gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
  ```

### 2. Container setup

`app.py` binds to `0.0.0.0` and Cloud Run's injected `$PORT` (defaulting to
`7860` for local runs):

```python
ui.launch(
    css=CSS,
    js=JS,
    theme=gr.themes.Base(),
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
)
```

This matters because Cloud Run's health check can't reach a container
listening only on `127.0.0.1`, and it always sets `PORT=8080` at runtime —
if the app doesn't read that env var, the deploy fails with a
"container failed to start and listen on the port" error.

The `Dockerfile` installs `requirements.txt`, copies the project in, and
runs `python app.py`.

### 3. Secrets

Never bake `OPENAI_API_KEY` or `EMAIL_APP_PASSWORD` into the image or an
`.env` file inside it (`.dockerignore` excludes `.env` for this reason).
Store them in Secret Manager instead:

```bash
echo -n "sk-...your-key..." | gcloud secrets create openai-api-key --data-file=-
echo -n "your-app-password" | gcloud secrets create email-app-password --data-file=-
```

Grant the Cloud Run service account access to each secret:

```bash
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding email-app-password \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 4. Deploy

```bash
gcloud run deploy deep-research \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DEFAULT_MODEL_NAME=gpt-5.4-mini,HOW_MANY_SEARCHES=5,USE_EMAIL=true,EMAIL_ADDRESS=you@example.com,EMAIL_SMTP_SERVER=smtp.example.com \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest,EMAIL_APP_PASSWORD=email-app-password:latest
```

This builds the image from the `Dockerfile` via Cloud Build, pushes it to
Artifact Registry, and deploys a new revision — no separate build/push
steps needed. The command outputs a public HTTPS URL once the revision
passes its health check.

### 5. Redeploying

Re-run the same `gcloud run deploy` command after making changes. Cloud
Run creates a new revision and shifts traffic to it once healthy; the
previous revision is kept (but idle, at no cost) unless deleted.

### 6. Cost behavior

Cloud Run scales to zero when idle, so cost is effectively zero for a
low-traffic personal tool, within the platform's always-free monthly
request quota. The trade-off is a cold start (a few seconds) on the first
request after a period of inactivity.

### Troubleshooting

- **"Container failed to start and listen on the port..."** — almost
  always means `server_name`/`server_port` in `app.py` aren't set as
  above, or a required env var/secret is missing and an agent module is
  throwing on import before Gradio ever calls `.launch()`. Check logs via
  the Cloud Console (Cloud Run → service → revision → Logs tab) or:
  
  ```bash
  gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=deep-research" --limit=50
  ```

- **Permission denied on a secret** — the compute service account needs
  the `Secret Manager Secret Accessor` role granted on that specific
  secret (see step 3).
