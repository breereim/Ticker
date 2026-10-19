"""Create a local Brightspace-ready Project 1 package without submitting it."""
from datetime import date
from html import escape
from pathlib import Path
import re
from shutil import copy2

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "Brightspace Submission Package"
PDFS = PACKAGE / "PDFs"
TRANSCRIPTS = PACKAGE / "Corrected Transcripts"
VIDEO_TRANSCRIPTS = PACKAGE / "Corrected Video Transcripts"
UPLOAD = PACKAGE / "Brightspace Upload - Project 1"


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=16),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#17365D"), spaceBefore=10, spaceAfter=6),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#17365D"), spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12, spaceAfter=5),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12, leftIndent=14, firstLineIndent=-9, spaceAfter=3),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.2, leading=9),
    }


def rich(text):
    """Render the small Markdown subset used in the written records."""
    safe = escape(text)

    def render_code(match):
        content = match.group(1)
        if content.startswith(("https://", "http://")):
            return f'<link href="{content}" color="#0563C1"><u><font face="Courier">{content}</font></u></link>'
        return f'<font face="Courier">{content}</font>'

    safe = re.sub(r"`([^`]+)`", render_code, safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", safe)
    return safe


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#566573"))
    canvas.drawString(0.65 * inch, 0.42 * inch, "FIN 43900 Project 1")
    canvas.drawRightString(7.85 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


def markdown_flowables(text, source_label, s):
    flowables = [Paragraph(escape(source_label), s["small"]), Spacer(1, 7)]
    lines = text.replace("\r\n", "\n").split("\n")
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].startswith("|"):
                if not set(lines[index].replace("|", "").strip()) <= {"-", ":"}:
                    table_lines.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            if table_lines:
                columns = max(len(row) for row in table_lines)
                width = 7.15 * inch / columns
                data = [[Paragraph(rich(cell), s["small"]) for cell in row] for row in table_lines]
                grid = Table(data, colWidths=[width] * columns, repeatRows=1)
                grid.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#AAB7C4")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                flowables.extend([grid, Spacer(1, 8)])
            continue
        hashes = len(line) - len(line.lstrip("#"))
        if hashes and line[hashes:hashes + 1] == " ":
            style = s["h1"] if hashes == 1 else s["h2"]
            flowables.append(Paragraph(rich(line[hashes + 1:].strip()), style))
        elif line.startswith(("- ", "* ")):
            flowables.append(Paragraph("- " + rich(line[2:].strip()), s["bullet"]))
        elif len(line) > 2 and line[0].isdigit() and ". " in line[:4]:
            flowables.append(Paragraph(rich(line), s["bullet"]))
        elif line.startswith("> "):
            flowables.append(Paragraph(rich(line[2:]), s["bullet"]))
        else:
            flowables.append(Paragraph(rich(line), s["body"]))
        index += 1
    return flowables


def make_pdf(destination, title, sources):
    s = styles()
    flowables = [Paragraph(escape(title), s["title"])]
    for source_index, (label, path) in enumerate(sources):
        if source_index:
            flowables.append(PageBreak())
        flowables += markdown_flowables(path.read_text(encoding="utf-8"), label, s)
    document = SimpleDocTemplate(str(destination), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch, topMargin=0.62 * inch, bottomMargin=0.65 * inch)
    document.build(flowables, onFirstPage=footer, onLaterPages=footer)


def manifest_text():
    return f"""# Project 1 Brightspace Submission Manifest

**Prepared:** {date.today().isoformat()}
**Submission status:** Prepared locally only. Do not submit until the unresolved items below are completed.

## Repository and access

| Item | Link or status | Evidence timestamp | Access confirmation |
|---|---|---|---|
| Runnable GitHub repository | `https://github.com/breereim/Ticker` | `Repository link added October 18, 2026` | `TO CONFIRM signed-out or incognito access` |
| Video 1 research evolution | `https://drive.google.com/file/d/14XChhPVawzrEyPe4_pBoDFVdDvCG6E0f/view?usp=drive_link` | `00:53 - explains how further research led to a 5% to 3% revenue-growth path; 01:13 - explains the FCFE-to-FCFF method correction and why watch/defer remains the decision` | `Student confirmed playback on 2026-10-19` |
| Video 2 code validation | `https://drive.google.com/file/d/1roiGWMcMdPzj7hSpd5piyj6r51KdaK04/view?usp=drive_link` | `01:10 - explains statement and SEC starting-value checks; 01:31 - shows a lower-growth sensitivity test; 02:08 - explains reset restores the original values` | `Student confirmed playback on 2026-10-19` |
| Video 3 committee defense and dashboard validation | `https://drive.google.com/file/d/1aK6-ibWnEfYgv3ctLZZ-1oRnKn-qCGLS/view?usp=drive_link` | `00:17 - states watch/defer and why no position is initiated; 01:10 - resets a changed dashboard input; 02:17 - explains valuation-method disagreement and terminal-value reliance; 02:57 - explains the product-bridge monitoring question` | `Student confirmed playback on 2026-10-19` |

## Brightspace upload files

1. `PDFs/Submission-Manifest.pdf` - repository link, video links, evidence timestamps, and access confirmations.
2. `PDFs/Research-Evolution.pdf` - unchanged Edition A followed by final Edition B.
3. `PDFs/Decision-Memo.pdf` - final committee memo.
4. `PDFs/Validation-and-AI-Use.pdf` - validation record and AI-use disclosure.
5. `Corrected Video Transcripts/` - three timestamped corrected transcripts for Videos 1-3.

## Local video staging

- `../Video 1.mp4` - research-evolution source video.
- `../Video 2.mp4` - code-validation source video.
- `../Video 3.mp4` - committee-defense and dashboard-validation source video.

Each video has a Google Drive URL in the manifest. The local files remain the source copies; signed-out playback still needs to be confirmed before submission.

## Required verification before submission

- Confirm the course accepts timestamped video transcripts as the required three corrected transcript files. The original Lab 10-12 records remain in the repository as historical written coursework and are not the three video-transcript upload files.
- Test the listed GitHub repository link in a signed-out browser session.
- Record each video URL, the required evidence timestamp, and an access confirmation after the videos are published.
- Compare filenames and required deliverables with the Major Project Student Checklist. The checklist is not present in this workspace.
- Submit manually through Brightspace and retain the Brightspace submission receipt.
"""


def main():
    PDFS.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    VIDEO_TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    UPLOAD.mkdir(parents=True, exist_ok=True)
    edition_a = ROOT / "JNJ-research" / "Johnson_Johnson_2026-09-01_Project1_Edition_A.md"
    edition_b = ROOT / "JNJ-research" / "Johnson_Johnson_2026-10-18_Project1_Edition_B.md"
    memo = ROOT / "docs" / "decision-memo.md"
    validation = ROOT / "docs" / "validation-and-ai-use.md"
    manifest = PACKAGE / "Submission-Manifest.md"
    manifest.write_text(manifest_text(), encoding="utf-8")
    make_pdf(PDFS / "Research-Evolution.pdf", "Research Evolution", [("Edition A preserved unchanged", edition_a), ("Edition B final memorandum", edition_b)])
    make_pdf(PDFS / "Decision-Memo.pdf", "Decision Memo", [("Final committee memorandum", memo)])
    make_pdf(PDFS / "Validation-and-AI-Use.pdf", "Validation and AI Use", [("Validation record and disclosure", validation)])
    make_pdf(PDFS / "Submission-Manifest.pdf", "Project 1 Submission Manifest", [("Complete required fields before Brightspace submission", manifest)])
    transcript_sources = [
        (ROOT / "Lab 10 jnj_proforma.md", "Lab 10 jnj_proforma.md"),
        (ROOT.parent / "Lab 11 jnj_sensitivity.md", "Lab 11 jnj_sensitivity.md"),
        (ROOT / "Lab 12 jnj_valuation_reflection.md", "Lab 12 jnj_valuation_reflection.md"),
    ]
    for source, name in transcript_sources:
        if not source.is_file():
            raise FileNotFoundError(source)
        copy2(source, TRANSCRIPTS / name)
    (TRANSCRIPTS / "README.md").write_text(
        "# Provisional transcript set\n\n"
        "This folder stages the three locally identifiable weekly records: Lab 10, Lab 11, and Lab 12. "
        "Confirm against the Major Project Student Checklist before submission. Lab 11 documents an earlier FCFE model and is retained as historical coursework, not the final FCFF basis.\n",
        encoding="utf-8",
    )
    video_transcript_sources = [
        (ROOT / "video-transcripts" / "Video 1 - Research Evolution Transcript.md", "Video 1 - Research Evolution Transcript.md"),
        (ROOT / "video-transcripts" / "Video 2 - Code Validation Transcript.md", "Video 2 - Code Validation Transcript.md"),
        (ROOT / "video-transcripts" / "Video 3 - Committee Defense and Dashboard Transcript.md", "Video 3 - Committee Defense and Dashboard Transcript.md"),
    ]
    for source, name in video_transcript_sources:
        if not source.is_file():
            raise FileNotFoundError(source)
        copy2(source, VIDEO_TRANSCRIPTS / name)
    upload_sources = [
        PDFS / "Submission-Manifest.pdf",
        PDFS / "Research-Evolution.pdf",
        PDFS / "Decision-Memo.pdf",
        PDFS / "Validation-and-AI-Use.pdf",
        *[VIDEO_TRANSCRIPTS / name for _, name in video_transcript_sources],
    ]
    for source in upload_sources:
        if not source.is_file():
            raise FileNotFoundError(source)
        copy2(source, UPLOAD / source.name)
    print(f"Prepared local submission package at: {PACKAGE}")


if __name__ == "__main__":
    main()
