import spacy
from spacy.training.example import Example
from spacy.util import minibatch
import random
import json

# Load the pre-trained model
nlp = spacy.load("en_core_web_trf")

# Load your training data
with open("training_data.json", "r", encoding="utf-8") as file:
    TRAIN_DATA = json.load(file)

# Disable other pipeline components to only focus on 'ner'
ner = nlp.get_pipe("ner")

# Add new labels to the model (ensure all your entity labels are included)
for _, annotations in TRAIN_DATA:
    for ent in annotations['entities']:
        ner.add_label(ent[2])

# Remove other components from the pipeline during training for efficiency
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

# Begin training
with nlp.disable_pipes(*unaffected_pipes):
    optimizer = nlp.resume_training()  # Use resume_training to continue training the transformer model
    for iteration in range(20):  # Number of iterations
        random.shuffle(TRAIN_DATA)
        losses = {}
        
        # Batch the examples and loop over them
        batches = minibatch(TRAIN_DATA, size=spacy.util.compounding(4.0, 32.0, 1.001))
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], losses=losses, drop=0.3, sgd=optimizer)
        
        print(f"Iteration {iteration+1}, Losses: {losses}")

# Save the trained model
output_dir = "./trained_model"
nlp.to_disk(output_dir)
print(f"Model saved to {output_dir}")

# Testing the model
test_text = "Pfizer and BioNTech developed a COVID-19 vaccine in record time."
doc = nlp(test_text)
print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
