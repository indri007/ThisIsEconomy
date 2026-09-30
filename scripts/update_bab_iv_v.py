"""
scripts/update_bab_iv_v.py
Satu kali jalan: perbarui 4.5 (paragraf usang), 5.1 (tandai), Bab V (5.3 + 5.4), rujukan silang.
Angka evaluasi dibaca dari results/FINAL_MODEL_COMPARISON.csv.
Pakai:  python scripts/update_bab_iv_v.py --dry-run   lalu   python scripts/update_bab_iv_v.py
"""
import re, sys, shutil, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "tesis_text.txt", ROOT / "mbg-sna-github" / "tesis_text.txt"]
ABSA_BELUM_SELESAI = True  # ubah ke False bila ABSA sudah rampung


def id_num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def load_metrics():
    rows = list(csv.DictReader(open(ROOT / "results" / "FINAL_MODEL_COMPARISON.csv", encoding="utf-8")))
    def pick(key):
        for r in rows:
            if key.lower() in r["Model"].lower():
                return r
        raise KeyError(f"Model '{key}' tidak ada di FINAL_MODEL_COMPARISON.csv: {[r['Model'] for r in rows]}")
    indo, lr, svm = pick("IndoBERT"), pick("Logistic"), pick("SVM")
    f = lambda r, k: float(r[k])
    return {
        "n": int(float(indo.get("Test_N", 1058))),
        "acc": f(indo, "Accuracy") * 100, "mf1": f(indo, "Macro_F1"), "wf1": f(indo, "Weighted_F1"),
        "lr": f(lr, "Accuracy") * 100, "svm": f(svm, "Accuracy") * 100,
    }

SUB_ABSA = """5.3.{n} Analisis Berbasis Aspek Belum Dirampungkan
Analisis sentimen berbasis aspek (ABSA) untuk tiga aspek, yaitu anggaran, logistik, dan kualitas gizi, belum dirampungkan dalam penelitian ini. Akibatnya, sintesis phygital gap pada subbagian 4.6 belum dapat diperkuat dengan pemetaan sentimen per aspek pelaksanaan program.

"""

