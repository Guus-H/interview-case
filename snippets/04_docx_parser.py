"""
Snippet 04 — Parsing a .docx file into clean, readable transcript text.

Word documents (.docx) are another common export format for meeting transcripts.
This snippet extracts the text content paragraph by paragraph, skipping empty lines,
and returns a clean string ready for further processing.
"""

from docx import Document


def parse_docx_to_text(filepath: str) -> str:
    """
    Read a .docx file and return its full text content as a plain string.
    Each non-empty paragraph becomes one line in the output.
    """
    doc = Document(filepath)
    lines = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(lines)


# --- Example usage ---
if __name__ == "__main__":
    transcript = parse_docx_to_text("transcripts/meeting_transcript.docx")
    print(transcript)
