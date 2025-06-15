"""
Module for creating embeddings from FAQ chunks
"""
import json
import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
import openai
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.PersistentClient(
            path=str(Path(__file__).parent.parent / "data" / "embeddings")
        )

        self.collection = self.client.get_or_create_collection(
            name="faq_chunks",
            metadata={"hnsw:space": "cosine"}
        )

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

    def verify_index(self) -> dict:
        """
        Verify the status of the ChromaDB index.
        
        Returns:
            dict: Status information including:
                - total_chunks: Number of chunks in the index
                - sources: List of unique source documents
                - has_embeddings: Boolean indicating if embeddings exist
                - persistence_path: Path where embeddings are stored
        """
        # Get all items from collection, including embeddings
        results = self.collection.get(include=['embeddings', 'metadatas'])
        
        # Extract unique sources from metadata
        sources = set()
        if results['metadatas']:
            sources = {meta['source'] for meta in results['metadatas']}
        
        # Check if embeddings exist and are non-empty
        embeddings = results.get('embeddings')
        has_embeddings = embeddings is not None and len(embeddings) > 0
        
        # Get the persistence path and normalize it
        persistence_path = os.path.normpath(str(Path(__file__).parent.parent / "data" / "embeddings"))
        
        return {
            'total_chunks': len(results['ids']) if results['ids'] else 0,
            'sources': list(sources),
            'has_embeddings': has_embeddings,
            'persistence_path': persistence_path
        }
    
if __name__ == "__main__":
    print("Creating embeddings...")
    embedder = Embedder()
    embedder.create_embeddings()
    print("Done!")