def build_bab5(absa: bool) -> str:
    n_absa = 7
    n_platform = 8 if absa else 7
    absa_block = SUB_ABSA.format(n=n_absa) if absa else ""

    rekom_riset = [
        "Membangun label gold standard melalui anotasi ulang sampel data uji oleh sedikitnya dua anotator manusia, disertai pengujian reliabilitas antaranotator menggunakan koefisien Cohen's κ.",
        "Mengembangkan model deteksi sindiran khusus yang dilatih dan dievaluasi terhadap label hasil anotasi manusia, sehingga mampu menangkap sindiran yang bergantung pada konteks.",
        "Menangani ketidakseimbangan kelas melalui penambahan data pada kelas minoritas atau penerapan teknik penyeimbangan data seperti oversampling dan class weighting.",
    ]
    if absa:
        rekom_riset.append("Merampungkan analisis ABSA tiga aspek (anggaran, logistik, dan kualitas gizi) untuk melengkapi sintesis phygital gap pada subbagian 4.6.")
    rekom_riset += [
        "Memperluas relasi jaringan di luar mention dengan menambahkan kolom in_reply_to_username, retweeted_username, dan quoted_username pada tahap scraping.",
        "Menerapkan representasi graf bipartit (akun–tagar atau akun–topik) untuk memetakan keterkaitan tematik antarkomponen jaringan yang secara struktural terisolasi pada representasi unipartit.",
        "Mengembangkan analisis jaringan dinamis temporal (dynamic network analysis) untuk memantau evolusi sentralitas aktor dari waktu ke waktu.",
        "Memperluas cakupan data ke platform media sosial lain dan periode yang lebih panjang, sehingga dinamika percakapan publik dapat dianalisis secara lintas platform dan longitudinal.",
    ]
    rekom_riset_txt = "\n".join(f"{i}. {t}" for i, t in enumerate(rekom_riset, 1))

    return f"""5.3 Keterbatasan Penelitian

Setiap temuan dalam penelitian ini perlu dibaca dengan memperhatikan sejumlah keterbatasan metodologis. Keterbatasan tersebut diuraikan secara terbuka agar pembaca dapat menilai sejauh mana hasil penelitian dapat ditafsirkan dan digeneralisasi, sekaligus menjadi pijakan bagi penelitian selanjutnya.

5.3.1 Perbedaan Estimasi Prevalensi Sindiran antara Tahap Awal dan Tahap Final
Pada tahap eksplorasi awal, sebelum korpus dan protokol analisis ditetapkan secara final, prevalensi unggahan bernada sindiran diperkirakan mencapai sekitar 37 persen. Angka pendahuluan tersebut sempat disampaikan kepada publik melalui rilis media. Setelah korpus dibersihkan dan metode deteksi dibakukan, analisis final mengidentifikasi 315 dari 3.395 cuitan unik, atau sekitar 9,3 persen, sebagai unggahan yang mengandung sindiran.
Perbedaan tersebut menunjukkan bahwa estimasi prevalensi sindiran sangat dipengaruhi oleh tiga faktor: definisi operasional sindiran, cakupan korpus, dan metode deteksi yang digunakan. Oleh karena itu, angka final sebesar 9,3 persen merupakan satu-satunya rujukan resmi dalam tesis ini, sedangkan estimasi pada tahap awal tidak dapat dijadikan dasar generalisasi.

5.3.2 Deteksi Sindiran Berbasis Aturan
Sindiran dalam penelitian ini dideteksi melalui pola inkongruensi linguistik berbasis aturan (rule-based), bukan melalui model klasifikasi yang dilatih dan diuji secara khusus. Pendekatan ini unggul dari sisi transparansi dan keterlacakan, karena setiap keputusan deteksi dapat ditelusuri kembali ke aturan yang digunakan.
Namun, sindiran yang maknanya bergantung pada konteks percakapan, latar budaya, atau pengetahuan bersama antarpengguna berpotensi tidak terdeteksi. Sebaliknya, sebagian pernyataan yang bersifat literal berpotensi keliru teridentifikasi sebagai sindiran.

5.3.3 Label Rujukan Evaluasi Bersifat Silver-Standard
Label emosi yang digunakan untuk melatih dan menguji model IndoBERT dihasilkan melalui anotasi semantik otomatis berbasis model bahasa dan leksikon (silver-standard), bukan melalui anotasi manusia (gold standard). Pada data uji sebanyak 1.058 cuitan, model memperoleh akurasi 79,40 persen, macro-F1 0,516, dan weighted-F1 0,785. Nilai-nilai tersebut perlu dimaknai sebagai tingkat kesesuaian model dengan label otomatis, bukan sebagai tingkat kesesuaian dengan penilaian manusia.
Pada tahap pengembangan awal, model sempat mencapai akurasi 83 persen. Audit lanjutan kemudian menemukan duplikasi teks antara data latih dan data uji yang dapat menggelembungkan hasil evaluasi. Protokol pengujian selanjutnya diperketat menggunakan pemisahan data berbasis kelompok (GroupShuffleSplit, random_state = 42) sehingga tidak terdapat tumpang tindih teks sama sekali. Dengan demikian, angka 83 persen tidak digunakan sebagai hasil penelitian.

5.3.4 Ketidakseimbangan Distribusi Kelas Emosi
Distribusi data uji didominasi oleh kelas Jijik (57,28 persen), sementara kelas Marah (14 data) dan Sedih (3 data) memiliki jumlah yang sangat terbatas. Ketimpangan ini berdampak langsung pada kinerja model di kelas minoritas, yang tercermin dari nilai recall kelas Marah sebesar 0,07 dan F1 kelas Sedih sebesar 0,00. Selain itu, dari sembilan kelas emosi yang dirancang, hanya enam kelas yang muncul dalam data uji.
Berdasarkan kondisi tersebut, nilai macro-F1 (0,516) lebih tepat digunakan untuk menggambarkan kemampuan model secara merata di seluruh kelas dibandingkan akurasi keseluruhan, yang cenderung terangkat oleh dominasi kelas mayoritas.

5.3.5 Relasi Jaringan Terbatas pada Mention
Data mentah hasil scraping tidak menyertakan identitas relasional terstruktur, yaitu in_reply_to_username, retweeted_username, dan quoted_username. Akibatnya, pembentukan edges jaringan dalam penelitian ini terbatas pada ekstraksi mention dari teks cuitan. Relasi balasan (reply), unggah ulang (retweet), dan kutipan (quote) yang sebenarnya terjadi berpotensi tidak seluruhnya tertangkap, sehingga struktur jaringan yang dianalisis merupakan representasi parsial dari interaksi yang berlangsung.

5.3.6 Representasi Jaringan Unipartit
Jaringan dimodelkan secara unipartit, yakni hanya menghubungkan akun dengan akun. Konsekuensinya, dua akun yang membahas isu yang sama, misalnya keracunan atau anggaran MBG, tetapi tidak saling menyebut, tidak akan terhubung dalam jaringan. Bersama keterbatasan pada subbab 5.3.5, kondisi ini berpotensi membuat tingkat fragmentasi jaringan (modularity 0,98 dengan 332 komponen) tampak lebih tinggi daripada kedekatan wacana yang sebenarnya. Fragmentasi tersebut lebih tepat dimaknai sebagai keterpisahan interaksi langsung antarakun, bukan keterpisahan topik pembicaraan. Keterkaitan tematik dan tagar lintas komponen, sebagaimana disinggung pada subbagian 2.6.7, belum tercakup dalam analisis ini.

{absa_block}5.3.{n_platform} Cakupan Platform dan Periode Data
Data penelitian terbatas pada platform X dengan periode pengumpulan Maret hingga Mei 2026. Karakteristik pengguna, pola interaksi, dan gaya bahasa di platform lain seperti TikTok, Instagram, atau Facebook dapat berbeda secara signifikan. Oleh karena itu, temuan penelitian ini belum dapat digeneralisasi untuk mewakili percakapan publik mengenai program MBG di platform lain maupun pada periode sesudahnya.

Keterbatasan-keterbatasan tersebut tidak mengurangi kontribusi utama penelitian ini, yaitu pemetaan struktur jaringan komunikasi publik mengenai program MBG di platform X. Keterbatasan ini justru mempertegas batas penafsiran hasil dan membuka ruang pengembangan metodologis bagi penelitian berikutnya.

5.4 Rekomendasi

5.4.1 Untuk Pemerintah / Badan Gizi Nasional
1. Membangun kanal informasi yang proaktif menjangkau komponen-komponen jaringan kecil yang teridentifikasi pada subbagian 4.2, alih-alih hanya berfokus pada komponen atau aktor dengan sentralitas tertinggi.
2. Melibatkan aktor dengan betweenness centrality tinggi (penjembatan antarklaster) sebagai mitra dialog strategis, sebagaimana diidentifikasi pada Tabel 4.3.
3. Memperbaiki mekanisme pemantauan sentimen digital secara berkelanjutan, dengan menjadikan hasil audit pelabelan pada subbagian 4.5.3 sebagai pengingat bahwa sistem deteksi otomatis memerlukan validasi berlapis sebelum dijadikan dasar pengambilan keputusan.

5.4.2 Untuk Penelitian Selanjutnya
{rekom_riset_txt}

"""


