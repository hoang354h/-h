import json
import random

def split_dataset():
    with open("D:\\KoiHackBop\\dataset\\koihackpop_data\\train.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    random.shuffle(data)
    train_size = int(0.8 * len(data))
    train_data = data[:train_size]
    val_data = data[train_size:]
    with open("D:\\KoiHackBop\\dataset\\koihackpop_data\\train.json", "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    with open("D:\\KoiHackBop\\dataset\\koihackpop_data\\val.json", "w", encoding="utf-8") as f:
        json.dump(val_data, f, ensure_ascii=False, indent=2)
    print("Split dataset into train/val!")
