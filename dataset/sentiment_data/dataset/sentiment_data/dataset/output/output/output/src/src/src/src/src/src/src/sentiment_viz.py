import json

def update_emotion_sphere(sentiment, score):
    with open("D:\\KoiHackBop\\output\\score.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    html_content = html_content.replace(f"KoiHackPop: {score-1 if score > 0 else 0}", f"KoiHackPop: {score}")
    with open("D:\\KoiHackBop\\output\\score.html", "w", encoding="utf-8") as f:
        f.write(html_content)
