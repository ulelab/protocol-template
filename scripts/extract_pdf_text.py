from pathlib import Path
import sys
from pypdf import PdfReader

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_pdf_text.py input.pdf output.txt")
        sys.exit(1)

    input_pdf = Path(sys.argv[1])
    output_txt = Path(sys.argv[2])

    if not input_pdf.exists():
        raise FileNotFoundError(f"Missing input PDF: {input_pdf}")

    reader = PdfReader(str(input_pdf))
    chunks = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"\n\n--- PAGE {i} ---\n\n{text}")

    output_txt.write_text("".join(chunks), encoding="utf-8")
    print(f"Wrote extracted text to {output_txt}")

if __name__ == "__main__":
    main()