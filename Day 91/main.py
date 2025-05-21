"""
Convert a PDF document into a single MP3 audiobook using the iSpeech TTS API.

Dependencies:
    pip install python-dotenv PyPDF2 requests

Example:
    python main.py input.pdf output.mp3
"""

import os
import sys
from dotenv import load_dotenv
import PyPDF2
import requests

# --- Configuration --- #
load_dotenv()  # expects a .env file in the same directory
TTS_API_KEY = os.getenv('TTS_API_KEY')
if not TTS_API_KEY:
    sys.stderr.write("ERROR: TTS_API_KEY missing in environment (.env)\n")
    sys.exit(1)

TTS_ENDPOINT = "http://api.ispeech.org/api/rest"
VOICE = "usenglishfemale"
FORMAT = "mp3"
MAX_CHARS = 4500  # limit per request to avoid service caps

# --- Functions --- #

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Reads every page of the PDF and returns the combined text.
    """
    texts = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            # some PdfReader versions may not have extract_text on page
            text = getattr(page, "extract_text", lambda: "")() or ""
            texts.append(text)
    return "\n\n".join(texts).strip()


def chunk_text(text: str, max_length: int) -> list[str]:
    """
    Splits `text` into a list of strings each <= max_length characters,
    without losing any text.
    """
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = start + max_length
        # try to break at the last space within the block
        if end < length:
            space = text.rfind(" ", start, end)
            if space > start:
                end = space
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def synthesize_speech(text: str) -> bytes:
    """
    Calls the iSpeech API to convert `text` into speech.
    Returns raw MP3 bytes.
    """
    params = {
        'apikey': TTS_API_KEY,
        'action': 'convert',
        'text': text,
        'voice': VOICE,
        'format': FORMAT,
    }
    response = requests.get(TTS_ENDPOINT, params=params, timeout=30)
    response.raise_for_status()
    return response.content


def pdf_to_audiobook(input_pdf: str, output_mp3: str):
    print(f"[1] Extracting text from: {input_pdf}")
    full_text = extract_text_from_pdf(input_pdf)
    if not full_text:
        sys.stderr.write("ERROR: No text found in PDF.\n")
        return

    print("[2] Splitting text into chunks")
    chunks = chunk_text(full_text, MAX_CHARS)
    print(f"    → {len(chunks)} chunks of up to {MAX_CHARS} characters")

    print(f"[3] Creating audiobook file: {output_mp3}")
    with open(output_mp3, 'wb') as out_f:
        for i, chunk in enumerate(chunks, start=1):
            print(f"    • Synthesizing chunk {i}/{len(chunks)} ({len(chunk)} chars)...", end=" ")
            audio = synthesize_speech(chunk)
            out_f.write(audio)
            print("done")

    print("✅ Audiobook successfully generated.")


# --- Command-line interface --- #
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: python main.py <input.pdf> <output.mp3>\n")
        sys.exit(1)
    pdf_to_audiobook(sys.argv[1], sys.argv[2])
