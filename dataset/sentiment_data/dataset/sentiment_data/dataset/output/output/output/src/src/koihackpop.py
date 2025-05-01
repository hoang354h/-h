import json
import random
from src.update_trendy import update_trendy
from collections import deque
from src.sentiment import analyze_sentiment
from llama_cpp import Llama
import torch

comment_cache = deque(maxlen=5)
llm = Llama(
    model_path="D:\\KoiHackBop\\dataset\\phogpt-4b-chat-q4_k_m.gguf",
    n_ctx=512,
    n_gpu_layers=20,
    n_threads=8,
    seed=42
)

def save_unknown_comment(comment, response):
    unknown_file = "D:\\KoiHackBop\\output\\unknown_comments.json"
    try:
        with open(unknown_file, "r", encoding="utf-8") as f:
            unknown_data = json.load(f)
    except FileNotFoundError:
        unknown_data = []
    unknown_data.append({"input": comment, "output": response})
    with open(unknown_file, "w", encoding="utf-8") as f:
        json.dump(unknown_data, f, ensure_ascii=False, indent=2)

def update_dataset():
    unknown_file = "D:\\KoiHackBop\\output\\unknown_comments.json"
    dataset_file = "D:\\KoiHackBop\\dataset\\koihackpop_data\\train.json"
    try:
        with open(unknown_file, "r", encoding="utf-8") as f:
            unknown_data = json.load(f)
        with open(dataset_file, "r", encoding="utf-8") as f:
            dataset = json.load(f)
        dataset.extend(unknown_data)
        with open(dataset_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        print("Updated dataset with new comments!")
    except FileNotFoundError:
        print("No unknown comments to update.")

async def generate_koihackpop_response(comment, gift_amount):
    comment_cache.append(comment)
    sentiment = analyze_sentiment(comment)
    style = random.choice(["drama", "cute", "troll"])
    with open("D:\\KoiHackBop\\dataset\\koihackpop_data\\train.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    matching_responses = [
        item["output"] for item in data
        if comment.lower() in item["input"].lower() and item["sentiment"] == sentiment and item["style"] == style
    ]
    if matching_responses:
        return random.choice(matching_responses)
    
    trending = update_trendy()
    context = " ".join(comment_cache)
    keywords = [word for word in context.split() if len(word) > 3][:2]
    
    if "?" in comment and random.random() < 0.3:
        responses = [
            f"Haha, {comment}? Tui không trả lời đâu, đoán xu đi cho tui vui! {random.choice(trending)}",
            f"Ủa, {comment}? Câu này khó, tui giả vờ không nghe nha! #KoiHackPop",
            f"{comment}? Tui bận drama, hỏi xu ở đâu đi, tui trả lời liền! {random.choice(trending)}"
        ]
        response = random.choice(responses)
    else:
        prompt = (
            f"Bạn là KoiHackPop, một VTuber yandere với tính cách dramatic, cute, hoặc troll. "
            f"Trả lời '{comment}' với sentiment '{sentiment}' và style '{style}'. "
            f"Sử dụng từ khóa: {' '.join(keywords)}. Hãy viral, dí dỏm, tự nhiên bằng tiếng Việt: "
        )
        response = llm(
            prompt,
            max_tokens=50,
            temperature=0.7,
            top_p=0.9,
            stop=["\n"]
        )["choices"][0]["text"]
        response = f"{response.strip()} {random.choice(trending)}"
    
    save_unknown_comment(comment, response)
    torch.cuda.empty_cache()
    return response
