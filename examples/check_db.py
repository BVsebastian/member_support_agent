import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from agent.embedder import Embedder

def main():
    embedder = Embedder()
    status = embedder.verify_index()
    print("\nDatabase Status:")
    print(f"Total chunks: {status['total_chunks']}")
    print(f"Sources: {status['sources']}")
    print(f"Has embeddings: {status['has_embeddings']}")
    print(f"Persistence path: {status['persistence_path']}")

if __name__ == "__main__":
    main() 