import os
import requests
import json
from dotenv import load_dotenv

# Memuat API Key dari file .env secara aman
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://groq.com"

def analyze_journal_emotions(journal_text):
    """
    Menggunakan Groq AI untuk mengekstrak tingkat stres dan emosi dari teks jurnal yang panjang.
    """
    if not GROQ_API_KEY:
        return {"error": "API Key GROQ_API_KEY belum diatur di file .env"}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Bertindaklah sebagai psikolog klinis AI. Analisis teks jurnal harian berikut. 
    Berikan penilaian angka antara 1-10 untuk tingkat Stres (stress_score), Kecemasan (anxiety_score), dan Kebahagiaan (happiness_score).
    Berikan juga 3 kata kunci pemicu stres (triggers).
    
    Teks Jurnal: "{journal_text}"
    
    Format Output Wajib (Gunakan format JSON baku berikut tanpa teks pengantar):
    {{
        "stress_score": 5,
        "anxiety_score": 4,
        "happiness_score": 7,
        "triggers": ["workload", "meetings", "insomnia"]
    }}
    """
    
    data = {
        "model": "llama3-8b-8192",  # Menggunakan model Llama-3 super cepat milik Groq
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}  # Memaksa Groq mengeluarkan format JSON murni
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        if response.status_code == 200:
            result_text = response.json()['choices']['message']['content'].strip()
            return json.loads(result_text)
        else:
            return {"error": f"Groq Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Gagal terhubung ke API Groq: {str(e)}"}
