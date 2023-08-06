from googletrans import Translator
import requests

def chat(value, uid = 1):
        response = requests.get("http://kenucheck.xyz/ai/api.php?uid=" + str(uid) +"&msg=" + value)
        veri = response.text.split(':"')[-1].split('"}')[0]
        return veri