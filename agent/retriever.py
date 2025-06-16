import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
import openai
from dotenv import load_dotenv

load_dotenv()

class Retriever:
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.PersistentClient(
            path=str(Path(__file__).parent.parent / "data" / "embeddings")
        )
    
        self.collection = self.client.get_collection(
        name="faq_chunks",)

    def retrieve_top_chunks(self, query: str, n_results: int = 3) -> list:
        """
        Retrieve the top N most relevant chunks for a given query.
        Args:
            query: The user's question or query string
            n_results: Number of top results to return (default: 3)

        Returns:
            list: List of dictionaries containing:
                - text: The chunk text
                - source: Source document
                - char_length: Length of the chunk
                - similarity_score: Cosine similarity score
        """
        #Create embedding for the query
        response = openai.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding

        #Query ChromaDB for similar chunks
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )
         
        #Format results into list of dictionaries
        formatted_results = []
        for text, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            formatted_results.append({
                'text': text,
                'source': metadata['source'],
                'char_length': metadata['char_length'],
                'similarity_score': 1 - distance
            })
        #Return the results
        return formatted_results


# if __name__ == "__main__":
#     print("Retrieving top chunks...")
#     retriever = Retriever()
#     results = retriever.retrieve_top_chunks("what are the required documents for signing up for a checking account?")
    
#     print("\nTop matching chunks:")
#     print("-" * 80)
#     for i, result in enumerate(results, 1):
#         print(f"\nResult {i}:")
#         print(f"Source: {result['source']}")
#         print(f"Similarity Score: {result['similarity_score']:.3f}")
#         print(f"Text: {result['text']}")
#         print("-" * 80)
    
#     print("\nDone!")

