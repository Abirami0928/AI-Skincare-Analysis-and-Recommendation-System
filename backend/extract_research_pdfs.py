
from pathlib import Path
import fitz
import json

BASE_DIR = Path(__file__).resolve().parent.parent

RESEARCH_DIR = BASE_DIR / "research_documents"
OUTPUT_DIR = BASE_DIR / "research_text"

OUTPUT_DIR.mkdir(exist_ok=True)


def extract_pdf(pdf_path):

    document = fitz.open(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text")

        if text.strip():
            extracted_pages.append(
                f"\n--- Page {page_number} ---\n{text}"
            )

    full_text = "\n".join(extracted_pages)

    output_file = OUTPUT_DIR / f"{pdf_path.stem}.txt"

    output_file.write_text(
        full_text,
        encoding="utf-8"
    )

    return {
        "file": pdf_path.name,
        "pages": len(document),
        "characters": len(full_text),
        "output": str(output_file)
    }


if __name__ == "__main__":

    pdf_files = list(RESEARCH_DIR.rglob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files")

    results = []

    for pdf_path in pdf_files:

        try:
            result = extract_pdf(pdf_path)
            results.append(result)

            print(
                f"Extracted: {result['file']} "
                f"({result['characters']} characters)"
            )

        except Exception as error:
            print(f"Failed: {pdf_path.name} - {error}")

    report_file = OUTPUT_DIR / "extraction_report.json"

    report_file.write_text(
        json.dumps(results, indent=4),
        encoding="utf-8"
    )

    print("\nPDF extraction completed!")
