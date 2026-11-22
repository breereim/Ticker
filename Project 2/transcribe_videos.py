"""Create timestamped draft transcripts from the three local Project 2 videos.

Requires: pip install faster-whisper av==16.0.1
The speech model is downloaded on the first run.
"""

from pathlib import Path

from faster_whisper import WhisperModel


PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).resolve().parent


def timestamp(seconds: float) -> str:
    total = round(seconds)
    minutes, seconds = divmod(total, 60)
    return f"{minutes:02d}:{seconds:02d}"


def main() -> None:
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    for number in range(1, 4):
        video = PROJECT / f"Project 2 Video {number}.mp4"
        segments, info = model.transcribe(
            str(video),
            language="en",
            beam_size=5,
            vad_filter=True,
            initial_prompt=(
                "Meridian Foundation Reserve. BIL, IEF, LQD, SPY. "
                "Codex, Streamlit, Brightspace, ALFRED, FRED, BAA. "
                "Portfolio allocation, volatility, turnover, issuer look-through."
            ),
        )
        lines = [
            f"# Project 2 Video {number} — Transcript",
            "",
            f"Source: `{video.name}`. Automated speech-to-text draft; verify against the recording before submission.",
            "",
        ]
        count = 0
        for segment in segments:
            spoken = segment.text.strip()
            if spoken:
                lines.append(f"**[{timestamp(segment.start)}–{timestamp(segment.end)}]** {spoken}")
                lines.append("")
                count += 1
        destination = OUTPUT / f"project-2-video-{number}-transcript.md"
        destination.write_text("\n".join(lines), encoding="utf-8")
        print(f"{destination.name}: {count} segments, language={info.language}", flush=True)


if __name__ == "__main__":
    main()
