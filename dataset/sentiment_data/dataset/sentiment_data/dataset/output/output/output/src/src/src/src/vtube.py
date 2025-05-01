import time

def update_vtuber(sentiment, personality, is_reading):
    expressions = {
        "vui": "smile_lowres.exp3",
        "gian": "angry_lowres.exp3",
        "hao_hung": "smile_lowres.exp3"
    }
    print(f"Live2D: KoiHackPop - Sentiment: {sentiment} - Expression: {expressions[sentiment]}")
    for i in range(5):
        alpha = i / 5
        print(f"Transition: {alpha*100}% to {expressions[sentiment]}")
        time.sleep(0.03)
