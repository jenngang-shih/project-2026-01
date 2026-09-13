Saved at topic-1-prompt-chaining/topic1_end_to_end_colab.ipynb and sent to you above so it's available on any device.

To run it:
1. Go to https://colab.research.google.com → File → Upload notebook → select this file
2. Open the 🔑 Secrets panel in the left sidebar and add these four secrets, then toggle "Notebook access" on for each: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT. (AZURE_OPENAI_EMBEDDING_DEPLOYMENT is not used — this chain has no embeddings/RAG step.)
3. Run cells top to bottom. Cell 1 (credentials) reads the four secrets above via `google.colab.userdata` — no typing/pasting keys into the notebook itself. If a secret is missing or access wasn't granted, the cell raises a clear error naming which one and what to fix.
4. Cell 6 runs Stage A live and prints 4+ candidate micro-intents
5. Cell 7 is the human checkpoint — type the index you want
6. Cell 8 runs Stage B + the audit/correct loop live, printing the final paragraph and full audit trail (including the pre-correction draft, per the fix from earlier)
7. Cell 9 downloads the session JSON to your machine before Colab's runtime recycles it

What's genuinely ported vs. adapted, spelled out in the notebook's own header cell:
- Schemas, prompt templates, and the orchestrator's control flow are embedded verbatim from the actual project files (I had the script read them directly off disk rather than retyping them, so there's no transcription drift)
- Only two things are adapted for Colab: credentials come from Colab Secrets (`google.colab.userdata`) instead of `.env`, and SESSIONS_DIR points at a local ./sessions folder instead of a path relative to __file__

One limitation worth knowing: this notebook is a standalone port, not a live link to your repo — if you later change orchestrator.py, prompts.py, schemas.py, or the .md prompt files locally, the notebook won't pick that up automatically. I generated it with a small script (build_colab_notebook.py, currently in my scratchpad) that reads those source files and rebuilds the notebook; say the word if you want me to move that script into the repo so you can re-run it yourself after future edits, or just ask me to regenerate it whenever the source changes.
