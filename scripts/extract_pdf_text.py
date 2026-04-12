"""Extract text from a single PDF file and write it to a plain text file."""

from pathlib import Path
import sys
from pypdf import PdfReader

def resolve_input_pdf(input_arg: str) -> Path:
    input_path = Path(input_arg)

    if input_path.is_file():
        return input_path

    if input_path.is_dir():
        pdf_files = sorted(
            [p for p in input_path.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
        )

        if len(pdf_files) == 0:
            raise FileNotFoundError(
                f"No PDF files found in folder: {input_path}. Expected exactly one .pdf file."
            )

        if len(pdf_files) > 1:
            names = ", ".join(p.name for p in pdf_files)
            raise ValueError(
                f"Multiple PDF files found in folder: {input_path}. "
                f"Expected exactly one .pdf file, found {len(pdf_files)}: {names}"
            )

        return pdf_files[0]

    raise FileNotFoundError(f"Input path does not exist: {input_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_pdf_text.py <input.pdf|input_folder> output.txt")
        sys.exit(1)

    input_pdf = resolve_input_pdf(sys.argv[1])
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