OLD_45 = re.compile(r"Hasil evaluasi model yang dilaporkan pada bagian 4\.5 ini karena itu berfungsi sebagai checkpoint diagnostik[^\n]*")

def new_45(m):
    n = f"{m['n']:,}".replace(",", ".")
    return (f"Hasil evaluasi yang dilaporkan pada bagian 4.5 merupakan hasil final setelah audit dan perbaikan protokol pengujian. "
            f"Model IndoBERT diuji pada data uji independen sebanyak {n} cuitan dengan pemisahan berbasis kelompok "
            f"(GroupShuffleSplit, random_state = 42) tanpa tumpang tindih teks antara data latih dan data uji. "
            f"Model memperoleh akurasi {id_num(m['acc'])} persen, macro-F1 {id_num(m['mf1'],3)}, dan weighted-F1 {id_num(m['wf1'],3)}, "
            f"lebih tinggi dibandingkan model pembanding TF-IDF + Logistic Regression ({id_num(m['lr'])} persen) "
            f"dan TF-IDF + Linear SVM ({id_num(m['svm'])} persen) pada data uji yang sama. "
            f"Keterbatasan terkait label silver-standard dan ketidakseimbangan kelas dibahas lebih lanjut pada subbab 5.3.3 dan 5.3.4.")

