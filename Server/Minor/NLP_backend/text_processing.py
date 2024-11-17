from spacy import displacy

def chunk_text(text, nlp):
    doc = nlp(text)
    chunks = []
    for sent in doc.sents:
        chunks.append(sent.text)
        print(f"Chunk: {sent.text}")  # Print each chunk
    return chunks

def extract_entities_and_relationships(text_chunks, nlp):
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
        "Relationships": []
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

        # Extract relationships
        relationships = extract_relationships(doc)
        entities["Relationships"] = relationships

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

def extract_relationships(doc):
    relationships = []
    for token in doc:
        if token.dep_ in ("nsubj", "dobj", "pobj", "iobj"):
            subject = [w for w in token.head.lefts if w.dep_ == "nsubj"]
            if subject:
                subject = subject[0]
                relationships.append((subject.text, token.head.text, token.text))
    return relationships