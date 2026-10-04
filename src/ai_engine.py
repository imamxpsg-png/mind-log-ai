import os
import requests
import json
from dotenv import load_dotenv

# Memuat API Key dari file .env secara aman
load_dotenv()
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_API_URL = "https://featherless.ai"

def analyze_journal_emotions(journal_text):
    """
    Menggunakan Featherless AI untuk mengekstrak tingkat stres dan emosi dari teks jurnal yang panjang.
    """
    if not FEATHERLESS_API_KEY:
        return {"error": "API Key Featherless belum diatur di file .env"}

    headers = {
        "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prompt khusus untuk menyuruh AI mengeluarkan data terstruktur (JSON)
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
        "model": "meta-llama/Meta-Llama-3-8B-Instruct", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    try:
        response = requests.post(FEATHERLESS_API_URL, json=data, headers=headers)
        if response.status_code == 200:
            # Mengambil teks respons dari AI
            result_text = response.json()['choices'][0]['message']['content'].strip()
            # Mengonversi teks string JSON menjadi dictionary Python
            return json.loads(result_text)
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Gagal terhubung ke API: {str(e)}"}
