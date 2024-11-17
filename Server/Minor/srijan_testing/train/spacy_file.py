import os
import json
import spacy
from tqdm import tqdm
from spacy.tokens import DocBin

# Load the spaCy model
nlp = spacy.load("en_core_web_trf")  # load other spacy model

# Load the training data
with open("converted_data.json", "r", encoding="utf-8") as file:
    TRAIN_DATA = json.load(file)

db = DocBin()  # create a DocBin object

for text, annot in tqdm(TRAIN_DATA):  # data in previous format
    doc = nlp.make_doc(text)  # create doc object from text
    ents = []
    for start, end, label in annot["entities"]:  # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print(f"Skipping entity in text: {text[start:end]}")
        else:
            ents.append(span)
            print(f"Entity: {span.text}, Label: {label}, Start: {start}, End: {end}")
    doc.ents = ents  # label the text with the ents
    db.add(doc)
    print(f"Processed text: {text}")
    print(f"Entities: {[(ent.text, ent.label_) for ent in ents]}")
    print("-" * 80)

# Save the DocBin object
output_path = "./train.spacy"
db.to_disk(output_path)
print(f"Training data saved to {output_path}")