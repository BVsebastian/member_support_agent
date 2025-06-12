"""
Tests for the pdf_processor module.
"""

import unittest
from agent.pdf_processor import process_pdfs, chunk_text, read_pdf
from pathlib import Path

class TestPDFProcessor(unittest.TestCase):
    def test_read_pdf(self):
        """Test PDF reading functionality"""
        knowledge_base_dir = Path(__file__).parent.parent / 'data' / 'knowledge_base'
        test_pdfs = list(knowledge_base_dir.glob('*.pdf'))

        # Verify that the test PDFs are found
        self.assertGreater(len(test_pdfs), 0, "No test PDFs found")

        # Test reading first available PDF
        test_pdf = test_pdfs[0]
        text = read_pdf(str(test_pdf))

        # Basic validations
        self.assertIsInstance(text, str, "Read text is not a string")
        self.assertGreater(len(text), 0, "Read text is empty")
        self.assertEqual(text.strip(), text, "Extracted text should not contain leading/trailing whitespace")

        # Test non-existent file
        with self.assertRaises(FileNotFoundError):
            read_pdf("nonexistent.pdf")
    

if __name__ == '__main__':
    unittest.main()






