import torch
from transformers import VitsModel, AutoTokenizer
import json

def finetune_vits():
    model = VitsModel.from_pretrained("facebook/mms-tts-vie").to("cuda")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")
    with open("D:\\KoiHackBop\\dataset\\vits\\vivos_custom\\transcript.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        audio_file, text = line.strip().split("|")
        inputs = tokenizer(text, return_tensors="pt").to("cuda")
        audio = torch.tensor(sf.read(f"D:\\KoiHackBop\\dataset\\vits\\vivos_custom\\{audio_file}")[0]).to("cuda")
        # Fake finetune (thay bằng code thực trên Kaggle)
        print(f"Finetuning VITS with {audio_file}")
    model.save_pretrained("D:\\KoiHackBop\\dataset\\vits_model")
