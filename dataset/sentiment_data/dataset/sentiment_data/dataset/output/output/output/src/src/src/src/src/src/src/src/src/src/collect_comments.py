import json
import re
import asyncio
from TikTokLive import TikTokLiveClient
from src.koihackpop import generate_koihackpop_response
from src.vits import generate_speech
from src.vtube import update_vtuber
from src.sentiment import analyze_sentiment
from src.sentiment_viz import update_emotion_sphere
from src.minigame import play_treasure_hunt

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def save_comments(comments):
    with open("D:\\KoiHackBop\\output\\interaction_history.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

async def collect_comments():
    client = TikTokLiveClient(unique_id="@YourTikTokID")
    comments = []

    @client.on("comment")
    async def on_comment(event):
        content = clean_text(event.comment.text)
        if len(content) > 5:
            gift_amount = event.gift.amount if event.gift else 0
            comment_data = {"content": content, "gift_amount": gift_amount}
            comments.append(comment_data)
            save_comments(comments)
            
            sentiment = analyze_sentiment(content)
            response = await generate_koihackpop_response(content, gift_amount)
            audio_file = generate_speech(response, sentiment, "koihackpop")
            scores = play_treasure_hunt([comment_data])
            
            update_vtuber(sentiment, "koihackpop", is_reading=True)
            update_emotion_sphere(sentiment, scores["koihackpop"])
            update_vtuber(sentiment, "koihackpop", is_reading=False)
            
            print(f"[KoiHackPop] {content} -> {response} (Sentiment: {sentiment}, Score: {scores['koihackpop']})")

    @client.on("gift")
    async def on_gift(event):
        if event.gift:
            content = f"Fan tặng {event.gift.name}!"
            gift_amount = event.gift.amount
            comment_data = {"content": content, "gift_amount": gift_amount}
            comments.append(comment_data)
            save_comments(comments)
            
            sentiment = analyze_sentiment(content)
            response = await generate_koihackpop_response(content, gift_amount)
            audio_file = generate_speech(response, sentiment, "koihackpop")
            scores = play_treasure_hunt([comment_data])
            
            update_vtuber(sentiment, "koihackpop", is_reading=True)
            update_emotion_sphere(sentiment, scores["koihackpop"])
            update_vtuber(sentiment, "koihackpop", is_reading=False)
            
            print(f"[KoiHackPop] {content} -> {response} (Sentiment: {sentiment}, Score: {scores['koihackpop']})")

    await client.start()
    try:
        await asyncio.sleep(3600)
    finally:
        await client.stop()
    return comments

if __name__ == "__main__":
    asyncio.run(collect_comments())
