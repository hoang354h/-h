from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
model = AutoModelForSequenceClassification.from_pretrained("D:\\KoiHackBop\\dataset\\phobert_model").to("cuda")

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256).to("cuda")
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    sentiment_id = torch.argmax(probs, dim=-1).item()
    sentiment_map = {0: "vui", 1: "gian", 2: "hao_hung"}
    return sentiment_map.get(sentiment_id, "vui")
