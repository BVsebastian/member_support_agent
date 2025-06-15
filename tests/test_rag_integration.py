"""
Integration tests for the RAG pipeline
"""
import unittest
import os
from pathlib import Path
from agent.embedder import Embedder
from agent.retriever import Retriever

class TestRAGIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.embedder = Embedder()
        self.retriever = Retriever()
        # Clear the collection before each test
        all_ids = self.embedder.collection.get()['ids']
        if all_ids:
            self.embedder.collection.delete(ids=all_ids)

    def tearDown(self):
        """Clean up test fixtures"""
        # Clear the collection after each test
        all_ids = self.embedder.collection.get()['ids']
        if all_ids:
            self.embedder.collection.delete(ids=all_ids)

    def test_embedder_retriever_integration(self):
        """Test that embedded chunks can be retrieved"""
        # Create embeddings
        self.embedder.create_embeddings()
        
        # Try to retrieve
        results = self.retriever.retrieve_top_chunks("test query")
        
        self.assertGreater(len(results), 0, "Should retrieve at least one result")
        
        # Verify result structure
        for result in results:
            self.assertIn('text', result)
            self.assertIn('source', result)
            self.assertIn('char_length', result)
            self.assertIn('similarity_score', result)

    def test_edge_cases(self):
        """Test edge cases for retrieval"""
        # Create embeddings first
        self.embedder.create_embeddings()
        
        # Test empty query
        empty_results = self.retriever.retrieve_top_chunks("")
        self.assertEqual(len(empty_results), 3, "Empty query should still return default number of results")
        
        # Test very long query
        long_query = "test " * 100
        long_results = self.retriever.retrieve_top_chunks(long_query)
        self.assertEqual(len(long_results), 3, "Long query should return default number of results")
        
        # Test query with special characters
        special_query = "!@#$%^&*()_+{}|:<>?~`"
        special_results = self.retriever.retrieve_top_chunks(special_query)
        self.assertEqual(len(special_results), 3, "Special characters query should return default number of results")

if __name__ == '__main__':
    unittest.main() 