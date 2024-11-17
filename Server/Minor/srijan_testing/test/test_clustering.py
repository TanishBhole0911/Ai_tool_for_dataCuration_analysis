import spacy
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

nlp = spacy.load("en_core_web_lg")

# Function to chunk text into contextually related parts
def context_aware_chunk(text, threshold=0.3):
    # Break the text into sentences first
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # Use TF-IDF to measure similarity between sentences
    vectorizer = TfidfVectorizer().fit_transform(sentences)
    vectors = vectorizer.toarray()
    
    # Compute pairwise cosine similarity
    cosine_sim = cosine_similarity(vectors)
    
    # Initialize chunks list
    chunks = []
    chunk = [sentences[0]]  # Start with the first sentence
    
    for i in range(1, len(sentences)):
        # Compare current sentence to the previous one
        if cosine_sim[i-1][i] > threshold:  # If similarity is above threshold, group together
            chunk.append(sentences[i])
        else:
            # Finalize current chunk and start a new one
            chunks.append(" ".join(chunk))
            print(f"Chunk created: {' '.join(chunk)}")  # Print each chunk
            chunk = [sentences[i]]
    
    # Append the last chunk
    if chunk:
        chunks.append(" ".join(chunk))
        print(f"Chunk created: {' '.join(chunk)}")  # Print the last chunk
    
    return chunks

# Same NER-based CSV creation process as before
def extract_entities(text_chunks):
    structured_data = []
    current_row = defaultdict(list)

    for chunk in text_chunks:
        doc = nlp(chunk)
        entities = defaultdict(list)

        # Extract entities and group by type
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)

        # Resolve conflicts and combine related chunks
        conflict = False
        for key in entities:
            if current_row[key] and entities[key]:
                conflict = True
                break

        if conflict:
            structured_data.append(dict(current_row))
            current_row = entities
        else:
            for key in entities:
                current_row[key].extend(entities[key])

    # Add last chunk to structured data
    if any(current_row.values()):
        structured_data.append(dict(current_row))

    return structured_data

# Convert to a Pandas DataFrame and save as CSV
def convert_to_table(data):
    df = pd.DataFrame(data)
    return df

# Example usage
file_path = "sample1.txt"

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

text = read_text_file(file_path)
chunks = context_aware_chunk(text)  # Context-aware chunking
structured_data = extract_entities(chunks)
table = convert_to_table(structured_data)

print(table)
table.to_csv("structured_data.csv", index=False)