from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load tokenizer and model (pretrained)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=4
)

# Labels for prediction
LABELS = ["Network", "Software", "Hardware", "Access"]

def predict_category(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)
    confidence, predicted_class = torch.max(probabilities, dim=1)

    return LABELS[predicted_class.item()], confidence.item()
