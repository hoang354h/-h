import torch
from transformers import VitsModel, AutoTokenizer
import soundfile as sf

model = VitsModel.from_pretrained("D:\\KoiHackBop\\dataset\\vits_model").to("cuda")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")

def generate_speech(text, sentiment, personality):
    inputs = tokenizer(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        audio = model(**inputs).waveform.squeeze().cpu().numpy()
    output_file = f"D:\\KoiHackBop\\dataset\\vits\\vivos_custom\\audio_{int(torch.randint(1000, 9999, (1,)))}.wav"
    sf.write(output_file, audio, 22050)
    
    transcript_file = "D:\\KoiHackBop\\dataset\\vits\\vivos_custom\\transcript.txt"
    with open(transcript_file, "a", encoding="utf-8") as f:
        f.write(f"{output_file.split('/')[-1]}|{text}\n")
    
    return output_file
