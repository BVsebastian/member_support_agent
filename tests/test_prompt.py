import unittest
from app.prompt_manager import get_system_prompt, load_identity_profile

class TestPromptManager(unittest.TestCase):
    def test_identity_profile_loading(self):
        """Test that identity profile can be loaded"""
        identity = load_identity_profile()
        self.assertIsInstance(identity, str)
        self.assertTrue(len(identity) > 0)

    def test_system_prompt_format(self):
        """Test that system prompt contains required elements"""
        prompt = get_system_prompt()
        
        # Check for key phrases
        self.assertIn("Alexa", prompt)
        self.assertIn("Horizon Bay Credit Union", prompt)
        self.assertIn("Virtual Member Support Representative", prompt)
        
        # Check for important guidelines
        self.assertIn("professional, friendly tone", prompt)
        self.assertIn("Never disclose that you are an AI", prompt)
        self.assertIn("record_unknown_question()", prompt)
        self.assertIn("record_user_details()", prompt)
        self.assertIn("sensitive data", prompt)
        self.assertIn("member security and privacy", prompt)

if __name__ == '__main__':
    unittest.main()
