"""
Visual example of how embeddings work
"""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import openai
from dotenv import load_dotenv

load_dotenv()

def create_embedding(text):
    """Create an embedding for a given text"""
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def visualize_embeddings():
    # Example texts
    texts = [
        "How do I reset my password?",
        "I forgot my login credentials",
        "Need to change my password",
        "How do I update my profile?",
        "Where can I change my account settings?",
        "I want to modify my user information",
        "How do I contact customer support?",
        "I need help with my account",
        "Where can I get assistance?",
        "How do I reach the help desk?"
    ]
    
    # Create embeddings for all texts
    print("Creating embeddings...")
    embeddings = [create_embedding(text) for text in texts]
    
    # Convert embeddings to numpy array
    embeddings_array = np.array(embeddings)
    
    # Use PCA to reduce dimensions to 2D for visualization
    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(embeddings_array)
    
    # Create the visualization
    plt.figure(figsize=(12, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='blue', alpha=0.5)
    
    # Add text labels
    for i, text in enumerate(texts):
        plt.annotate(text, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    
    plt.title("Visualization of Text Embeddings\n(Similar texts are closer together)")
    plt.xlabel("PCA Dimension 1")
    plt.ylabel("PCA Dimension 2")
    
    # Save the plot
    plt.savefig('embedding_visualization.png')
    print("\nVisualization saved as 'embedding_visualization.png'")
    
    # Print similarity scores between first text and others
    print("\nSimilarity scores with 'How do I reset my password?':")
    first_embedding = embeddings[0]
    for i, text in enumerate(texts[1:], 1):
        similarity = np.dot(first_embedding, embeddings[i]) / (
            np.linalg.norm(first_embedding) * np.linalg.norm(embeddings[i])
        )
        print(f"{text}: {similarity:.3f}")

if __name__ == "__main__":
    visualize_embeddings() 