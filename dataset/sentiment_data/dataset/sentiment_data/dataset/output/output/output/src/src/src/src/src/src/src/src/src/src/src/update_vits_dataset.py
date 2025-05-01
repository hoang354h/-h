import os

def update_vits_dataset():
    transcript_file = "D:\\KoiHackBop\\dataset\\vits\\vivos_custom\\transcript.txt"
    if os.path.exists(transcript_file):
        with open(transcript_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in lines:
                if line.strip():
                    f.write(line)
        print("Updated VITS dataset!")
