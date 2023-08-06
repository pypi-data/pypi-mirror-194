from googletrans import Translator
import requests

def chat(value, serialkey):
        response = requests.get("http://kenucheck.xyz/ai/ai.php?key=" + serialkey "+&msg=" + value)
        veri = response.text.split(':"')[-1].split('"}')[0]
        return veri