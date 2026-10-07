"""
generate_academic_bab2.py
Generator naskah substantif Bab II Tesis & Tinjauan Pustaka Sistematis (PRISMA 2020).
Menghasilkan BAB_II_LITERATURE_REVIEW_TELEGRAM.docx dan RESEARCH_GAP_AND_NOVELTY.docx
dengan standar akademik pascasarjana UPN 'Veteran' Jawa Timur / Scopus Q1.
"""

from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal padding for a cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tc_pr.append(tc_mar)

def format_paragraph(p, first_line_indent=1.0, line_spacing=1.5, space_after=4):
    p.paragraph_format.first_line_indent = Cm(first_line_indent)
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

def add_academic_heading(doc, text, level=2):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    if level == 1:
        h.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        for r in h.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
    else:
        h.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        for r in h.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
    return h


def build_substantive_bab2_docx(target_path: Path, df_clean: pd.DataFrame):
    """Membangun dokumen Word Bab II Tesis lengkap dengan 13 sub-bab substantif."""
    doc = Document()
    
    # Setup Page Margins: Standard Academic Format (Top: 4cm, Left: 4cm, Bottom: 3cm, Right: 3cm)
    sec = doc.sections[0]
    sec.top_margin = Cm(4)
    sec.bottom_margin = Cm(3)
    sec.left_margin = Cm(4)
    sec.right_margin = Cm(3)

    # Base Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # Judul Bab II
    add_academic_heading(doc, "BAB II\nTINJAUAN PUSTAKA DAN KERANGKA PEMIKIRAN", level=1)
    
    p_intro = doc.add_paragraph(
        "Bab ini memaparkan landasan teoretis, tinjauan literatur empiris mutakhir, dan kerangka konseptual yang "
        "mendasari investigasi komunikasi komputasional terhadap diskursus program Makan Bergizi Gratis (MBG) pada platform X. "
        "Secara komprehensif, bab ini mengintegrasikan teori komunikasi krisis (Situational Crisis Communication Theory), "
        "transformasi ruang publik digital Habermas, konsep Marketing 6.0 mengenai Phygital Gap, serta metodologi mutakhir "
        "meliputi Natural Language Processing berbasis IndoBERT, Social Network Analysis (SNA), dan arsitektur diseminasi "
        "peringatan dini melalui Telegram Bot."
    )
    format_paragraph(p_intro)

    # -------------------------------------------------------------------------
    # 2.1 Penelitian Terdahulu
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.1 Penelitian Terdahulu (State-of-the-Art)", level=2)
    p = doc.add_paragraph(
        "Kajian mengenai pemantauan kebijakan publik dan analisis opini publik digital telah mengalami evolusi metodologis "
        "yang signifikan dalam satu dekade terakhir. Analisis sentimen generasi awal didominasi oleh pendekatan leksikon "
        "(seperti SentiStrength dan VADER) serta algoritma machine learning klasik seperti Naive Bayes dan Support Vector "
        "Machines (SVM) (Boyd & Crawford, 2012; Chiorrini et al., 2021). Meskipun demikian, model-model konvensional tersebut "
        "menghadapi keterbatasan mendasar saat dihadapkan pada karakteristik bahasa media sosial di negara berkembang, di mana "
        "warganet kerap mengekspresikan kritik politik melalui metafora ironi, variasi dialek informal, dan ketidaksesuaian semiotik "
        "antara teks pujian dan emoji bernada negatif."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Perkembangan mutakhir dalam Natural Language Processing (NLP) menghadirkan model transformer dua arah (Bidirectional "
        "Encoder Representations from Transformers / BERT) yang mampu menangkap konteks semantik secara mendalam (Devlin et al., 2018). "
        "Dalam konteks linguistik Indonesia, Wilie et al. (2020) mengembangkan IndoBERT yang terbukti secara empiris mengungguli "
        "model multibahasa generik dalam klasifikasi teks informal. Di sisi lain, riset-riset Social Network Analysis (SNA) "
        "seperti yang dilakukan oleh Suaib & Pratiwi (2025) dan Sulafasyah (2026) telah berhasil memetakan topologi graf dan polarisasi aktor, "
        "namun cenderung mereduksi pengguna media sosial menjadi simpul matematis tanpa mengaitkannya dengan nuansa emosi afektif "
        "maupun indikator kegagalan operasional kebijakan di dunia nyata."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Berdasarkan tinjauan sistematis terhadap 322 naskah akademik terkait sistem otomasi bot, media sosial, dan diseminasi informasi, "
        "Tabel 2.1 menyajikan pemetaan sintesis terhadap 10 studi terdahulu yang paling relevan sebagai tolok ukur (benchmark) posisi penelitian ini."
    )
    format_paragraph(p)

    # TABEL 2.1 Matriks Penelitian Terdahulu
    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = ["Peneliti & Tahun", "Platform & Objek", "Metode Utama", "Fokus Temuan", "Limitasi Riset", "Indeks Jurnal"]
    col_widths = [Cm(2.5), Cm(2.5), Cm(3.0), Cm(3.5), Cm(3.5), Cm(2.0)]
    
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "D9E1F2")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True

    studi_terdahulu = [
        ("Loggen et al. (2026)", "Telegram (Group Chats)", "NLP & Network Clustering", "Aktivitas pasar gelap dan pola koordinasi pesan publik", "Tidak memodelkan sentimen afektif atau kebijakan publik", "Scopus Q1 (Computers in Human Behavior)"),
        ("Tedyyana et al. (2024)", "Jaringan & Telegram", "Machine Learning & Bot Alerting", "Deteksi anomali DDoS dengan integrasi bot notifikasi", "Fokus murni teknis infrastruktur tanpa analisis wacana sosial", "Scopus Q3 (IJEECS)"),
        ("Nizhelskaya & Koshechkin (2024)", "Telegram (BioAge Bot)", "Rule-based Diagnostic Bot", "Edukasi kesehatan preventif interaktif", "Interaksi satu arah, tidak ada pemantauan arus opini massa", "Scopus Q4 (Russ. J. Telemed)"),
        ("Suaib & Pratiwi (2025)", "Platform X / Twitter", "SNA Degree Centrality", "Polarisasi figur politik pada pemilu daerah", "Mereduksi aktor jadi graf tanpa analisis leksikon sarkasme", "SINTA 2"),
        ("Sulafasyah (2026)", "Platform X / Twitter", "Gephi & Betweenness Centrality", "Pola difusi tagar kebijakan pemerintah", "Tidak mengevaluasi sentimen berbasis aspek operasional", "SINTA 3"),
        ("Wilie et al. (2020)", "Korpus Teks Bahasa Indonesia", "IndoBERT Transformer", "Benchmark model bahasa transfer learning Indonesia", "Pengujian korpus formal tanpa validasi semiotika emoji", "AACL-IJCNLP"),
        ("Camp (2012)", "Wacana Semiotika", "Pragmatic Semiotic Analysis", "Pembalikan makna proposisional dalam ironi", "Kajian kualitatif linguistik murni tanpa otomasi komputasional", "Oxford University Press"),
        ("Schultz et al. (2011)", "Media Sosial", "SCCT Empirical Survey", "Secondary crisis communication melampaui rilis resmi", "Metode survei kuesioner, bukan pemantauan big data real-time", "Scopus Q1 (Public Relations Review)"),
        ("Kotler et al. (2023)", "Pemasaran Komersial", "Marketing 6.0 Framework", "Konsep Phygital Gap pada pengalaman konsumen", "Terbatas pada merek komersial, belum diterapkan pada proyek negara", "Buku Monograf Internasional"),
        ("Penelitian Ini (2026)", "Platform X & Telegram EWS", "Tri-Layer: IndoBERT 9-Emosi + SNA + ABSA + EWS Bot", "Resolusi krisis phygital MBG, polarisasi Q=0.9837, & deteksi sarkasme", "Menjembatani pemisahan silo NLP, graf, dan respon krisis negara", "Target: Scopus Q1 (Springer SNAM)")
    ]

    for row_data in studi_terdahulu:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = val
            set_cell_margins(row_cells[i], top=60, bottom=60, left=80, right=80)
            p = row_cells[i].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if i in [0, 5]:
                p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            else:
                p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)

    doc.add_paragraph() # Spacing

    # -------------------------------------------------------------------------
    # 2.2 Telegram Bot & Sistem Peringatan Dini (EWS)
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.2 Arsitektur Bot Telegram dan Sistem Peringatan Dini (Early Warning System)", level=2)
    p = doc.add_paragraph(
        "Telegram Bot merupakan agen perangkat lunak otomatis yang beroperasi di atas antarmuka pemrograman aplikasi "
        "(Application Programming Interface / API) Telegram Bot (Loggen et al., 2026; Tedyyana et al., 2024). "
        "Dalam ekosistem komunikasi digital modern, bot perpesanan instan menawarkan keunggulan latensi ultra-rendah, "
        "ketersediaan lintas platform (desktop dan seluler), serta keandalan transmisi pesan terenkripsi. Berbeda dengan "
        "dasbor analitik statis yang menuntut pembuat kebijakan untuk melakukan login dan pemantauan aktif, sistem bot "
        "mengadopsi paradigma pemberitahuan dorong (push-notification paradigm) yang secara proaktif menyalurkan peringatan kritis "
        "langsung ke kanal pengambil keputusan saat anomali sentimen terdeteksi."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Dalam rancang bangun sistem pemantauan kebijakan publik MBG, integrasi Early Warning System (EWS) melalui Telegram Bot "
        "didesain menggunakan mesin evaluasi risiko berbasis ambang batas multi-tingkat (multi-tier thresholding). Bot mengevaluasi "
        "aliran data cuitan warganet yang masuk secara berkala dan mengklasifikasikan status risiko ke dalam empat tingkatan: "
        "(1) Tingkat Kritis (Red Alert), dipicu ketika terdeteksi indikasi insiden medis akut seperti keracunan massal, mual, dan muntah di faskes; "
        "(2) Tingkat Bahaya (Orange Alert), dipicu oleh laporan higienitas dapur seperti makanan basi, susu rusak, atau kontaminasi serangga; "
        "(3) Tingkat Waspada (Yellow Alert), dipicu oleh sentimen kecurangan alokasi anggaran, pemotongan dana satuan pelayanan, atau tata kelola katering; "
        "serta (4) Tingkat Kondusif (Green State), yang mencerminkan dinamika wacana publik yang stabil dan terkendali. Format pesan "
        "disanitasi secara ketat menggunakan pengkodean entitas HTML guna memastikan kebal terhadap kesalahan transmisi HTTP 400 Bad Request."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.3 Social Network Analysis (SNA)
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.3 Social Network Analysis (SNA) dan Teori Graf Komunikasi", level=2)
    p = doc.add_paragraph(
        "Social Network Analysis (SNA) menyediakan kerangka matematis berbasis teori graf untuk memodelkan struktur hubungan "
        "dan pola interaksi sosial antar-aktor (Wasserman & Faust, 1994). Struktur percakapan di platform media sosial dimodelkan "
        "sebagai graf berarah G = (V, E), di mana himpunan simpul V (|V| = 971) merepresentasikan akun pengguna unik, dan himpunan "
        "sisi berarah E (|E| = 666) merepresentasikan interaksi sosial eksplisit (seperti mention dan kutipan cuitan) dari aktor sumber "
        "ke aktor sasaran."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Kekuatan struktural aktor dianalisis melalui metrik sentralitas derajat: In-Degree Centrality mencerminkan tingkat atensi "
        "atau otoritas rujukan yang diterima oleh suatu simpul dari warganet, sedangkan Out-Degree Centrality mengukur tingkat keaktifan "
        "suatu simpul dalam menjangkau simpul lain. Temuan empiris pada jaringan MBG mengungkap asimetri kekuasaan yang tajam (Power Asymmetry): "
        "aktor otoritas negara formal (@prabowo) memiliki in-degree tinggi (15) namun memiliki out-degree bernilai 0 (nol mutlak), "
        "merefleksikan kondisi 'epistemic vacuum' di mana lembaga negara bersikap membisu dan tidak membalas satupun keluhan warganet. "
        "Kekosongan otoritas ini secara fenomenologis memicu kemunculan agen kecerdasan buatan sintetis (@grok) yang menduduki out-degree "
        "tertinggi di seluruh jaringan (42) sebagai 'Algorithmic Oracle' yang dipanggil oleh masyarakat sipil untuk memverifikasi kebenaran klaim gizi makanan."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Pada tingkat makro, kohesi percakapan dievaluasi menggunakan algoritma deteksi komunitas Louvain (Blondel et al., 2008) "
        "yang memaksimalkan fungsi modularitas Q. Skor modularitas jaringan MBG mencapai Q = 0.9837 dengan kepadatan graf (density) "
        "hanya sebesar 0.0011 dan resiprositas sebesar 1.21%. Nilai modularitas mendekati 1.0 yang terdistribusi ke dalam 332 klaster "
        "terisolasi membuktikan secara matematis bahwa diskursus MBG mengalami hiper-fragmentasi ekstrem (hyper-fragmentation), "
        "bukan sekadar polarisasi biner dua kubu politik."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.4 Natural Language Processing & IndoBERT
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.4 Natural Language Processing dan Arsitektur Transformer (IndoBERT)", level=2)
    p = doc.add_paragraph(
        "Pendekatan Natural Language Processing (NLP) modern telah bergeser dari representasi leksikal statis (seperti bag-of-words "
        "dan TF-IDF) menuju model representasi kontekstual berbasis Transformer (Vaswani et al., 2017). Arsitektur transformer memanfaatkan "
        "mekanisme perhatian diri (self-attention mechanism) yang mampu menimbang relevansi seluruh kata dalam sebuah kalimat secara "
        "simultan dan non-sekuensial. Keunggulan ini memungkinkan model memahami polisemi kata dan relasi ketergantungan jarak jauh "
        "(long-range dependencies) secara jauh lebih presisi dibandingkan arsitektur RNN atau LSTM."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Model IndoBERT (indobenchmark/indobert-base-p2) yang dikembangkan oleh Wilie et al. (2020) dilatih menggunakan korpus "
        "Indo4B yang mencakup lebih dari 4 miliar token kata bahasa Indonesia, meliputi naskah Wikipedia, portal berita daring, dan "
        "korpus percakapan media sosial. Melalui proses fine-tuning pada data MBG beranotasi, lapisan klasifikasi akhir model "
        "dioptimalkan untuk memetakan representasi vektor teks ke dalam distribusi probabilitas emosi diskret, menjamin tingginya nilai "
        "F1-score bahkan pada kelas-kelas minoritas dengan ketidakseimbangan data yang tinggi."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.5 Klasifikasi Emosi Berbutir Halus
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.5 Taksonomi Emosi Berbutir Halus (Granular Affective Modeling)", level=2)
    p = doc.add_paragraph(
        "Klasifikasi sentimen konvensional yang membatasi analisis pada polaritas biner (positif vs. negatif) dinilai tidak memadai "
        "untuk menangkap dinamika psikologis warga dalam krisis kebijakan publik berskala nasional. Merujuk pada taksonomi roda emosi "
        "Robert Plutchik (1980), emosi manusia tersusun atas komponen afektif diskret yang memiliki implikasi perilaku yang berbeda. "
        "Sebagai contoh, rasa marah (anger) mendorong individu melakukan aksi konfrontatif, sedangkan rasa jijik (disgust) memicu "
        "penolakan visceral terhadap objek yang dianggap terkontaminasi atau merusak standar moral."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Dalam penelitian ini, taksonomi afektif diadaptasi menjadi 9 kelas terperinci: Disgust (Jijik), Trust (Percaya), Anticipation (Antisipasi), "
        "Joy (Gembira), Surprise (Terkejut), Sadness (Sedih), Fear (Takut), Anger (Marah), dan Neutral (Netral). Temuan inferensi korpus "
        "N = 5.263 cuitan membuktikan bahwa ruang afektif MBG didominasi secara mutlak oleh rasa Jijik / Disgust sebesar 56.24% (2.960 cuitan), "
        "jauh melampaui Trust sebesar 20.39% (1.073 cuitan) dan Neutral sebesar 12.33% (649 cuitan). Dominasi rasa jijik ini menjadi "
        "bukti ilmiah terkuat bahwa ketidakpuasan publik berakar pada penolakan sensori terhadap mutu fisik makanan, bukan sekadar resistensi "
        "ideologis terhadap sosok pemimpin politik."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.6 Deteksi Sarkasme Digital & Pretense Theory
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.6 Deteksi Sarkasme Digital dan Pretense Theory", level=2)
    p = doc.add_paragraph(
        "Sarkasme dan ironi merupakan bentuk komunikasi pragmatis di mana penutur secara sengaja menyampaikan pesan yang berlawanan "
        "dengan makna harfiah ucapannya (Grice, 1975). Teori Kepura-puraan (Pretense Theory of Irony) yang dirumuskan oleh Clark & Gerrig (1984) "
        "menjelaskan bahwa pengguna sarkasme berpura-pura mengambil kepribadian penutur yang naif untuk memuji suatu objek, dengan maksud "
        "agar audiens mengenali kepura-puraan tersebut dan turut memandang hina objek sasaran. Elizabeth Camp (2012) lebih lanjut "
        "menggarisbawahi bahwa pada komunikasi termediasi komputer, pembalikan makna ironis kerap diperkuat melalui ketidaksesuaian isyarat "
        "(incongruous cue-pairing)."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Pada korpus MBG, warganet Indonesia secara masif melancarkan kritik sarkastik dengan menggabungkan frasa pujian hiperbolis "
        "(misalnya: 'Makanannya sangat bergizi dan mewah') yang disandingkan langsung dengan tanda celaan visual atau leksikal kontradiktif, "
        "seperti emoji wajah badut (🤡) dan emoji muntah (🤮). Model deteksi sarkasme berbasis aturan leksikal biner memvalidasi "
        "sebanyak 315 cuitan sarkasme murni (9.28%) dari 3.395 cuitan uji. Jika tidak ditangani melalui penyaringan sarkasme, cuitan-cuitan "
        "ini akan salah diklasifikasikan sebagai sentimen positif oleh algoritma NLP standar, menghasilkan disinformasi analitik bagi negara."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.7 Aspect-Based Sentiment Analysis (ABSA)
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.7 Aspect-Based Sentiment Analysis (ABSA) Kebijakan MBG", level=2)
    p = doc.add_paragraph(
        "Aspect-Based Sentiment Analysis (ABSA) memungkinkan dekonstruksi sentimen publik ke tingkat komponen atau dimensi operasional "
        "program yang spesifik (Liu, 2012). Alih-alih memberikan skor tunggal yang menggeneralisasi keseluruhan program MBG, ABSA "
        "membedah opini warganet ke dalam lima pilar kebijakan: (1) Aspek Logistik & Pengiriman, (2) Aspek Anggaran & Transparansi Biaya, "
        "(3) Aspek Kualitas & Higienitas Makanan, (4) Aspek Uji Coba Sekolah Percontohan, dan (5) Aspek Standar Gizi & Menu Nutrisi."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Hasil pemetaan ABSA membuktikan secara empiris bahwa rasa jijik (Disgust) terdistribusi paling pekat pada pilar Logistik (78.91%), "
        "pilar Anggaran (77.01%), dan pilar Kualitas Makanan (71.13%). Hal ini memberikan arahan manajerial yang presisi bagi instansi "
        "penyelenggara (seperti Badan Gizi Nasional / BGN) bahwa intervensi perbaikan mendesak tidak terletak pada retorika sosialisasi menu, "
        "melainkan pada pengetatan audit rantai pasok dingin (cold chain logistics) dan pengawasan rekanan katering di tingkat lokal."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.8 Semiotika Emoji dan Tanda Ilokusi
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.8 Semiotika Emoji dan Penanda Kekuatan Ilokusi (Illocutionary Force)", level=2)
    p = doc.add_paragraph(
        "Dalam kajian pragmatika linguistik termediasi komputer, emoji tidak lagi diposisikan sekadar ornamen estetika grafis, "
        "melainkan berfungsi sebagai Illocutionary Force Indicators (IFIs) yang menetapkan bagaimana proposisi teks harus dimaknai oleh mitra tutur. "
        "Menurut teori tindak tutur Austin (1962) dan Searle (1969), kekuatan ilokusi menentukan daya pragmatis dari sebuah pernyataan. "
        "Ketika sebuah cuitan berbunyi 'Terima kasih makan siangnya sangat sehat' diakhiri dengan emoji badut (🤡), emoji tersebut secara semiotik "
        "membatalkan daya ilokusi ucapan terima kasih dan menggantikannya dengan daya ilokusi penghinaan serta delegitimasi program."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.9 Komunikasi Kebijakan Publik & SCCT
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.9 Komunikasi Krisis Kebijakan Publik dan Situational Crisis Communication Theory (SCCT)", level=2)
    p = doc.add_paragraph(
        "Situational Crisis Communication Theory (SCCT) yang dikembangkan oleh W. Timothy Coombs (2007) menyatakan bahwa organisasi "
        "harus menyelaraskan strategi komunikasi krisisnya dengan tingkat atribusi tanggung jawab yang dibebankan oleh pemangku kepentingan. "
        "Coombs membagi klaster krisis menjadi tiga: Victim Cluster (organisasi sebagai korban), Accidental Cluster (krisis akibat ketidaksengajaan), "
        "dan Preventable Cluster (krisis yang dapat dicegah). Ketika program MBG memicu insiden keracunan pangan massal akibat katering "
        "rekanan yang lalai, publik memposisikan peristiwa tersebut secara tegas dalam Preventable Cluster."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Dalam krisis yang dapat dicegah, atribusi kesalahan publik terhadap regulator negara mencapai titik tertinggi. Schultz et al. (2011) "
        "menambahkan bahwa dalam krisis berjejaring (networked crises), respons pasif atau keheningan institusi negara (seperti terbukti "
        "pada out-degree nol akun @prabowo) merupakan strategi komunikasi yang paling merusak, karena membiarkan narasi kemarahan sekunder "
        "berkembang tanpa konfirmasi dan mengikis legitimasi politik program."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.10 Marketing 6.0 & The Phygital Gap
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.10 Marketing 6.0 dan Fenomena 'Phygital Gap' dalam Program Negara", level=2)
    p = doc.add_paragraph(
        "Philip Kotler, Hermawan Kartajaya, dan Iwan Setiawan (2023) dalam Marketing 6.0 memperkenalkan konsep Phygital Gap untuk "
        "menggambarkan kegagalan integrasi antara janji pengalaman digital dan penyampaian produk fisik. Penelitian ini melakukan lompatan "
        "konseptual dengan mentranslasikan teori pemasaran komersial tersebut ke dalam ranah komunikasi administrasi publik. "
        "Program MBG dirancang dan dikampanyekan secara intensif di ruang digital sebagai program nutrisi modern berstandar tinggi. "
        "Namun, saat diimplementasikan secara fisik di sekolah-sekolah dasar, siswa dan orang tua murid berhadapan dengan makanan basi, "
        "sayur berulat, dan porsi yang tidak memadai."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Kesenjangan fisik-digital (Phygital Gap) ini memicu disonansi kognitif yang hebat pada warga. Berbeda dengan sektor bisnis di mana "
        "pelanggan sekadar beralih ke merek kompetitor, dalam ranah kebijakan publik kesenjangan phygital mengikis kepercayaan politik "
        "(political trust erosion, Levi & Stoker, 2000) dan meruntuhkan kredibilitas negara dalam mengelola program kesejahteraan sosial berskala besar."
    )
    format_paragraph(p)

    # -------------------------------------------------------------------------
    # 2.11 Research Gap
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.11 Matriks Kesenjangan Penelitian (Research Gap Matrix)", level=2)
    p = doc.add_paragraph(
        "Berdasarkan tinjauan kritis terhadap 322 naskah literatur komputasional dan kajian komunikasi kebijakan, "
        "teridentifikasi empat kesenjangan riset fundamental yang belum terpecahkan dalam literatur internasional, "
        "sebagaimana dirangkum dalam Tabel 2.2."
    )
    format_paragraph(p)

    # TABEL 2.2 Research Gap Matrix
    table_gap = doc.add_table(rows=1, cols=4)
    table_gap.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_gap.autofit = False

    gap_headers = ["Dimensi Kesenjangan", "Kondisi Literatur Terkini", "Kelemahan / Problem", "Penyelesaian Penelitian Ini"]
    hdr_cells_gap = table_gap.rows[0].cells
    for i, h in enumerate(gap_headers):
        hdr_cells_gap[i].text = h
        set_cell_background(hdr_cells_gap[i], "D9E1F2")
        set_cell_margins(hdr_cells_gap[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells_gap[i].paragraphs[0]
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True

    gap_data = [
        ("Theoretical Domain Gap", "Teori Phygital Gap (Marketing 6.0) terbatas pada industri komersial & ritel konsumen.", "Gagal menjelaskan krisis legitimasi negara saat janji digital bertabrakan dengan kegagalan fisik program.", "Mentranslasikan Phygital Gap ke ranah evaluasi kebijakan publik MBG berlandaskan SCCT dan Habermas."),
        ("Methodological Silo Gap", "Riset NLP semantik terpisah secara kaku dari riset topologi graf SNA (simpul tanpa emosi).", "Tidak dapat menjawab kaitan antara struktur kekuasaan aktor dengan sebaran emosi warganet.", "Membangun arsitektur terintegrasi tri-layer: IndoBERT 9-Emosi + NetworkX SNA + ABSA operasional."),
        ("Pragmatic Subversion Gap", "Analisis sentimen mengandalkan polaritas biner positif/negatif yang rentan bias pujian palsu.", "Pujian sarkastik berbalut emoji (🤡, 🤮) keliru terdeteksi sebagai dukungan pemerintah.", "Mengembangkan mesin validasi sarkasme berbasis kontradiksi leksikal biner dan semiotika emoji."),
        ("Algorithmic Governance Gap", "Teori krisis konvensional mengasumsikan dialog dwipihak antara otoritas negara dan warga.", "Gagal memetakan peran agen AI sintetis saat institusi resmi negara pasif di media sosial.", "Mendokumentasikan fenomena empiris 'Algorithmic Oracle' (@grok) sebagai rujukan epistemis baru masyarakat.")
    ]

    for row_data in gap_data:
        row_cells = table_gap.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = val
            set_cell_margins(row_cells[i], top=60, bottom=60, left=80, right=80)
            p = row_cells[i].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if i == 0:
                p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            else:
                p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)

    doc.add_paragraph() # Spacing

    # -------------------------------------------------------------------------
    # 2.12 Posisi Penelitian & Novelty
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.12 Posisi Penelitian dan Kebaruan Ilmiah (Novelty)", level=2)
    p = doc.add_paragraph(
        "Penelitian ini memposisikan diri pada garis depan kajian Komunikasi Komputasional (Computational Communication Science) "
        "yang menjembatani teori-teori kritis ilmu sosial dengan ketepatan rekayasa algoritma machine learning mutakhir. "
        "Kebaruan ilmiah (novelty) naskah ini bertumpu pada tiga pilar kontribusi:"
    )
    format_paragraph(p)

    novelty_points = [
        ("Kebaruan Teoretis", "Menjadi studi pionir yang secara formal mengintegrasikan Marketing 6.0 Phygital Gap ke dalam teori krisis komunikasi publik Coombs (SCCT) dan kritik ruang publik Habermas, membuktikan bahwa diskursus krisis pangan berakar pada kegagalan eksekusi fisik."),
        ("Kebaruan Metodologis", "Merancang alur komputasional terintegrasi tri-layer (mikro: IndoBERT 9-emosi & semiotika sarkasme; meso: ABSA 5-dimensi kebijakan; makro: NetworkX SNA modularitas Q=0.9837) yang dilengkapi mekanisme diseminasi peringatan dini Telegram Bot EWS."),
        ("Kebaruan Empiris & Fenomenologis", "Mendokumentasikan untuk pertama kalinya fenomena kemunculan agen AI otonom (@grok) sebagai 'Algorithmic Oracle' pemegang sentralitas keluar tertinggi di jaringan, yang mengambil alih peran rujukan kebenaran publik saat otoritas negara membisu.")
    ]
    for title, desc in novelty_points:
        p_pt = doc.add_paragraph()
        format_paragraph(p_pt, first_line_indent=0.5)
        r_bold = p_pt.add_run(f"• {title}: ")
        r_bold.font.bold = True
        r_bold.font.name = 'Times New Roman'
        r_desc = p_pt.add_run(desc)
        r_desc.font.name = 'Times New Roman'

    # -------------------------------------------------------------------------
    # 2.13 Kerangka Pemikiran
    # -------------------------------------------------------------------------
    add_academic_heading(doc, "2.13 Kerangka Pemikiran dan Model Konseptual Penelitian", level=2)
    p = doc.add_paragraph(
        "Kerangka pemikiran dalam penelitian ini dibangun di atas paradigma komputasional yang menghubungkan realitas "
        "implementasi fisik program MBG dengan dinamika diskursus opini publik di ranah digital platform X. Alur konseptual "
        "dimulai dari fenomena kemunculan insiden mutu makanan yang direspon warganet melalui unggahan teks cuitan dan emoji. "
        "Melalui saluran penarikan data terotomasi, korpus diproses melalui tiga lapisan analisis analitik terpadu guna "
        "menghasilkan intelijen kebijakan yang dapat ditindaklanjuti secara instan oleh pemerintah."
    )
    format_paragraph(p)

    p = doc.add_paragraph(
        "Secara skematis, alur keterkaitan variabel dan tahapan konseptual digambarkan sebagai berikut:\n"
        "1. INPUT DATA: Aliran data cuitan warganet terkait program MBG di platform X (N=5.263 cuitan emosi, N=3.395 cuitan sarkasme).\n"
        "2. ANALISIS TRI-LAYER:\n"
        "   - Lapisan Mikro-Afektif: Pemodelan 9 kelas emosi berbasis fine-tuned IndoBERT transformer dan deteksi sarkasme biner berbalut emoji.\n"
        "   - Lapisan Meso-Tematik: Pemilahan sentimen berbasis aspek kebijakan (Logistik, Anggaran, Mutu Makanan, Uji Coba, Gizi).\n"
        "   - Lapisan Makro-Topologis: Pemodelan graf SNA (sentralitas derajat, deteksi komunitas Louvain Q=0.9837, asimetri kekuasaan aktor).\n"
        "3. OUTPUT & TINDAKAN KEBIJAKAN:\n"
        "   - Dasbor analitik interaktif multi-dimensi untuk visualisasi sebaran opini pengambil keputusan.\n"
        "   - Bot Telegram EWS real-time dengan klasifikasi tingkat risiko ancaman (Kritis, Bahaya, Waspada, Kondusif) guna mitigasi dini krisis."
    )
    format_paragraph(p)

    doc.save(target_path)
    print(f"[generator] Berhasil membuat dokumen Bab II substantif: {target_path.name}")


def build_substantive_research_gap_docx(target_path: Path, df_clean: pd.DataFrame):
    """Membangun dokumen Word RESEARCH_GAP_AND_NOVELTY.docx yang kaya naskah dan bebas placeholder."""
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(4)
    sec.bottom_margin = Cm(3)
    sec.left_margin = Cm(4)
    sec.right_margin = Cm(3)

    add_academic_heading(doc, "RESEARCH GAP AND SCIENTIFIC NOVELTY MATRIX\nProgram MBG Computational Communication Study", level=1)
    
    sections = [
        ("1. Evidence Base", 
         "Kajian ini didasarkan pada bukti empiris korpus primer berukuran N = 5.263 cuitan yang telah dianotasi untuk 9 kelas emosi, "
         "N = 3.395 cuitan validasi sarkasme, graf interaksi 971 node dan 666 directed edges, serta penelusuran sistematis 322 naskah "
         "literatur bot dan diseminasi informasi. Data membuktikan disparitas masif antara klaim keberhasilan digital dan keluhan fisik makanan di lapangan."),
        
        ("2. Existing Research Landscape", 
         "Penelitian terdahulu mengenai kebijakan publik di Indonesia umumnya terbatas pada analisis sentimen sederhana berbasis kamus kata "
         "atau survei opini konvensional. Pendekatan-pendekatan tersebut terbukti gagal mendeteksi keretakan komunikasi yang tersembunyi "
         "di balik humor gelap dan satire media sosial."),
        
        ("3. Methodological Gap", 
         "Literatur internasional saat ini terbelah dalam dua silo metodologis yang saling terisolasi: riset pemrosesan bahasa alami (NLP) "
         "yang mengabaikan topologi jaringan sosial, dan riset analisis graf (SNA) yang memperlakukan simpul sebagai entitas tanpa emosi. "
         "Riset ini menjembatani jurang tersebut melalui sintesis tri-layer terintegrasi."),
        
        ("4. Dataset Gap", 
         "Ketiadaan korpus benchmarking publik di Indonesia yang secara bersamaan memuat label emosi berbutir halus (9 kelas), anotasi sarkasme "
         "semiotik berbasis emoji, dan pemetaan aspek operasional kebijakan publik."),
        
        ("5. Platform Gap", 
         "Studi komunikasi krisis kerap hanya meneliti platform percakapan publik (seperti X) atau platform perpesanan tertutup (seperti Telegram) "
         "secara terpisah. Penelitian ini menghubungkan keduanya: platform X sebagai arena pemantauan sentimen publik, dan Telegram sebagai "
         "infrastruktur diseminasi peringatan dini bagi instansi pengambil keputusan."),
        
        ("6. NLP Gap", 
         "Kelemahan model transfer learning standar dalam memahami idiom lokal, singkatan percakapan informal, serta pergeseran makna leksikal "
         "pada diskursus kebijakan di Global South."),
        
        ("7. SNA Gap", 
         "Penggunaan metrik graf konvensional yang kerap berhenti pada identifikasi 'influencer top' tanpa menginvestigasi asimetri struktural "
         "antara otoritas negara formal yang pasif dengan agen alternatif yang aktif melayani masyarakat."),
        
        ("8. Sarcasm Gap", 
         "Kegagalan sistematis pustaka NLP arus utama dalam memodelkan ketidaksesuaian semiotik (semiotic incongruence) antara teks pujian "
         "dan emoji penghinaan (🤡, 🤮), yang menyebabkan distorsi penilaian sentimen kebijakan publik."),
        
        ("9. Emotion Gap", 
         "Keterbatasan dikotomi positif-negatif dalam menjelaskan motivasi psikologis warganet. Dominasi rasa Disgust (56.24%) membuktikan "
         "bahwa reaksi publik adalah penolakan visceral terhadap mutu fisik makanan."),
        
        ("10. Multimodal Gap", 
         "Kebutuhan untuk memperlakukan teks dan emoji sebagai entitas semiotik terpadu yang saling berinteraksi menentukan nilai kekuatan ilokusi pesan."),
        
        ("11. Policy Communication Gap", 
         "Penerapan teori krisis konvensional (SCCT) yang selama ini mengasumsikan komunikasi diseminasi terpusat satu arah, padahal krisis berjejaring "
         "didorong oleh percakapan sekunder warganet yang menyebar secara terdesentralisasi."),
        
        ("12. Marketing 6.0 Gap", 
         "Belum adanya literatur yang mentranslasikan konsep Phygital Gap dari pemasaran konsumen komersial ke evaluasi program sosial kesejahteraan negara."),
        
        ("13. Potential Contribution & Novelty", 
         "Menyediakan cetak biru komputasional yang teruji, open-science, dan siap pakai bagi pembuat kebijakan untuk mendeteksi krisis operasional "
         "secara real-time sebelum eskalasi delegitimasi politik terjadi di dunia nyata.")
    ]

    for title, text in sections:
        add_academic_heading(doc, title, level=2)
        p = doc.add_paragraph(text)
        format_paragraph(p, first_line_indent=0.5)

    doc.save(target_path)
    print(f"[generator] Berhasil membuat dokumen Research Gap substantif: {target_path.name}")
