"""
Module for processing PDF documents into chunks for RAG
"""

import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
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
    
    print(f"\nProcessing PDF: {pdf_path.name}")
    print(f"Total pages: {len(reader.pages)}")
    
    for i, page in enumerate(reader.pages, 1):
        page_text = page.extract_text()
        print(f"\nPage {i} content:")
        print(page_text)
        print("="*80)  # Separator line
        text += page_text + "\n\n"
    
    return text.strip()

def clean_text(text: str) -> str:
    """Clean text before chunking"""
    # Remove duplicate headers
    lines = text.split('\n')
    cleaned_lines = []
    for i, line in enumerate(lines):
        if i > 0 and line == lines[i-1]:
            continue
        cleaned_lines.append(line)
    
    # Remove empty lines
    cleaned_lines = [line for line in cleaned_lines if line.strip()]
    
    return '\n'.join(cleaned_lines)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks with better boundary detection
    """
    # Clean text first
    text = clean_text(text)
    
    # If text is shorter than chunk_size, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this isn't the last chunk, try to break at a natural boundary
        if end < len(text):
            # Look for better break points in order of preference
            break_points = [
                '\n\n',           # Paragraph break
                '.\n',            # End of sentence with newline
                '. ',             # End of sentence
                '\n',             # Any newline
                ' '               # Space as last resort
            ]
            
            for break_point in break_points:
                last_break = text[start:end].rfind(break_point)
                if last_break != -1:
                    end = start + last_break + len(break_point)
                    break
        
        # Add the chunk to list
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        # Move start point back by overlap amount
        start = end - overlap

    return chunks

def process_pdfs(chunk_size: int = 500, overlap: int = 50, 
                input_dir: Optional[Path] = None, 
                output_file: Optional[Path] = None) -> None:
    """
    Process PDFs in knowledge base directory and save chunks to JSON

    Args:
        chunk_size (int): Target size for each chunk in characters
        overlap (int): Number of characters to overlap between chunks
        input_dir (Optional[Path]): Directory containing PDF files. If None, uses default knowledge_base directory
        output_file (Optional[Path]): Path to output JSON file. If None, uses default faq_chunks.json
    """
    print("Starting PDF processing")
    print(f"Chunk size: {chunk_size}, Overlap: {overlap}")

    # Get the knowledge base directory path
    if input_dir is None:
        input_dir = Path(__file__).parent.parent / 'data' / 'knowledge_base'
    if output_file is None:
        output_file = Path(__file__).parent.parent / 'data' / 'faq_chunks.json'

    # List of our PDF Files
    pdf_files = list(input_dir.glob('*.pdf'))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to process")
    all_chunks = []
    chunk_id = 0

    # Process each PDF file
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        try:
            # Extract text from PDF
            text = read_pdf(str(pdf_file))
            
            # Clean and chunk text
            text_chunks = chunk_text(text, chunk_size, overlap)
            
            # Add metadata to each chunk
            for chunk in text_chunks:
                if chunk.strip():  # Only add non-empty chunks
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

    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(all_chunks)} chunks from {len(pdf_files)} files and saved to {output_file}")

if __name__ == "__main__":
    print("Starting PDF processing script")
    process_pdfs()
    print("PDF processing completed")

