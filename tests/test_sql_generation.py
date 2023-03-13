from helpers import generate_word_addition

class TestSQLGeneration:
    def test_1(self):
        with open('tests/output_1.txt', encoding='utf-8') as f:
            text = f.readlines()
            text = ''.join(text)
        
        out = generate_word_addition("deçà")
        assert text == out, "Incorrect SQL generation"
