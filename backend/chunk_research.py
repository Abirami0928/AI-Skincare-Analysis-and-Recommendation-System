
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "research_text"
OUTPUT_DIR = BASE_DIR / "research_chunks"

OUTPUT_DIR.mkdir(exist_ok=True)

CHUNK_SIZE = 1200
OVERLAP = 200


def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def create_chunks(text, source):
    # Separate the text into paragraphs
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r'\n\s*\n', text)
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        sentences = split_into_sentences(paragraph)

        for sentence in sentences:

            # Handle an unusually long sentence
            if len(sentence) > CHUNK_SIZE:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                for start in range(0, len(sentence), CHUNK_SIZE - OVERLAP):
                    piece = sentence[start:start + CHUNK_SIZE]
                    if piece.strip():
                        chunks.append(piece.strip())

                continue

            if len(current_chunk) + len(sentence) + 1 <= CHUNK_SIZE:
                current_chunk += " " + sentence if current_chunk else sentence

            else:
                if current_chunk:
                    chunks.append(current_chunk)

                # Preserve some context from the previous chunk
                overlap_text = current_chunk[-OVERLAP:] if current_chunk else ""

                current_chunk = (
                    overlap_text + " " + sentence
                    if overlap_text else sentence
                )

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return [
        {
            "chunk_id": index,
            "source": source,
            "text": chunk
        }
        for index, chunk in enumerate(chunks)
    ]


if __name__ == "__main__":

    all_chunks = []

    text_files = list(INPUT_DIR.glob("*.txt"))

    print("Research documents found:", len(text_files))

    for file_path in text_files:

        text = file_path.read_text(encoding="utf-8")

        document_chunks = create_chunks(text, file_path.name)

        all_chunks.extend(document_chunks)

        print(
            f"{file_path.name}: "
            f"{len(document_chunks)} chunks"
        )

    output_file = OUTPUT_DIR / "chunks.json"

    output_file.write_text(
        json.dumps(all_chunks, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nChunking completed!")
    print("Total chunks:", len(all_chunks))
    print("Saved to:", output_file)
