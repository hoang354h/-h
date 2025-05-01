from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def finetune_phobert():
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
    model = AutoModelForSequenceClassification.from_pretrained("vinai/phobert-base").to("cuda")
    with open("D:\\KoiHackBop\\dataset\\sentiment_data\\train.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        inputs = tokenizer(item["text"], return_tensors="pt", truncation=True, max_length=256).to("cuda")
        labels = torch.tensor([{"vui": 0, "gian": 1, "hao_hung": 2}[item["label"]]]).to("cuda")
        # Fake finetune (thay bằng code thực trên Kaggle)
        print(f"Finetuning PhoBERT with {item['text']}")
    model.save_pretrained("D:\\KoiHackBop\\dataset\\phobert_model")
