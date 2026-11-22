# Major Project Student Checklist — Project 2

Source: professor-provided checklist and submission architecture in conversation, 2026-11-18. This file records the Project 2 rules from those materials.

## Project 2 rules

- Every written part is Markdown in `docs/`, including `decision-memo.md` and `validation-and-ai-use.md`; attach those same `.md` files to Brightspace.
- Edition A, Edition B, their comparison, and the research-evolution item are not submitted for Project 2. The Locked Changed-Input Record still applies.
- The README, memo, and each video open with an AI-use announcement and an education/not-investment-advice statement.
- Videos are YouTube links, not video files. Video 3 opens with the app running live.
- Video 1: system and thinking changes plus one checked AI output; maximum 3:00.
- Video 2: code architecture, data flow, finance logic, reproducibility, and a meaningful validation or changed-input check; maximum 5:00.
- Video 3: live app opening, committee decision and defense, range, evidence, assumptions, risks, triggers, and committee ask; maximum 5:00.
- Corrected transcripts are required as `transcript-video-1.txt`, `transcript-video-2.txt`, and `transcript-video-3.txt`. Correct material finance terms, tickers, names, attribution, and numbers.
- Videos must be Public or Unlisted, never Private, and viewable by the instructional team. Record title, duration, URL, and timestamp index in the manifest.
- Every location in the manifest is a GitHub link except video locations, which are YouTube links. The architecture describes 12 manifest rows: 11 required and one optional deployed-output row; mark the research-evolution row not required for Project 2.
- The repository must include runnable source, environment/dependency file, README, visible executed output showing material inputs, as-of date, and decision, the two named Markdown records, and transcripts. Include `.env.example` only if credentials are needed.
- The memo must lead with the decision and include an allocation or decision range, as-of date, evidence, assumptions, sensitivity, failure conditions, monitoring triggers, committee ask, and pointer to the named AI disclosure.
- `validation-and-ai-use.md` must cover sources and as-of boundary, tests and results, limitations, material AI uses with tool/model/version and interaction date, and the complete Locked Changed-Input Record.
- The Locked Changed-Input Record needs a student-authored AI-off prediction committed before execution, exact old/new values with units, expected direction and decision effect, timestamp and immutable commit, then preserved before/after output, actual decision effect, reconciliation, and failure diagnosis when needed.
- Cold check: follow the README as a clean user; confirm repository/video access while logged out; ensure artifacts agree; confirm no credentials/private data; ensure recommendations have conditions, reversal triggers, and committee ask.
- Brightspace final submission attaches `decision-memo.md`, `validation-and-ai-use.md`, and the three corrected transcript `.txt` files, with a manifest of stable links and evidence timestamps.

The published Brightspace header controls points and due date. The analytic rubric controls scoring; neither was included in the material provided here.
