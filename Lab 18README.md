# Lab 18 — Buffett EDGAR skill

The repo skill is at [`.agents/skills/buffett-edgar/SKILL.md`](../.agents/skills/buffett-edgar/SKILL.md). Its script gets ticker CIKs and companyfacts directly from SEC EDGAR. It uses only 10-K facts and computes the table and checks; the model writes the business judgment.

Set a real contact identity for SEC requests in your PowerShell session, then run:

```powershell
$env:SEC_USER_AGENT = 'Your Name your.email@example.edu'
& .\.venv\Scripts\python.exe .\.agents\skills\buffett-edgar\scripts\edgar_buffett.py COST
& .\.venv\Scripts\python.exe .\lab18\validate.py
& .\.venv\Scripts\python.exe -m streamlit run .\lab18\app.py
```

Replace the sample identity with your own before running. From a new Codex chat, ask: “Use `$buffett-edgar` on COST. Save a short business-only memo in `lab18/memos/COST.md`.” The app displays that file and lets you edit it for the hand-typed number probe. Use its **Save memo** button to keep an edit.

The checkout constants in `validate.py` are only a test oracle from the lab handout. They are never used to populate the script's report or the app. The source code includes no price request or valuation model.

The repo currently has no Git metadata or remote configured, so GitHub file links can be added after you publish these files to your repository.
