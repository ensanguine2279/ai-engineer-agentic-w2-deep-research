# Deploying Deep Research to Google Cloud Run

## 0. Prerequisites

- A Google Cloud account (free tier is enough — Cloud Run's always-free tier
  covers 2 million requests/month, which is far more than a personal demo needs).
- [`gcloud` CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated:
  ```bash
  gcloud auth login
  gcloud config set project YOUR_PROJECT_ID
  ```
  If you don't have a project yet: `gcloud projects create YOUR_PROJECT_ID`
- Billing enabled on the project. This is required even for free-tier usage —
  Google needs a card on file, but you will not be charged as long as you stay
  within the free tier (which a low-traffic demo easily does).

## 1. Files you need in your project folder

Make sure these all sit in the same directory as `app.py`, `styles.py`, and
`research_manager.py`:

- `Dockerfile`
- `.dockerignore`
- `requirements.txt` — **fill this in** with whatever `research_manager.py`
  actually imports (OpenAI SDK, an agents framework, a search API client,
  etc.). The starter file only has `gradio` and `python-dotenv`, which are the
  only two imports visible in `app.py`.

## 2. Handle your API keys / secrets

Your app calls `load_dotenv()`, which is meant for **local** development.
On Cloud Run, don't ship a `.env` file into the image (it's excluded by
`.dockerignore` on purpose). Instead, pass these as environment variables at
deploy time via `--set-env-vars` / `--set-secrets` (step 4):

| Variable | Required? | Used by |
|---|---|---|
| `OPENAI_API_KEY` | **Yes** | `agents` SDK (planner, search, writer, email agents all call the OpenAI API) |
| `DEFAULT_MODEL_NAME` | No (defaults to `gpt-5.4-mini`) | all four agents |
| `HOW_MANY_SEARCHES` | No (defaults to `5`) | `planner_agent.py` |
| `USE_EMAIL` | No (defaults to `true`) | `email_agent.py` — set to `false` to push via Pushover instead of sending email |
| `EMAIL_ADDRESS`, `EMAIL_SMTP_SERVER`, `EMAIL_APP_PASSWORD` | Only if `USE_EMAIL=true` | `messenger.py` — `send_email` (note: current code sends **from and to the same address**) |
| `PUSHOVER_USER`, `PUSHOVER_TOKEN` | Only if `USE_EMAIL=false` | `messenger.py` — `push` |

Treat `OPENAI_API_KEY` and `EMAIL_APP_PASSWORD` as sensitive — use
[Secret Manager](https://cloud.google.com/run/docs/configuring/services/secrets)
(`--set-secrets`) for those rather than plain `--set-env-vars`, so they don't
show up in `gcloud run services describe` output or Cloud Console env var
lists in plaintext.

## 3. Enable the required APIs (one-time)

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

## 4. Build and deploy

From the project folder (where the `Dockerfile` lives), one command builds
the image, pushes it, and deploys it:

```bash
gcloud run deploy deep-research \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DEFAULT_MODEL_NAME=gpt-5.4-mini,HOW_MANY_SEARCHES=5,USE_EMAIL=true,EMAIL_ADDRESS=you@example.com,EMAIL_SMTP_SERVER=smtp.example.com \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest,EMAIL_APP_PASSWORD=email-app-password:latest
```

The `--set-secrets` values assume you've already created these in Secret
Manager:

```bash
echo -n "sk-...your-key..." | gcloud secrets create openai-api-key --data-file=-
echo -n "your-app-password" | gcloud secrets create email-app-password --data-file=-
```

If you'd rather keep it simple for a first deploy, you can pass everything
through `--set-env-vars` instead (including the API key) and move to Secret
Manager later — just know the key will then be visible in plaintext via
`gcloud run services describe` and the Cloud Console.

- `--source .` tells Cloud Run to build the Dockerfile in this directory
  using Cloud Build — no need to build/push the image manually.
- `--allow-unauthenticated` makes the app publicly reachable (drop this if
  you want to gate access behind Google auth/IAM instead).
- `--set-env-vars` — repeat as `KEY=value,KEY2=value2` for each secret your
  app needs. For anything sensitive, prefer `--set-secrets` with Secret
  Manager instead of a plain env var.
- Pick a `--region` close to you or your users (e.g. `us-central1`,
  `europe-west1`, `asia-southeast1`).

The first deploy will ask you to confirm creating an Artifact Registry
repository — accept it.

When it finishes, you'll get a URL like:
```
https://deep-research-xxxxx-uc.a.run.app
```
That's your live app.

## 5. Redeploying after changes

Same command, run again:

```bash
gcloud run deploy deep-research --source . --region us-central1
```

Cloud Run builds a new revision and shifts traffic to it once it's healthy;
the old revision is kept around briefly so a bad deploy can be rolled back.

## 6. Cost/idle behavior to expect

- Cloud Run scales to **zero** when nobody's using the app — you pay nothing
  while idle, and the free tier's 2M requests/month resets monthly.
- On the first request after idling, expect a **cold start** (a few seconds)
  while a container instance spins up. If that's a problem, you can set
  `--min-instances 1` to keep one warm — but that moves you off the free
  tier for compute time, since you're now paying for an always-on instance.

## 7. Common issues

- **"Container failed to start / listen on $PORT"** — this is almost always
  the app not binding to `0.0.0.0` and Cloud Run's injected `$PORT`. The
  patched `app.py` you have now handles this (`server_name="0.0.0.0"`,
  `server_port=int(os.environ.get("PORT", 7860))`).
- **Missing module errors at runtime** — `requirements.txt` is missing one of
  `research_manager.py`'s actual dependencies. Check the Cloud Run logs
  (`gcloud run services logs read deep-research --region us-central1`) for
  the exact `ModuleNotFoundError` and add it.
- **App loads but API calls fail** — usually a missing environment variable/
  secret (step 2). Check logs the same way.
