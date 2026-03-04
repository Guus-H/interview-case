"""
Snippet 02 — Parsing a .vtt file into clean, readable transcript text.

VTT (Web Video Text Tracks) is the format exported by Microsoft Teams and Copilot.
Raw VTT files contain timestamps, cue numbers, and XML-style speaker tags that
need to be stripped before the text can be processed further.

This snippet provides two outputs:
  - A plain text string (speaker: text, one line per turn)
  - A list of dicts [{"speaker": ..., "text": ...}, ...]
"""

import re


def parse_vtt_to_text(filepath: str) -> str:
    """
    Read a .vtt file and return a clean transcript as a plain string.
    Each line is in the format "Speaker Name: their words here."
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove the WEBVTT header line
    content = re.sub(r"^WEBVTT[^\n]*\n", "", content, flags=re.MULTILINE)

    # Remove timestamp lines: "00:00:05.000 --> 00:00:09.340"
    content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}[^\n]*\n", "", content)

    # Remove cue index lines (lines that are just a number)
    content = re.sub(r"^\d+\s*$", "", content, flags=re.MULTILINE)

    # Convert "<v Speaker Name>text</v>" to "Speaker Name: text"
    content = re.sub(r"<v ([^>]+)>(.*?)</v>", r"\1: \2", content)

    # Strip any remaining HTML/XML tags
    content = re.sub(r"<[^>]+>", "", content)

    # Collapse multiple blank lines into one
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()


def parse_vtt_to_list(filepath: str) -> list[dict]:
    """
    Read a .vtt file and return a list of speaker turns.
    Each item is {"speaker": "Name", "text": "What they said"}.
    Lines without a recognisable speaker prefix are skipped.
    """
    plain = parse_vtt_to_text(filepath)
    turns = []
    for line in plain.splitlines():
        line = line.strip()
        if not line:
            continue
        if ": " in line:
            speaker, _, text = line.partition(": ")
            turns.append({"speaker": speaker.strip(), "text": text.strip()})
    return turns


# --- Example usage ---
if __name__ == "__main__":
    path = "transcripts/meeting_transcript.vtt"

    print("=== Plain text ===")
    print(parse_vtt_to_text(path))

    print("\n=== Structured list (first 3 turns) ===")
    turns = parse_vtt_to_list(path)
    for turn in turns[:3]:
        print(turn)
