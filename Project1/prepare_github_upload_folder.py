"""Stage a clean Project 1 folder for manual upload to GitHub.

The staged folder intentionally excludes the large local video files. Their hosted
Google Drive links are already embedded in the submission manifest.
"""
from pathlib import Path
from shutil import copy2, copytree


ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / "GitHub Upload - Project 1"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, destination)


def copy_directory(source: Path, destination: Path) -> None:
    copytree(
        source,
        destination,
        dirs_exist_ok=True,
        ignore=lambda _folder, names: {
            name for name in names
            if name in {".Rhistory", "__pycache__", "tmp"}
            or name.endswith(".mp4")
        },
    )


def main() -> None:
    DESTINATION.mkdir(exist_ok=True)

    for name in [
        "README.md",
        "jnj_project1_fcff.py",
        "jnj_valuation_app.py",
        "jnj_valuation_dashboard.html",
        "jnj_peer_multiples.py",
        "jnj_pe_valuation.py",
        "validation_suite.py",
        "cold_run_validation.py",
        "cold_run_validation.ps1",
        "export_final_report.py",
        "Start-JNJ-Dashboard.ps1",
        "prepare_submission_package.py",
        "prepare_github_upload_folder.py",
        "Lab 10 jnj_proforma.md",
        "Lab 12 jnj_valuation_reflection.md",
    ]:
        source = ROOT / name
        if not source.is_file():
            raise FileNotFoundError(source)
        copy_file(source, DESTINATION / name)

    for name in ["docs", "JNJ-research", "video-transcripts"]:
        source = ROOT / name
        if not source.is_dir():
            raise FileNotFoundError(source)
        copy_directory(source, DESTINATION / name)

    parent_lab11 = ROOT.parent / "Lab 11 jnj_sensitivity.md"
    if not parent_lab11.is_file():
        raise FileNotFoundError(parent_lab11)
    copy_file(parent_lab11, DESTINATION / "Historical Course Records" / parent_lab11.name)

    final_upload = ROOT / "Brightspace Submission Package" / "Brightspace Upload - Project 1"
    if not final_upload.is_dir():
        raise FileNotFoundError(final_upload)
    copy_directory(final_upload, DESTINATION / "Brightspace Submission Files")

    readme = DESTINATION / "README - Upload to GitHub.md"
    readme.write_text(
        "# GitHub upload folder\n\n"
        "Upload the contents of this folder to the `Ticker` repository. It contains the runnable Project 1 dashboard, "
        "supporting code, written records, source transcripts, and the final Brightspace submission files.\n\n"
        "The local video .mp4 files are intentionally excluded. The submission manifest contains their Google Drive links.\n",
        encoding="utf-8",
    )
    print(f"GitHub upload folder prepared at: {DESTINATION}")


if __name__ == "__main__":
    main()
