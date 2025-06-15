"""
Tests for the Embedder class
"""
import unittest
import json
import os
from pathlib import Path
from agent.embedder import Embedder

class TestEmbedder(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.embedder = Embedder()
        # Clear the collection before each test
        self.embedder.collection.delete(where={})
        
        self.sample_chunks = {
            'chunks': [
                {
                    'chunk_id': 'test1',
                    'text': 'Sample FAQ text 1',
                    'source': 'test_source.pdf',
                    'char_length': 15
                },
                {
                    'chunk_id': 'test2',
                    'text': 'Sample FAQ text 2',
                    'source': 'test_source.pdf',
                    'char_length': 15
                }
            ]
        }
        # Create temporary chunks file
        self.chunks_file = Path("test_chunks.json")
        with open(self.chunks_file, 'w', encoding='utf-8') as f:
            json.dump(self.sample_chunks, f)

    def tearDown(self):
        """Clean up test fixtures"""
        # Clear the collection after each test
        self.embedder.collection.delete(where={})
        if self.chunks_file.exists():
            self.chunks_file.unlink()

    def test_verify_index_empty(self):
        """Test verify_index on an empty collection"""
        status = self.embedder.verify_index()
        
        self.assertEqual(status['total_chunks'], 0)
        self.assertEqual(status['sources'], [])
        self.assertFalse(status['has_embeddings'])
        expected_path = os.path.normpath(os.path.join('data', 'embeddings'))
        self.assertTrue(status['persistence_path'].endswith(expected_path))

    def test_verify_index_with_chunks(self):
        """Test verify_index after adding chunks"""
        # Create embeddings
        self.embedder.create_embeddings(str(self.chunks_file))
        
        # Verify index
        status = self.embedder.verify_index()
        
        self.assertEqual(status['total_chunks'], len(self.sample_chunks['chunks']))
        self.assertEqual(status['sources'], ['test_source.pdf'])
        self.assertTrue(status['has_embeddings'])
        expected_path = os.path.normpath(os.path.join('data', 'embeddings'))
        self.assertTrue(status['persistence_path'].endswith(expected_path))

if __name__ == '__main__':
    unittest.main() 