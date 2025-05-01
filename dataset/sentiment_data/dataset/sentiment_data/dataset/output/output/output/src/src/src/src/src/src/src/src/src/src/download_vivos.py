import requests
import os

def download_vivos():
    url = "https://ailab.hcmus.edu.vn/assets/vivos.tar.gz"
    os.makedirs("D:\\KoiHackBop\\dataset\\vits\\vivos_custom", exist_ok=True)
    response = requests.get(url)
    with open("D:\\KoiHackBop\\dataset\\vits\\vivos.tar.gz", "wb") as f:
        f.write(response.content)
    print("Downloaded VIVOS dataset!")
