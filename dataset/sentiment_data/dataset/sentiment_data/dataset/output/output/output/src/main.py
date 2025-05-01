import asyncio
import json
from src.sentiment import analyze_sentiment
from src.koihackpop import generate_koihackpop_response
from src.vits import generate_speech
from src.vtube import update_vtuber
from src.sentiment_viz import update_emotion_sphere
from src.minigame import play_treasure_hunt
from src.model_manager import ModelManager
from src.collect_comments import collect_comments

def save_history(comments, responses, sentiments):
    history_file = "D:\\KoiHackBop\\dataset\\koihackpop_data\\history.json"
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    for c, r, s in zip(comments, responses, sentiments):
        history.append({
            "input": c["content"],
            "output": r,
            "sentiment": s,
            "gift_amount": c["gift_amount"],
            "weight": 1 + c["gift_amount"] // 1000
        })
    history = sorted(history, key=lambda x: x["weight"], reverse=True)[:1000]
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

async def process_comments(comments):
    model_manager = ModelManager()
    model_manager.clear_cache()
    
    sentiments = [analyze_sentiment(c["content"]) for c in comments]
    responses = [await generate_koihackpop_response(c["content"], c["gift_amount"]) for c in comments]
    audio_files = [generate_speech(r, s, "koihackpop") for r, s in zip(responses, sentiments)]
    
    scores = play_treasure_hunt(comments)
    for s, r in zip(sentiments, responses):
        update_vtuber(s, "koihackpop", is_reading=True)
        update_emotion_sphere(s, scores["koihackpop"])
        update_vtuber(s, "koihackpop", is_reading=False)
    
    save_history(comments, responses, sentiments)
    model_manager.clear_cache()
    return responses, sentiments, audio_files

async def run_livestream():
    print("Starting KoiHackPop livestream with TikTok integration...")
    await collect_comments()

if __name__ == "__main__":
    asyncio.run(run_livestream())
