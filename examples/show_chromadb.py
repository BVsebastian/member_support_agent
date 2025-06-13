"""
Display the contents of ChromaDB
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path
import json
import openai
from dotenv import load_dotenv

load_dotenv()

def create_embeddings():
    # Initialize ChromaDB client
    client = chromadb.Client(Settings(
        persist_directory=str(Path(__file__).parent.parent / "data" / "embeddings")
    ))
    
    # Create or get the collection
    collection = client.get_or_create_collection(name="faq_chunks")
    
    # Example FAQ data
    faqs = [
        {
            "id": "faq1",
            "text": "To reset your password, go to the login page and click 'Forgot Password'.",
            "source": "password_faq.pdf",
            "char_length": 80
        },
        {
            "id": "faq2",
            "text": "You can update your membership details in the Profile section.",
            "source": "membership_faq.pdf",
            "char_length": 70
        },
        {
            "id": "faq3",
            "text": "Our customer support team is available 24/7 through the Contact Us page.",
            "source": "support_faq.pdf",
            "char_length": 90
        }
    ]
    
    # Create embeddings for each FAQ
    for faq in faqs:
        response = openai.embeddings.create(
            input=faq['text'],
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        
        # Add to ChromaDB
        collection.add(
            ids=[faq['id']],
            embeddings=[embedding],
            documents=[faq['text']],
            metadatas=[{
                'source': faq['source'],
                'char_length': faq['char_length']
            }]
        )
    
    print("Created embeddings for example FAQs")
    return collection

def show_chromadb_contents():
    # First create some embeddings
    collection = create_embeddings()
    
    # Get all items from the collection
    results = collection.get(include=['embeddings', 'documents', 'metadatas'])
    
    print("\n=== ChromaDB Contents ===")
    print(f"Number of items in collection: {len(results['ids'])}")
    
    # Print each item with its metadata
    for i in range(len(results['ids'])):
        print(f"\nItem {i+1}:")
        print(f"ID: {results['ids'][i]}")
        print(f"Document: {results['documents'][i]}")
        print(f"Metadata: {results['metadatas'][i]}")
        
        # Get the embedding (first 5 dimensions for display)
        embedding = results['embeddings'][i]
        print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
        print("-" * 80)

if __name__ == "__main__":
    show_chromadb_contents() 