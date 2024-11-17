import unittest
import time
from file_utils import read_text_file
from text_processing import chunk_text, extract_entities_and_relationships

class TestEntityExtractor(unittest.TestCase):

    def setUp(self):
        self.file_path = "sample1.txt"
        self.text = read_text_file(self.file_path)
        self.chunks = chunk_text(self.text)

    def test_chunking(self):
        self.assertGreater(len(self.chunks), 0, "Chunking failed, no chunks created.")

    def test_entity_extraction(self):
        structured_data = extract_entities_and_relationships(self.chunks)
        self.assertGreater(len(structured_data), 0, "Entity extraction failed, no entities found.")

    def test_performance(self):
        start_time = time.time()
        extract_entities_and_relationships(self.chunks)
        end_time = time.time()
        duration = end_time - start_time
        self.assertLess(duration, 5, "Entity extraction is too slow.")

    def test_accuracy(self):
        structured_data = extract_entities_and_relationships(self.chunks)
        # Update the known entities to match the actual content of sample.txt
        known_entities = {
            "Person": ["David Curry"],
            "Org": ["OpenAI", "Google", "Microsoft", "Amazon"],
            "Date": ["January 2023", "2023", "next year"],
            "Loc": ["San Francisco", "New York City", "Mount Everest", "K2", "Mount Kilimanjaro"],
            "Money": ["$120,000"],
            "Percent": ["50%"],
            "Time": ["9 AM", "5 PM"],
            "Quantity": ["1,000"],
            "Ordinal": [],
            "Cardinal": [],
        }
        for entity_type, entities in known_entities.items():
            for entity in entities:
                self.assertIn(entity, structured_data[0][entity_type], f"Entity {entity} not found in {entity_type}.")

if __name__ == "__main__":
    unittest.main()