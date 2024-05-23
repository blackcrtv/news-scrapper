from transformers import pipeline

#from spacy.lang.ro.examples import sentences 

#FacebookAI/xlm-roberta-large-finetuned-conll03-english
class TextProcessor:
    def __init__(self, summarization_model="Iulian277/ro-bart-1024", token_classification_model="51la5/roberta-large-NER"):
        self.summarizer = pipeline("summarization", model=summarization_model)
        self.classifier = pipeline("token-classification", model=token_classification_model)


    def preprocess_text(self, text):
        replacements = {"ţ": "ț", "ş": "ș", "Ţ": "Ț", "Ş": "Ș"}
        return text.translate(str.maketrans(replacements))

    def summarize(self, text):
        preprocessed_text = self.preprocess_text(text)
        return self.summarizer(preprocessed_text)[0]['summary_text']

    def tokenize(self, text):
        preprocessed_text = self.preprocess_text(text)
        return self.classifier(preprocessed_text)

    def mark_entities(self, text, ner_results):
        sorted_entities = sorted(ner_results, key=lambda x: x['start'])
        marked_text = ""
        last_idx = 0

        for entity in sorted_entities:
            start = entity['start']
            end = entity['end']
            label = entity['entity']

            marked_text += text[last_idx:start]
            marked_text += f"[{text[start:end]} ({label})]"
            last_idx = end

        marked_text += text[last_idx:]
        return marked_text