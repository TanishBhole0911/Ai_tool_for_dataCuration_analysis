import json

def convert_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    converted_data = []
    for entry in data:
        text = entry["text"]
        entities = entry["entities"]
        entity_tuples = [(start, end, label) for start, end, label in entities]
        converted_data.append((text, {"entities": entity_tuples}))

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(converted_data, file, indent=4)

if __name__ == "__main__":
    input_file = "training_data.json"
    output_file = "converted_data.json"
    convert_json(input_file, output_file)
    print(f"Converted data saved to {output_file}")