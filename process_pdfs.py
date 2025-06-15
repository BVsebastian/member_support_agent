"""
Script to process PDF documents into chunks for RAG
"""

from agent.pdf_processor import process_pdfs

if __name__ == "__main__":
    # Process PDFs with default settings
    process_pdfs() 