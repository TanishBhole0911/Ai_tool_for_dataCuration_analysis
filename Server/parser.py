import spacy
from spacy.matcher import PhraseMatcher
import os
import re
# import time
   
class parser:
    def __init__(self, context_keywords):
        self.nlp = spacy.load("en_core_web_lg")
        self.matcher = PhraseMatcher(self.nlp.vocab)
        self.context_keywords = context_keywords
        context_patterns = [self.nlp.make_doc(text) for text in context_keywords]
        self.matcher.add("CONTEXT_TERMS", context_patterns)

    def clean_text(self, text):
        sentences = text.split('.')
        cleaned_sentences = []
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 1 and not (len(words) < 3 and words[0] == '- '):
                cleaned_sentences.append(sentence)
        cleaned_text = ' '.join(re.sub(r'[^A-Za-z0-9., ]+', '', ' '.join(cleaned_sentences)).split())
        return cleaned_text
    
    def filter_relevant_info(self,text):
        doc = self.nlp(text)
        relevant_sentences = []
        
        for sent in doc.sents:
            matches = self.matcher(sent)
            if matches:
                if any(keyword in sent.text for keyword in self.context_keywords):
                    relevant_sentences.append(sent.text)
        return relevant_sentences
    
    def remove_incoherent_and_repetitive(self,sentences):
        unique_sentences = list(set(sentences))  # Remove duplicates
        coherent_sentences = [sent for sent in unique_sentences if len(sent.split()) > 3]  # Remove incoherent sentences
        return coherent_sentences
    
    def open_file(self,file: str):
        with open(file, "r", encoding="utf-8") as file:
            scraped_data = file.read()
        return scraped_data
    
    def write_to_file(data: list):
        current_path = os.getcwd()
        output_file_path = os.path.join(current_path, "filtered_info.txt")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            for info in data:
                output_file.write(info+"\n")
        return output_file_path
    
    def parse_data(self,scraped_data_path: str):
        scraped_data = self.open_file(scraped_data_path)
        cleaned_data = self.clean_text(scraped_data)
        filtered_info = self.filter_relevant_info(cleaned_data)
        data = self.remove_incoherent_and_repetitive(filtered_info)
        # print(self.write_to_file(final_info))
        current_path = os.getcwd()
        output_file_path = os.path.join(current_path, "filtered_info.txt")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.writelines(info + '\n' for info in data)
        return output_file_path
            




# # Testing
# context_keywords = ["Apple", "iPhone", "stock price"]
# parser = parser(context_keywords)
# start_time = time.time()
# print(parser.parse_data(r"C:\Users\srija\Documents\GitHub\Minor\Server\dataset_20241021_115734.txt"))
# end_time = time.time()

# print(f"Execution time: {end_time - start_time} seconds")