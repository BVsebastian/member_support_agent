import os
from pathlib import Path
import json
import chromadb
from chromadb.config import Settings
import openai
from dotenv import load_dotenv
from agent.pdf_processor import process_pdfs
from agent.embedder import Embedder

load_dotenv()

def setup_rag_pipeline():
    """Initialize RAG pipeline by creating embeddings if they don't exist."""
    data_dir = Path(__file__).parent.parent / "data"
    embeddings_dir = data_dir / "embeddings"
    chunks_file = data_dir / "faq_chunks.json"
    knowledge_base_dir = data_dir / "knowledge_base"

    # Check if we need to process PDFs
    if not chunks_file.exists():
        print("Processing PDFs to create FAQ chunks...")
        process_pdfs(
            chunk_size=1000,
            overlap=200,
            input_dir=knowledge_base_dir,
            output_file=chunks_file
        )
        print("FAQ chunks created successfully!")

    # Check if we need to create embeddings
    if not embeddings_dir.exists() or not list(embeddings_dir.glob("*")):
        print("Initializing RAG pipeline...")
        
        # Create embeddings directory if it doesn't exist
        embeddings_dir.mkdir(parents=True, exist_ok=True)
        
        # Create embeddings using the Embedder class
        embedder = Embedder()
        embedder.create_embeddings(chunks_file)
        
        print("RAG pipeline initialization complete!")
    else:
        print("RAG pipeline already initialized.")

if __name__ == "__main__":
    setup_rag_pipeline() 