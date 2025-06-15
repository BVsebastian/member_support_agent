import unittest
import os
from agent.retriever import Retriever

class TestRetriever(unittest.TestCase): 
    def setUp(self):
        self.retriever = Retriever()
    
    def test_retriever_initialization(self):
        self.assertIsNotNone(self.retriever)
        self.assertEqual(self.retriever.collection.name, "faq_chunks")

    def test_retrieve_top_chunks(self):
        query = "How can I open an account?"
        results = self.retriever.retrieve_top_chunks(query)

        #Test 1: Check that we got results
        self.assertIsNotNone(results)

        #Test 2: Check that we got the default number of results (3)
        self.assertEqual(len(results), 3)

        #Test 3: Check the structure of each result
        for result in results:
            self.assertIn('text', result)
            self.assertIn('source', result)
            self.assertIn('char_length', result)
            self.assertIn('similarity_score', result)

            #Test 4: Check similarity score is between 0 and 1
            self.assertGreaterEqual(result['similarity_score'], 0)
            self.assertLessEqual(result['similarity_score'], 1)

    def test_retrieve_specific_content(self):
        """Test that specific queries return expected content"""
        query = "What documents do I need to open an account?"
        results = self.retriever.retrieve_top_chunks(query)
        
        # Check if results contain account opening info
        account_info_found = any(
            "Required documents" in result['text'] 
            for result in results
        )
        self.assertTrue(account_info_found, "Results should contain account opening requirements")

if __name__ == '__main__':
    unittest.main()