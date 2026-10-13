#!/usr/bin/env python3
"""
cli_run_simulation.py
=====================
CLI Interaktif untuk Menjalankan Simulasi MiroFish-Lite MBG
Menggunakan Model Lokal Ollama (100% Gratis & Offline).
"""

import os
import sys
import json
from pathlib import Path

# Tambahkan root path ke sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from scripts.mirofish_simulator.mirofish_engine import MiroFishSwarmSimulator, check_ollama_status

PRESET_SCENARIOS = [
    {
        "id": "1",
        "title": "Kenaikan Anggaran & Standarisasi Higienitas BPOM",
        "text": "Pemerintah resmi menaikkan pagu MBG dari Rp 10.000 menjadi Rp 20.000 per porsi dan mewajibkan uji sampel laboratorium BPOM di setiap dapur kecamatan setiap pagi."
    },
    {
        "id": "2",
        "title": "Insiden Keracunan Baru & Pembekuan Vendor Katering",
        "text": "Terjadi kasus 35 siswa mengalami mual dan diare setelah mengonsumsi telur balado di Kabupaten Bandung Barat. BGN langsung membekukan izin vendor swasta terkait."
    },
    {
        "id": "3",
        "title": "Peralihan dari UMKM Lokal ke Ransum Makanan Pabrikan",
        "text": "BGN mempertimbangkan mengganti masakan katering basah lokal menjadi ransum biskuit & susu formula steril pabrikan besar untuk mencegah risiko pembusukan makanan."
    }
]

def main():
    print("=" * 80)
    print("🐟 SELAMAT DATANG DI SIMULATOR SWARM INTELLIGENCE MBG (MIROFISH-LITE)")
    print("Ditenagai oleh Model Lokal Ollama (100% Bebas Biaya API & Privasi Terjamin)")
    print("=" * 80)

    if not check_ollama_status():
        print("⚠️ PERINGATAN: Server Ollama tidak terdeteksi aktif di http://localhost:11434.")
        print("   Jalankan perintah: 'ollama serve' di terminal Anda.")
        print("   Melanjutkan dalam mode fallback...\n")

    print("\nPilih Skenario Kebijakan MBG yang Ingin Disimulasikan:")
    for sc in PRESET_SCENARIOS:
        print(f"  [{sc['id']}] {sc['title']}")
        print(f"      \"{sc['text']}\"")
    print("  [4] Tulis Skenario Kustom Sendiri")

    choice = input("\nMasukkan pilihan (1-4) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        scenario = PRESET_SCENARIOS[0]["text"]
    elif choice == "2":
        scenario = PRESET_SCENARIOS[1]["text"]
    elif choice == "3":
        scenario = PRESET_SCENARIOS[2]["text"]
    elif choice == "4":
        scenario = input("\nKetik Skenario Kebijakan MBG Kustom: ").strip()
        if not scenario:
            scenario = PRESET_SCENARIOS[0]["text"]
    else:
        scenario = PRESET_SCENARIOS[0]["text"]

    model_choice = input("\nPilih Model Ollama (qwen3:8b / llama3.1:8b) [default: qwen3:8b]: ").strip() or "qwen3:8b"

    simulator = MiroFishSwarmSimulator(model=model_choice)
    results = simulator.run_simulation(scenario)

    # Tampilkan Hasil Visual di Terminal
    print("\n" + "=" * 80)
    print("📢 HASIL SIMULASI PERCAKAPAN WARGANET (ROUND 1 & 2):")
    print("=" * 80)
    
    print("\n--- [ROUND 1: CUITAN REAKSI AWAL] ---")
    for post in results["round_1_initial_reactions"]:
        print(f"\n👤 {post['name']} ({post['handle']}) | {post['cluster']}")
        print(f"💬 \"{post['tweet']}\"")

    print("\n--- [ROUND 2: DEBAT & SALING MEMBALAS] ---")
    for inter in results["round_2_interactions"]:
        print(f"\n↩️  {inter['from_handle']} membalas {inter['replying_to']}:")
        print(f"💬 \"{inter['reply_tweet']}\"")

    print("\n" + "=" * 80)
    print("📊 LAPORAN PREDIKSI STRATEGIS (EXECUTIVE FORECAST BRIEF):")
    print("=" * 80)
    synth = results["synthesis_report"]
    print(f"• Prediksi Sentimen Publik : {synth.get('predicted_public_sentiment', '-')}")
    print(f"• Dominasi Emosi Proyeksi : {synth.get('dominant_projected_emotion', '-')}")
    print(f"• Tingkat Risiko Krisis   : {synth.get('crisis_risk_level', '-')}")
    print(f"• Titik Api Friksi Utama  : {synth.get('key_friction_point', '-')}")
    print(f"• Rekomendasi untuk BGN   : {synth.get('strategic_policy_recommendation', '-')}")
    print("=" * 80)

    # Simpan log ke results
    output_dir = root_dir / "results" / "mirofish_simulations"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"simulation_{int(os.times()[4])}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📁 Log simulasi lengkap disimpan di: {out_file}\n")

if __name__ == "__main__":
    main()
