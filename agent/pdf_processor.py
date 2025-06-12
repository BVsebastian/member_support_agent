"""
Module for processing PDF documents into chunks for RAG
"""

import json
import datetime
from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader

def read_pdf(file_path: str) -> str:
    """
    Extract text from a PDF File.
    Args:
        file_path (str): Path to the PDF File
    Returns:
        str: Extracted text content
    Raises:
        FileNotFoundError: If the file does not exist
    """

    pdf_path = Path(file_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found at {file_path}")
    
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n\n"
    
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into chunks with overlap.
    Args:
        text (str): Text to split into chunks
        chunk_size (int): Target size for each chunk in characters
        overlap (int): Number of characters to overlap between chunks
    Returns:
        List[str]: List of text chunks
    """
    # If text is shorter than chunk_size, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        # If this isn't the last chunk, try to break at a sentence or paragraph
        if end < len(text):
            # Look for natural break points (period followed by space or newline)
            for break_point in ['. ', '.\n','\n\n']:
                last_break = text[start:end].rfind(break_point)
                if last_break != -1:
                    end = start + last_break + len(break_point)
                    break
        # Add the chunk to list
        chunks.append(text[start:end].strip())

        #Move start point back by overlap amount
        start = end - overlap

    return chunks

def process_pdfs(chunk_size: int = 500, overlap: int = 100) -> None:
    """
    Process PDFs in knowledge base directory and save chunks to JSON

    Args:
        chunk_size (int): Target size for each chunk in characters
        overlap (int): Number of characters to overlap between chunks
    """
    # Get the knowledge base directory path
    knowledge_base_dir = Path(__file__).parent.parent / 'data' /'knowledge_base'
    output_file = Path(__file__).parent.parent / 'data' / 'faq_chunks.json'

    # List of our PDF Files
    pdf_files = list(knowledge_base_dir.glob('*.pdf'))
    if not pdf_files:
        print(f"No PDF files found in {knowledge_base_dir}")
        return

    all_chunks = []
    chunk_id = 0

    # Process each PDF file
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        try:
            # Extract text from PDF
            text = read_pdf(str(pdf_file))  # pdf_file is already a full path

            # Split into chunks
            text_chunks = chunk_text(text, chunk_size, overlap)

            # Add metadata to each chunk
            for chunk in text_chunks:
                chunk_id += 1
                all_chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "text": chunk,
                    "source": pdf_file.name,
                    "char_length": len(chunk)
                })
        except FileNotFoundError as e:
            print(f"Error processing {pdf_file.name}: {e}")
            continue

    # Prepare the output JSON
    output_data = {
        "chunks": all_chunks,
        "metadata": {
            "total_chunks": len(all_chunks),
            "processed_files": [f.name for f in pdf_files],
            "chunk_size": chunk_size,
            "overlap": overlap,
            "creation_timestamp": datetime.datetime.now().isoformat()
        }
    }

    # Create data directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(all_chunks)} chunks from {len(pdf_files)} files and saved to {output_file}")