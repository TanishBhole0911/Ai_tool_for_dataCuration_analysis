import spacy
import pandas as pd
from spacy import displacy
import time
import unittest

# Load the transformer-based model
nlp = spacy.load("en_core_web_trf")

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def chunk_text(text):
    doc = nlp(text)
    chunks = []
    for sent in doc.sents:
        chunks.append(sent.text)
        print(f"Chunk: {sent.text}")  # Print each chunk
    return chunks

def extract_entities(text_chunks):
    structured_data = []
    all_html = ""
    current_row = {
        "Person": [],
        "Org": [],
        "Date": [],
        "Loc": [],
        "Misc": [],
        "Money": [],
        "Percent": [],
        "Time": [],
        "Quantity": [],
        "Ordinal": [],
        "Cardinal": [],
        "Product": [],
    }

    for i, chunk in enumerate(text_chunks):
        doc = nlp(chunk)
        entities = {
            "Person": [],
            "Org": [],
            "Date": [],
            "Loc": [],
            "Misc": [],
            "Money": [],
            "Percent": [],
            "Time": [],
            "Quantity": [],
            "Ordinal": [],
            "Cardinal": [],
            "Product": [],
        }
        for ent in doc.ents:  # Named Entity Recognition
            entity_info = ent.text
            if ent.label_ == "PERSON":
                entities["Person"].append(entity_info)
            elif ent.label_ == "ORG":
                entities["Org"].append(entity_info)
            elif ent.label_ == "DATE":
                entities["Date"].append(entity_info)
            elif ent.label_ == "GPE":
                entities["Loc"].append(entity_info)
            elif ent.label_ == "MONEY":
                entities["Money"].append(entity_info)
            elif ent.label_ == "PERCENT":
                entities["Percent"].append(entity_info)
            elif ent.label_ == "TIME":
                entities["Time"].append(entity_info)
            elif ent.label_ == "QUANTITY":
                entities["Quantity"].append(entity_info)
            elif ent.label_ == "ORDINAL":
                entities["Ordinal"].append(entity_info)
            elif ent.label_ == "CARDINAL":
                entities["Cardinal"].append(entity_info)
            elif ent.label_ == "PRODUCT":
                entities["Product"].append(entity_info)
            else:
                entities["Misc"].append(entity_info)

        # Check for conflicts and add to structured_data
        conflict = False
        for key in entities:
            if current_row[key] and entities[key]:
                conflict = True
                break

        if conflict:
            structured_data.append(current_row)
            current_row = entities
        else:
            for key in entities:
                current_row[key].extend(entities[key])

        # Visualize entities using displacy and concatenate HTML
        html = displacy.render(doc, style="ent", page=True)
        all_html += html

    # Add the last row
    if any(current_row.values()):
        structured_data.append(current_row)

    # Save all visualizations to a single HTML file
    with open("entities_all_chunks.html", "w", encoding="utf-8") as file:
        file.write(all_html)

    return structured_data

def convert_to_table(data):
    df = pd.DataFrame(data)
    return df

file_path = "sample1.txt"

text = read_text_file(file_path)
chunks = chunk_text(text)
structured_data = extract_entities(chunks)
table = convert_to_table(structured_data)

print(table)
table.to_csv("structured_data.csv", index=False)

# class TestEntityExtractor(unittest.TestCase):

#     def setUp(self):
#         self.text = read_text_file(file_path)
#         self.chunks = chunk_text(self.text)

#     def test_chunking(self):
#         self.assertGreater(len(self.chunks), 0, "Chunking failed, no chunks created.")

#     def test_entity_extraction(self):
#         structured_data = extract_entities(self.chunks)
#         self.assertGreater(len(structured_data), 0, "Entity extraction failed, no entities found.")

#     def test_performance(self):
#         start_time = time.time()
#         extract_entities(self.chunks)
#         end_time = time.time()
#         duration = end_time - start_time
#         self.assertLess(duration, 5, "Entity extraction is too slow.")

#     def test_accuracy(self):
#         structured_data = extract_entities(self.chunks)
#         # Update the known entities to match the actual content of sample.txt
#         known_entities = {
#             "Person": ["David Curry"],
#             "Org": ["OpenAI", "Google", "Microsoft", "Amazon"],
#             "Date": ["January 2023", "2023", "next year"],
#             "Loc": ["San Francisco", "New York City", "Mount Everest", "K2", "Mount Kilimanjaro"],
#             "Money": ["$120,000"],
#             "Percent": ["50%"],
#             "Time": ["9 AM", "5 PM"],
#             "Quantity": ["1,000"],
#             "Ordinal": [],
#             "Cardinal": [],
#         }
#         for entity_type, entities in known_entities.items():
#             for entity in entities:
#                 self.assertIn(entity, structured_data[0][entity_type], f"Entity {entity} not found in {entity_type}.")

# if __name__ == "__main__":
#     unittest.main()