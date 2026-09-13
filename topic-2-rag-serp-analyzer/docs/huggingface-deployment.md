<!--
Traceability: supports B3/B14 (a real frontend beyond the CLI) — walkthrough
for actually deploying app.py as a Hugging Face Space, consolidated into one
followable doc rather than scattered across README.md's Deploy section.
-->

# Topic 2 — Deploying the Gradio UI to a Hugging Face Space

This walks through turning `app.py` into a live, shareable web app. Total
time: maybe 10 minutes, most of it waiting for the build.

## What you're deploying

A Gradio web UI wrapping `generate_seo_proposal()` — enter a keyword, get
back the SERP competitive analysis, the retrieved manual compliance
passages, and the final proposal, each in its own tab. No new logic beyond
`app.py` — everything else is the same `src/` code already verified.

## Prerequisites

- A Hugging Face account ([huggingface.co](https://huggingface.co) — free to sign up)
- The same Azure OpenAI values you already used for the Colab notebook:
  `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`,
  `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`

## Step 1 — Create the Space

1. Go to **[huggingface.co/new-space](https://huggingface.co/new-space)**
2. **Owner**: your account
3. **Space name**: whatever you want (e.g. `rag-serp-analyzer`)
4. **SDK**: select **Gradio**
5. **Space hardware**: the free "CPU basic" tier is enough — the actual
   model inference happens on Azure, this Space just runs a lightweight
   Python web server
6. **Visibility**: read the note below before choosing, then click **Create Space**

> **Keep it Private unless you specifically want it public.** This Space
> will hold your Azure OpenAI credentials as secrets. A *public* Space
> doesn't expose the secret values themselves, but it does mean anyone who
> finds the URL can click "Generate" and trigger real, billable Azure API
> calls on your account. Private is the safer default for a prototype.

## Step 2 — Upload the files

The Space needs its own copy of the code **and** the data (it has no
access to this project's other topics or the shared `data/` folder the way
a clone of the full GitHub repo would).

**Files to include, from `topic-2-rag-serp-analyzer/`:**
- `app.py`
- `requirements.txt`
- `README.md` (already has the Space-configuration header at the top)
- the whole `src/` folder (8 files)
- the whole `prompts/` folder (2 files)

**Plus, a `data/` folder you create for the Space specifically** —
containing copies of:
- `data/SERP_Data.json` (from the project root, not inside `topic-2-rag-serp-analyzer/`)
- `data/Manual.txt` (same)

`app.py` looks for `data/` right next to itself first, which is exactly
this layout.

### Option A — drag-and-drop via the web UI (no git needed)

1. Open your new Space → **Files** tab → **Add file → Upload files**
2. Drag in `app.py`, `requirements.txt`, `README.md`, and the `src/` and
   `prompts/` folders (drag the folders directly — HF preserves the
   structure)
3. Create the `data/` folder the same way: **Add file → Upload files**,
   navigate into (or create) a `data` path, upload `SERP_Data.json` and
   `Manual.txt` there

### Option B — git push (if you're comfortable with git)

```bash
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>

# copy topic-2's files in
cp -r /path/to/project-2026-01-claude/topic-2-rag-serp-analyzer/app.py .
cp -r /path/to/project-2026-01-claude/topic-2-rag-serp-analyzer/requirements.txt .
cp -r /path/to/project-2026-01-claude/topic-2-rag-serp-analyzer/README.md .
cp -r /path/to/project-2026-01-claude/topic-2-rag-serp-analyzer/src .
cp -r /path/to/project-2026-01-claude/topic-2-rag-serp-analyzer/prompts .

# the data files, from the project root (not topic-2-rag-serp-analyzer/)
mkdir -p data
cp /path/to/project-2026-01-claude/data/SERP_Data.json data/
cp /path/to/project-2026-01-claude/data/Manual.txt data/

git add -A
git commit -m "Initial Space deployment"
git push
```

This uses Hugging Face's own git remote (separate from the GitHub repo —
they're two independent deployments of the same code, which is intentional:
GitHub is the code-of-record for B19, this Space is the live demo).

## Step 3 — Set the secrets

In the Space → **Settings** tab → **Repository secrets** → **New secret**,
add each of these five (never commit them as a file — this is exactly what
keeps them out of the repo):

| Secret name | Value |
|---|---|
| `AZURE_OPENAI_API_KEY` | your key |
| `AZURE_OPENAI_ENDPOINT` | `https://<your-resource>.openai.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | e.g. `2024-10-21` |
| `AZURE_OPENAI_DEPLOYMENT` | your chat deployment name |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | your embedding deployment name |

## Step 4 — Wait for the build, then use it

The Space rebuilds automatically after any file/secret change — watch the
**Logs** tab. First build takes a few minutes (`chromadb`'s dependency tree
is large — same as it was locally/in Colab). Once it says **Running**:

1. Open the Space's app
2. The keyword field is pre-filled with `房屋二胎利率` — click **Generate proposal**
3. **First click will be slower** — `app.py` auto-ingests the manual into a
   fresh Chroma collection on first use (storage is ephemeral on the free
   tier, so this happens again after every restart, automatically, no
   manual step)
4. Check the three tabs: **Proposal**, **SERP analysis**, **Retrieved manual passages**

## Troubleshooting

- **Build fails** — check the Logs tab first. Common causes: a typo in
  `requirements.txt`, or the SDK wasn't set to "gradio" when creating the
  Space.
- **App loads but errors on "Generate"** — almost always a missing or
  placeholder secret; the error message from `app.py`'s `gr.Error` wrapping
  will name what's wrong (e.g. a specific missing `AZURE_OPENAI_*` value)
  rather than a blank failure.
- **`ValidationError` on the proposal** — see
  `docs/component-specs.md`'s run notes; `schemas.py` has a defensive
  coercion for the malformed shape this project hit once already, but a
  sufficiently different one will still raise clearly.
- **Data not found** — confirms the `data/` folder wasn't uploaded to the
  Space, or was uploaded at the wrong path (`app.py` expects it directly
  alongside `app.py`, i.e. `<space-root>/data/`, not nested further).
