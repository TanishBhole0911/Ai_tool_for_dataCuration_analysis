# minor/nlp_backend/main.py

from .file_utils import read_text_file, save_to_csv
from .text_processing import chunk_text, extract_entities_and_relationships
from .visualization import visualize_relationships, convert_to_table
import spacy
import os

# Load the transformer-based model
nlp = spacy.load("en_core_web_sm")

# Add necessary components to the pipeline if not already present
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")
if "parser" not in nlp.pipe_names:
    nlp.add_pipe("parser")

def process_nlp(file, columns_to_save):
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found.")
    
    text = read_text_file(file)  # Update to read from file object
    chunks = chunk_text(text, nlp)
    structured_data = extract_entities_and_relationships(chunks, nlp)

    # Collect all docs for visualization
    docs = [nlp(chunk) for chunk in chunks]

    # Visualize all relationships in a single SVG
    visualize_relationships(docs)

    table = convert_to_table(structured_data)

    # Specify the columns to save
    # columns_to_save = ["Person", "Org", "Date", "Loc","Money","Quantity", "Relationships"]
    csv_filename = "structured_data.csv"
    save_to_csv(table, csv_filename, columns_to_save)

    return "relationships.svg", csv_filename  # Return paths to SVG and CSV files

# from file_utils import read_text_file, save_to_csv
# from text_processing import chunk_text, extract_entities_and_relationships
# from visualization import visualize_relationships, convert_to_table
# import spacy

# # Load the transformer-based model
# nlp = spacy.load("en_core_web_trf")

# # Add the sentencizer and dependency parser components to the pipeline
# if "sentencizer" not in nlp.pipe_names:
#     nlp.add_pipe("sentencizer")
# if "parser" not in nlp.pipe_names:
#     nlp.add_pipe("parser")

# file_path = "/Users/srishti/Desktop/Server/Minor/NLP_backend/sample1.txt"

# text = read_text_file(file_path)
# chunks = chunk_text(text, nlp)
# structured_data = extract_entities_and_relationships(chunks, nlp)

# # Collect all docs for visualization
# docs = [nlp(chunk) for chunk in chunks]

# # Visualize all relationships in a single SVG
# visualize_relationships(docs)

# table = convert_to_table(structured_data)

# print(table)

# # Specify the columns to save
# columns_to_save = ["Person", "Org", "Date", "Loc", "Relationships"]
# save_to_csv(table, "structured_data.csv", columns_to_save)
