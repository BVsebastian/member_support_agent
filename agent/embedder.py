"""
Module for creating embeddings from FAQ chunks
"""
import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
import openai
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.Client(Settings(
            persist_directory=str(Path(__file__).parent.parent / "data" / "embeddings")
        ))

        self.collection = self.client.get_or_create_collection(
            name="faq_chunks")

    def create_embeddings(self, chunks_file: str = None):
        """
        Create embeddings for FAQ chunks and store in ChromaDB

        Args:
            chunks_file: Path to the JSON file containing chunks. If none, uses default location
        """
        if chunks_file is None:
            chunks_file = Path(__file__).parent.parent / "data" / "faq_chunks.json"

        with open(chunks_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks = data['chunks']

        for chunk in chunks:
            response = openai.embeddings.create(
                input=chunk['text'],
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
        
            self.collection.add(
                ids=[chunk['chunk_id']],
                embeddings=[embedding],
                documents=[chunk['text']],
                metadatas=[{
                    'source': chunk['source'],
                    'char_length': chunk['char_length'],
                }])

        # Print confirmation message
        print(f"Created embeddings for {len(chunks)} chunks")