from spacy import displacy
import pandas as pd

def visualize_relationships(docs):
    options = {"compact": True, "color": "blue", "bg": "#f0f0f0", "font": "Source Sans Pro"}
    svg_fragments = [displacy.render(doc, style="dep", options=options) for doc in docs]
    
    # Extract the inner content of each SVG fragment and combine them with spacing
    combined_svg_content = ""
    y_offset = 0
    for svg in svg_fragments:
        start_index = svg.find("<svg")
        end_index = svg.find("</svg>") + len("</svg>")
        svg_content = svg[start_index:end_index]
        
        # Adjust the y position of each SVG fragment
        svg_content = svg_content.replace('<svg', f'<svg y="{y_offset}"', 1)
        combined_svg_content += svg_content
        y_offset += 200  # Adjust this value to control the spacing between fragments
    
    # Wrap the combined content in a single SVG tag
    final_svg = f'<svg xmlns="http://www.w3.org/2000/svg" height="{y_offset}">{combined_svg_content}</svg>'
    
    with open("relationships.svg", "w", encoding="utf-8") as file:
        file.write(final_svg)

def convert_to_table(data):
    rows = []
    for entry in data:
        row = {
            "Person": ", ".join(entry["Person"]),
            "Org": ", ".join(entry["Org"]),
            "Date": ", ".join(entry["Date"]),
            "Loc": ", ".join(entry["Loc"]),
            "Misc": ", ".join(entry["Misc"]),
            "Money": ", ".join(entry["Money"]),
            "Percent": ", ".join(entry["Percent"]),
            "Time": ", ".join(entry["Time"]),
            "Quantity": ", ".join(entry["Quantity"]),
            "Ordinal": ", ".join(entry["Ordinal"]),
            "Cardinal": ", ".join(entry["Cardinal"]),
            "Product": ", ".join(entry["Product"]),
            "Relationships": "; ".join([f"{rel[0]} -> {rel[1]} -> {rel[2]}" for rel in entry["Relationships"]])
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df