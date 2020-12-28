import datetime
import unittest
from va_assistant import VoiceAssistant, correct_numerals, numerals_reconciliation
from datetime import datetime, timedelta


class TestAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = VoiceAssistant()
        self.assistant.active = False
        self.assistant.sec_to_offline = 40

    def test_correct_numerals(self):
        self.assertEqual(correct_numerals('1 минута'), 'одна минута')
        self.assertEqual(correct_numerals('1 вдох'), 'один вдох')

    def test_numerals_reconciliation(self):
        self.assertEqual((numerals_reconciliation(phrase='2 час 11 минута 21 секунда'), '2 часа 11 минут 21 секунда'))
        self.assertEqual((numerals_reconciliation(phrase='5 час 4 минута 9 секунда'), '5 часов 4 минуты 9 секунд'))

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
