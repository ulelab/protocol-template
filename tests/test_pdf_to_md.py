"""Tests for PDF-to-Markdown conversion helpers."""

import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "pdf_to_md" / "pdf_to_md.py"


def load_pdf_to_md_module():
    spec = importlib.util.spec_from_file_location("test_pdf_to_md_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ConvertPdfTests(unittest.TestCase):
    def test_convert_pdf_normalizes_image_dir_to_string_for_fast_mode(self) -> None:
        module = load_pdf_to_md_module()
        fake_extractor = types.SimpleNamespace()

        fast_mock = mock.Mock(return_value="markdown")
        fake_extractor.extract_pdf_fast = fast_mock

        with mock.patch.dict(sys.modules, {"extractor": fake_extractor}):
            with tempfile.TemporaryDirectory() as temp_dir:
                image_dir = Path(temp_dir) / "images"
                result = module.convert_pdf(
                    "example.pdf",
                    image_dir=image_dir,
                    show_progress=False,
                    docling=False,
                )

        self.assertEqual(result, "markdown")
        self.assertEqual(fast_mock.call_args.kwargs["image_dir"], str(image_dir))

    def test_convert_pdf_normalizes_image_dir_to_string_for_docling_mode(self) -> None:
        module = load_pdf_to_md_module()
        fake_extractor = types.SimpleNamespace()

        docling_mock = mock.Mock(return_value=("markdown", []))
        fake_extractor.extract_pdf_docling = docling_mock

        with mock.patch.dict(sys.modules, {"extractor": fake_extractor}):
            with tempfile.TemporaryDirectory() as temp_dir:
                image_dir = Path(temp_dir) / "images"
                result = module.convert_pdf(
                    "example.pdf",
                    image_dir=image_dir,
                    show_progress=False,
                    docling=True,
                )

        self.assertEqual(result, "markdown")
        self.assertEqual(docling_mock.call_args.kwargs["output_dir"], str(image_dir))


if __name__ == "__main__":
    unittest.main()
