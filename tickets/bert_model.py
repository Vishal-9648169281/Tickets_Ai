from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "distilbert-base-uncased"

_tokenizer = None
_model = None

def load_model():
    global _tokenizer, _model
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    return _tokenizer, _model


def predict_category(text):
    tokenizer, model = load_model()

    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    confidence, predicted = torch.max(probs, dim=1)

    categories = ["Network", "Software", "Hardware", "Access"]
    return categories[predicted.item()], confidence.item()

