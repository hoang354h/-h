import json

def play_treasure_hunt(comments):
    with open("D:\\KoiHackBop\\dataset\\minigame_score.json", "r", encoding="utf-8") as f:
        scores = json.load(f)
    total_gifts = sum(c["gift_amount"] for c in comments)
    difficulty = min(3, 1 + total_gifts // 5000)
    for comment in comments:
        if "trái" in comment["content"] or "phải" in comment["content"]:
            scores["koihackpop"] += (1 + (comment["gift_amount"] // 1000)) // difficulty
    with open("D:\\KoiHackBop\\dataset\\minigame_score.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)
    return scores
