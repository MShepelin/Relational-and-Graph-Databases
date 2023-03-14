from helpers import generate_word_addition, generate_graph_word_addition

class TestSQLGeneration:
    def test_1(self):
        with open('tests/output_sql.txt', encoding='utf-8') as f:
            text = f.readlines()
            text = ''.join(text)
        
        out = generate_word_addition("deçà")
        assert text == out, "Incorrect SQL generation"

class TestCypherGeneration:
    def test_1(self):
        with open('tests/output_cypher.txt', encoding='utf-8') as f:
            text = f.readlines()
            text = ''.join(text)
        
        out = generate_graph_word_addition("deçà")
        assert text == out, "Incorrect Cypher generation"
