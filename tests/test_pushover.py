from app.pushover_alerts import record_user_details, record_unknown_question, push
import unittest

def test_push():
    push("test")

def test_record_user_details():
    record_user_details("test@test.com", "test", "test")

def test_record_unknown_question():
    record_unknown_question("test")

if __name__ == "__main__":
    test_push()
    test_record_user_details()
    test_record_unknown_question()

