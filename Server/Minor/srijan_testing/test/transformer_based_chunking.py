import spacy
import pandas as pd
from transformers import pipeline

# Load transformer-based summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nlp = spacy.load("en_core_web_lg")

# Function to summarize long text into coherent chunks
def summarize_text(text, max_chunk_length=150):
    summaries = summarizer(text, max_length=max_chunk_length, min_length=30, do_sample=False)
    print(summaries)
    return [summary['summary_text'] for summary in summaries]

# Use summarized text as input for NER processing
def extract_entities(text_chunks):
    structured_data = []
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
    }

    for chunk in text_chunks:
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
        }
        for ent in doc.ents:
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
            else:
                entities["Misc"].append(entity_info)

        # Combine data into rows for structured output
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

    if any(current_row.values()):
        structured_data.append(current_row)

    return structured_data

# Convert extracted data into a table (DataFrame)
def convert_to_table(data):
    df = pd.DataFrame(data)
    return df

# Example usage
file_path = "sample1.txt"

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

text = read_text_file(file_path)

# Summarize large text into coherent chunks
summarized_chunks = summarize_text(text)
print("Summarized Chunks:", summarized_chunks)

# Process summarized chunks through NER
structured_data = extract_entities(summarized_chunks)
table = convert_to_table(structured_data)

# Save the structured data to CSV
print(table)
table.to_csv("structured_data.csv", index=False)
