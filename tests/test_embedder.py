"""
Tests for the Embedder class using unittest
"""
import json
from pathlib import Path
import unittest
from agent.embedder import Embedder

class TestEmbedder(unittest.TestCase):
    def setUp(self):
        self.embedder = Embedder()
        self.sample_chunks = {
            "chunks": [
                {
                    "chunk_id": "test1",
                    "text": "This is a test chunk for embedding.",
                    "source": "test_source.pdf",
                    "char_length": 30
                },
                {
                    "chunk_id": "test2",
                    "text": "Another test chunk for embedding.",
                    "source": "test_source.pdf",
                    "char_length": 35
                }
            ]
        }

    def test_create_embeddings(self):
        # Save sample chunks to a temporary JSON file
        chunks_file = Path("test_chunks.json")
        with open(chunks_file, "w") as f:
            json.dump(self.sample_chunks, f)
        
        # Create embeddings
        self.embedder.create_embeddings(str(chunks_file))
        
        # Verify embeddings were created
        results = self.embedder.collection.get(include=['embeddings', 'documents', 'metadatas'])
        self.assertEqual(len(results['ids']), 2)
        self.assertEqual(results['ids'], ['test1', 'test2'])
        self.assertEqual(results['documents'], [self.sample_chunks['chunks'][0]['text'], self.sample_chunks['chunks'][1]['text']])
        self.assertEqual(results['metadatas'][0]['source'], 'test_source.pdf')
        self.assertEqual(results['metadatas'][1]['source'], 'test_source.pdf')
        self.assertIsNotNone(results['embeddings'])
        self.assertEqual(len(results['embeddings']), 2)

if __name__ == '__main__':
    unittest.main() 