from googletrans import Translator
import requests

def chat(value):
        response = requests.get("http://kenucheck.xyz/ai/api.php?msg=" + value)
        veri = response.text.split(':"')[-1].split('"}')[0]
        return veri