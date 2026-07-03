import sys
import requests
import json
import os
from dotenv import load_dotenv

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY tidak ditemukan di environment.")

def analyze(tool, output, target):
    prompt = f"""Anda asisten keamanan ofensif ahli. Tool '{tool}' dijalankan terhadap '{target}'. Output:
{output[:3000]}

Tugas:
1. Rangkum temuan penting dalam bahasa Indonesia.
2. Identifikasi kerentanan atau informasi berharga.
3. Sarankan langkah eksploitasi/serangan lanjutan (gunakan tool seperti Metasploit, Hydra, dll).
4. Jika tidak ada temuan, saran untuk reconnaissance lebih dalam.
Balas singkat padat."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    headers = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}
    data = {"contents":[{"parts":[{"text": prompt}]}]}
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 200:
        resp = r.json()
        try:
            return resp['candidates'][0]['content']['parts'][0]['text']
        except:
            return "AI tidak bisa menganalisa."
    else:
        return f"Error AI: {r.status_code}"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: ai_analyzer.py <tool> <target> <output_text>")
        sys.exit(1)
    tool = sys.argv[1]
    target = sys.argv[2]
    output = sys.argv[3]
    print(analyze(tool, output, target))
