import pandas as pd

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

def save_to_csv(dataframe, file_path, columns):
    dataframe[columns].to_csv(file_path, index=False)