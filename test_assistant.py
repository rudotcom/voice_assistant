import datetime
import unittest
from va_assistant import VoiceAssistant
from datetime import datetime, timedelta


class TestAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = VoiceAssistant()
        self.assistant.active = False
        self.assistant.sec_to_offline = 40

    def test_pays_attention(self):
        self.assertEqual(self.assistant.pays_attention(phrase='что как'), False)
        self.assertEqual(self.assistant.pays_attention(phrase='мурзилка что как'), True)

    def test_is_alert(self):
        self.assistant.last_active = datetime.now() - timedelta(seconds=self.assistant.sec_to_offline)
        self.assertEqual((self.assistant.is_alert()), False)

        self.assistant.last_active = datetime.now()
        self.assertEqual((self.assistant.is_alert()), True)

    def test_sleep(self):
        self.assertEqual(self.assistant.sleep(), self.assistant.recognition_mode == 'offline')
        self.assertEqual(self.assistant.sleep(), self.assistant.active is False)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
