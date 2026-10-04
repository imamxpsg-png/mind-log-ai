import json
import os
from ai_engine import analyze_journal_emotions

def main():
    # Menentukan jalur ke berkas input dan output
    input_file_path = os.path.join(os.path.dirname(__file__), '..', 'sample_journals.json')
    output_file_path = os.path.join(os.path.dirname(__file__), '..', 'output_data.json')
    
    # 1. Membaca data simulasi curhatan harian
    if not os.path.exists(input_file_path):
        print(f"Error: Berkas {input_file_path} tidak ditemukan.")
        return
        
    with open(input_file_path, 'r', encoding='utf-8') as f:
        journals_data = json.load(f)
        
    print(f"Memulai analisis untuk {len(journals_data)} entri jurnal harian...\n")
    processed_results = []
    
    # 2. Memproses setiap curhatan menggunakan Featherless AI
    for entry in journals_data:
        date = entry.get("date")
        text = entry.get("journal")
        
        print(f"Memproses tanggal: {date}...")
        # Memanggil mesin AI dari ai_engine.py
        ai_analysis = analyze_journal_emotions(text)
        
        # Menggabungkan tanggal asli dengan hasil analisis dari AI
        if "error" not in ai_analysis:
            combined_entry = {
                "date": date,
                "stress_score": ai_analysis.get("stress_score"),
                "anxiety_score": ai_analysis.get("anxiety_score"),
                "happiness_score": ai_analysis.get("happiness_score"),
                "triggers": ", ".join(ai_analysis.get("triggers", [])) # Diubah ke teks biasa agar mudah dibaca dasbor
            }
            processed_results.append(combined_entry)
        else:
            print(f"Gagal memproses tanggal {date}: {ai_analysis['error']}")
            
    # 3. Menyimpan hasil akhir ke berkas baru untuk diunggah ke Adaption Labs
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_results, f, indent=4)
        
    print(f"\nSelesai! Hasil analisis matang berhasil disimpan di: {output_file_path}")

if __name__ == "__main__":
    main()
