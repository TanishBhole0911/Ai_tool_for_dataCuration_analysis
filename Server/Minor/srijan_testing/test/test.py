import spacy
import pandas as pd
from collections import defaultdict

# Load NER model
nlp = spacy.load("en_core_web_lg")

# Step 1: Extract all entities and their relationships
def extract_entities(text):
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_  # Correct key is "label"
        })
    return entities

# Step 2: Create chunks based on entity coherence
def create_chunks(text, entity_list, max_chunk_size=3):
    chunks = []
    current_chunk = []
    
    for entity in entity_list:
        current_chunk.append(entity)

        # If the chunk reaches the max size, append it and start a new chunk
        if len(current_chunk) >= max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = []

    # Append the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Step 3: Map entities into predefined user attributes
def map_to_attributes(entity_chunks):
    structured_data = []
    
    for chunk in entity_chunks:
        current_row = defaultdict(list)
        
        for entity in chunk:
            label = entity["label"]  # Correct key is "label"
            text = entity["text"]

            if label == "PERSON":
                current_row["Person"].append(text)
            elif label == "ORG":
                current_row["Org"].append(text)
            elif label == "DATE":
                current_row["Date"].append(text)
            elif label == "GPE":
                current_row["Loc"].append(text)
            elif label == "MONEY":
                current_row["Money"].append(text)
            elif label == "PERCENT":
                current_row["Percent"].append(text)
            elif label == "TIME":
                current_row["Time"].append(text)
            elif label == "QUANTITY":
                current_row["Quantity"].append(text)
            elif label == "ORDINAL":
                current_row["Ordinal"].append(text)
            elif label == "CARDINAL":
                current_row["Cardinal"].append(text)
            else:
                current_row["Misc"].append(text)

        structured_data.append(dict(current_row))

    return structured_data

# Convert the structured data into a DataFrame
def convert_to_table(data):
    df = pd.DataFrame(data)
    return df

# Example usage
file_path = "sample1.txt"

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Example usage flow
text = read_text_file(file_path)

# Step 1: Extract entities
entities = extract_entities(text)

# Step 2: Create coherent chunks of entities based on relationships
entity_chunks = create_chunks(text, entities, max_chunk_size=3)

# Step 3: Map entities to user-defined attributes
structured_data = map_to_attributes(entity_chunks)

# Step 4: Convert to DataFrame
table = convert_to_table(structured_data)

# Save the structured data to CSV
print(table)
table.to_csv("structured_data1.csv", index=False)