CROSSREF = [
    ("sebagaimana disinggung pada keterbatasan di subbagian 5.4", "sebagaimana dibahas pada subbab 5.3.5"),
    ("sebagaimana dicatat pada bagian Keterbatasan Penelitian (5.4)", "sebagaimana dibahas pada subbab 5.3"),
    ("dicatat kembali sebagai salah satu keterbatasan metodologis pada Bab V penelitian",
     "dicatat kembali sebagai salah satu keterbatasan metodologis pada subbab 5.3.6"),
]
BAB5 = re.compile(r"5\.3 Keterbatasan Penelitian.*?(?=DAFTAR PUSTAKA)", re.DOTALL)
STALE = re.compile(r"retrain|0,39|n\s*=\s*501|masih dalam proses|checkpoint diagnostik|placeholder", re.I)


def process(path, m, dry):
    print(f"\n=== {path.relative_to(ROOT)} ===")
    if not path.exists():
        print("  [LEWATI] tidak ada"); return
    orig = path.read_text(encoding="utf-8"); t = orig
    found = BAB5.findall(t)
    if len(found) != 1:
        print(f"  [GAGAL] blok Bab V ditemukan {len(found)}x (harus 1). Tidak diubah."); return
    t = BAB5.sub(lambda _: build_bab5(ABSA_BELUM_SELESAI), t, count=1); print("  [OK] Bab V")
    k = len(OLD_45.findall(t))
    if k == 1:
        t = OLD_45.sub(lambda _: new_45(m), t, count=1); print("  [OK] paragraf 4.5 (checkpoint diagnostik)")
    else:
        print(f"  [INFO] paragraf 4.5 lama ditemukan {k}x")
    for o, n in CROSSREF:
        if o in t:
            t = t.replace(o, n); print(f"  [OK] rujukan: {o[:40]}...")
    lines = t.splitlines()
    sisa = [(i + 1, l) for i, l in enumerate(lines) if STALE.search(l) and "5.3.3 Label" not in l]
    print(f"  [SISA] {len(sisa)} baris masih memuat narasi lama (4.5 / 5.1) -> edit manual pakai angka final:")
    for i, l in sisa:
        print(f"     L{i}: {l[:140]}")
    for name, ok in {
        "satu '5.3 Keterbatasan Penelitian'": t.count("5.3 Keterbatasan Penelitian") == 1,
        "satu '5.4 Rekomendasi'": len(re.findall(r"^5\.4 Rekomendasi\s*$", t, re.M)) == 1,
        "ada '5.4.2 Untuk Penelitian Selanjutnya'": "5.4.2 Untuk Penelitian Selanjutnya" in t,
        "DAFTAR PUSTAKA utuh": "DAFTAR PUSTAKA" in t,
    }.items():
        print(f"  {'PASS' if ok else 'CEK '} {name}")
    if dry:
        print("  [DRY-RUN] tidak ditulis"); return
    shutil.copy2(path, str(path) + ".bak"); path.write_text(t, encoding="utf-8")
    print(f"  [DISIMPAN] backup {path.name}.bak")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    m = load_metrics()
    print("Metrik dari CSV:", {k: round(v, 4) for k, v in m.items()})
    for p in TARGETS:
        process(p, m, dry)
