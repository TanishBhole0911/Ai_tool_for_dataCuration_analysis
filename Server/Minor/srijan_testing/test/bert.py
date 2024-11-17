from transformers import pipeline
import pandas as pd
import time
import unittest

# Initialize the transformer model for NER
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def extract_entities(text):
    entities = ner_pipeline(text)
    structured_data = {
        "Entity": [],
        "Type": []
    }
    for entity in entities:
        structured_data["Entity"].append(entity["word"])
        structured_data["Type"].append(entity["entity_group"])
    return structured_data

def convert_to_table(data):
    df = pd.DataFrame(data)
    return df

file_path = "sample.txt"

text = read_text_file(file_path)
structured_data = extract_entities(text)
table = convert_to_table(structured_data)

print(table)
table.to_csv("structured_data_BERT.csv", index=False)

class TestEntityExtractor(unittest.TestCase):

    def setUp(self):
        self.text = read_text_file(file_path)

    def test_entity_extraction(self):
        structured_data = extract_entities(self.text)
        self.assertGreater(len(structured_data["Entity"]), 0, "Entity extraction failed, no entities found.")

if __name__ == "__main__":
    unittest.main()
