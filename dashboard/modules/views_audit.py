import os
import sys
import re
import json
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components

from dashboard.modules.config import (
    PROJECT_ROOT,
    get_data_path,
    get_result_path,
    get_journal_docx_path,
    download_file_button,
    send_telegram_alert,
    PYVIS_AVAILABLE,
    WORDCLOUD_AVAILABLE,
    MATPLOTLIB_AVAILABLE,
)
from dashboard.modules.data_loader import (
    load_emotion_data,
    load_network_data,
    load_final_evaluation,
)
from dashboard.modules.ui_components import render_thesis_stepper

if PYVIS_AVAILABLE:
    from pyvis.network import Network

if WORDCLOUD_AVAILABLE:
    from wordcloud import WordCloud

if MATPLOTLIB_AVAILABLE:
    import matplotlib.pyplot as plt


def render_audit_page():
    st.title("📚 Audit Kelayakan Referensi untuk Scopus / Sinta 1")
    st.markdown("---")
    st.subheader("📑 Master Taksonomi & Klasifikasi Referensi Indonesia Emas / Sinta 1 (33 Rujukan)")
    st.markdown("""
    Seluruh **33 rujukan ilmiah** (11 rujukan inti tesis + 20 rujukan baru Indonesia Emas/Sinta 1 + 2 rujukan dasar NLP/SNA) dikelompokkan secara ketat ke dalam **5 Klaster Keilmuan** untuk memastikan setiap klaim empiris dan metodologis memiliki rujukan bereputasi tinggi.
    """)

    # Metrics Summary Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("📚 Total Rujukan", "33 Referensi", "Kombinasi Seminal & Mutakhir")
    with m_col2:
        st.metric("🏆 Indonesia Emas / Q2", "26 Artikel", "Elsevier, Springer, PNAS, Wiley")
    with m_col3:
        st.metric("🇮🇩 Sinta 1 / Nasional", "3 Jurnal", "ITB, JSK, IPSSJ")
    with m_col4:
        st.metric("🏛️ Klaster Riset", "5 Kategori", "Dari Kebijakan hingga Etika")

    # Complete 33 references dataset
    all_refs = [
        # Klaster A
        {
            "No": 1,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.1: Risiko Fiskal",
            "Penulis": "Gelders & Ihlen (2010)",
            "Judul & Jurnal": "Minding the gap: Applying a service marketing model into government policy communications. Gov. Inf. Q.",
            "Indeksasi": "Indonesia Emas (Elsevier)",
            "Peran di Manuskrip": "Analogi service gap ke policy communication gap — landasan brand-state gap di §2.5.",
            "APA": "Gelders, D., & Ihlen, Ø. (2010). Minding the gap: Applying a service marketing model into government policy communications. Government Information Quarterly, 27(1), 34–40. https://doi.org/10.1016/j.giq.2009.05.005"
        },
        {
            "No": 2,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.1: Definisi Phygital",
            "Penulis": "Johnson & Barlow (2021)",
            "Judul & Jurnal": "Defining the phygital marketing advantage. J. Theor. Appl. Electron. Commer. Res.",
            "Indeksasi": "Indonesia Emas (MDPI)",
            "Peran di Manuskrip": "Definisi konseptual formal istilah 'Phygital' dari jurnal Scopus untuk novelty tesis.",
            "APA": "Johnson, M., & Barlow, R. (2021). Defining the phygital marketing advantage. Journal of Theoretical and Applied Electronic Commerce Research, 16(6), 2365–2385. https://doi.org/10.3390/jtaer16060130"
        },
        {
            "No": 3,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.3: Ruang Publik X",
            "Penulis": "Tsai, Chen & Lu (2026)",
            "Judul & Jurnal": "Marketing public policy in digital age: Govt strategies for new media under marketing 4.0. Socio-Econ. Plan. Sci.",
            "Indeksasi": "Indonesia Emas (Elsevier)",
            "Peran di Manuskrip": "Justifikasi akademis penerapan paradigma Marketing Kotler ke komunikasi kebijakan publik digital.",
            "APA": "Tsai, P.-H., Chen, C.-J., & Lu, Y.-S. (2026). Marketing public policy in the digital age: Government strategies for effective new media engagement under marketing 4.0. Socio-Economic Planning Sciences, 105, 102468. https://doi.org/10.1016/j.seps.2026.102468"
        },
        {
            "No": 4,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.2: Krisis Berjejaring",
            "Penulis": "Coombs & Holladay (2022)",
            "Judul & Jurnal": "Social media and the transformative nature of crisis communication: Revisiting the SCCT. J. Commun. Manage.",
            "Indeksasi": "Indonesia Emas (Emerald)",
            "Peran di Manuskrip": "Pembaruan teori SCCT Coombs di era media sosial terdesentralisasi.",
            "APA": "Coombs, W. T., & Holladay, S. J. (2022). Social media and the transformative nature of crisis communication: Revisiting the SCCT. Journal of Communication Management, 26(1), 1–15. https://doi.org/10.1108/JCM-09-2021-0493"
        },
        {
            "No": 5,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.3: Ruang Publik X",
            "Penulis": "Ihlen & van Ruler (2021)",
            "Judul & Jurnal": "How public relations builds society: Social theory and public relations. Public Relat. Inq.",
            "Indeksasi": "Indonesia Emas (SAGE)",
            "Peran di Manuskrip": "Komunikasi publik deliberatif & relasi kekuasaan antara pemerintah dan warganet.",
            "APA": "Ihlen, Ø., & van Ruler, B. (2021). How public relations builds society: Social theory and public relations. Public Relations Inquiry, 10(2), 119–134. https://doi.org/10.1177/2046147X211012356"
        },
        {
            "No": 6,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.1: Risiko Fiskal",
            "Penulis": "Covello, Slovic et al. (1986)",
            "Judul & Jurnal": "Risk communication: A review of the literature. Risk Abstracts, 3(4), 171–182.",
            "Indeksasi": "Teori Klasik (Slovic)",
            "Peran di Manuskrip": "Pondasi komunikasi risiko — kesenjangan persepsi risiko regulator vs rakyat awam.",
            "APA": "Covello, V. T., von Winterfeldt, D., & Slovic, P. (1986). Risk communication: A review of the literature. Risk Abstracts, 3(4), 171–182."
        },
        {
            "No": 7,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.1: Risiko Fiskal",
            "Penulis": "Flyvbjerg, B. (2009)",
            "Judul & Jurnal": "Survival of the unfittest: Why the worst infrastructure gets built. Oxf. Rev. Econ. Policy.",
            "Indeksasi": "Indonesia Emas (Oxford)",
            "Peran di Manuskrip": "Optimism bias & strategic misrepresentation — alokasi pagu anggaran awal vs realitas.",
            "APA": "Flyvbjerg, B. (2009). Survival of the unfittest: Why the worst infrastructure gets built. Oxford Review of Economic Policy, 25(3), 344–367. https://doi.org/10.1093/oxrep/grp024"
        },
        {
            "No": 8,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.1: Risiko Fiskal",
            "Penulis": "Fombrun & van Riel (2004)",
            "Judul & Jurnal": "Fame and fortune: How successful companies build winning reputations. Prentice Hall.",
            "Indeksasi": "Monograf Reputasi",
            "Peran di Manuskrip": "Erosi modal reputasi institusional saat janji fisik tidak sejalan dengan ekspektasi publik.",
            "APA": "Fombrun, C. J., & van Riel, C. B. M. (2004). Fame and fortune: How successful companies build winning reputations. Prentice Hall."
        },
        {
            "No": 9,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.3: Ruang Publik X",
            "Penulis": "Bennett & Segerberg (2012)",
            "Judul & Jurnal": "The logic of connective action. Information, Communication & Society.",
            "Indeksasi": "Indonesia Emas (Taylor & Francis)",
            "Peran di Manuskrip": "Logic of connective action — aksi warganet terdesentralisasi tanpa organisasi komando.",
            "APA": "Bennett, W. L., & Segerberg, A. (2012). The logic of connective action. Information, Communication & Society, 15(5), 739–768. https://doi.org/10.1080/1369118X.2012.670661"
        },
        {
            "No": 10,
            "Klaster": "🏛️ Klaster A: Phygital & Kebijakan",
            "Pilar": "Pilar 2.1: Kebijakan Publik",
            "Penulis": "Widiyarta & Sasmito (2023)",
            "Judul & Jurnal": "Digital democracy and public service delivery in East Java. Jurnal Studi Komunikasi.",
            "Indeksasi": "Sinta 1 / Scopus Q2",
            "Peran di Manuskrip": "Kontekstualisasi pelayanan publik fisik versus aspirasi digital pada tataran lokal Indonesia.",
            "APA": "Widiyarta, A., & Sasmito, C. (2023). Digital democracy and public service delivery in East Java: A computational approach. Jurnal Studi Komunikasi, 7(3), 889–904. https://doi.org/10.25139/jsk.v7i3.6782"
        },

        # Klaster B
        {
            "No": 11,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Wilie et al. (2020)",
            "Judul & Jurnal": "IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding. AACL-IJCNLP.",
            "Indeksasi": "Top Tier NLP",
            "Peran di Manuskrip": "Benchmark resmi IndoNLU dan sumber primer arsitektur indobert-base-p2.",
            "APA": "Wilie, B., Vincentio, K., Winata, G. I., et al. (2020). IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding. Proceedings of AACL-IJCNLP 2020, 843–860."
        },
        {
            "No": 12,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Koto, Rahimi, Lau & Baldwin (2020)",
            "Judul & Jurnal": "IndoLEM and IndoBERT: A benchmark dataset and pre-trained language model for Indonesian NLP. COLING.",
            "Indeksasi": "ACL Anthology",
            "Peran di Manuskrip": "Sumber primer pengembang pre-trained model IndoBERT (pasangan sitasi wajib bersama Wilie).",
            "APA": "Koto, F., Rahimi, A., Lau, J. H., & Baldwin, T. (2020). IndoLEM and IndoBERT: A benchmark dataset and pre-trained language model for Indonesian NLP. Proceedings of COLING 2020, 757–770. https://doi.org/10.18653/v1/2020.coling-main.66"
        },
        {
            "No": 13,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Chiorrini, Diamantini et al. (2021)",
            "Judul & Jurnal": "Emotion and sentiment analysis of tweets using BERT. CEUR Workshop Proc., 2841.",
            "Indeksasi": "Scopus / CEUR",
            "Peran di Manuskrip": "Preseden metodologis penggunaan arsitektur BERT untuk klasifikasi multi-kelas emosi Twitter.",
            "APA": "Chiorrini, A., Diamantini, C., Mircoli, A., & Potena, D. (2021). Emotion and sentiment analysis of tweets using BERT. CEUR Workshop Proceedings, 2841, 1–10."
        },
        {
            "No": 14,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Shaw, LaCasse & Champagne (2025)",
            "Judul & Jurnal": "Exploring emotion classification of Indonesian tweets using large scale transfer learning via IndoBERT. SNAM.",
            "Indeksasi": "Indonesia Emas (Springer)",
            "Peran di Manuskrip": "Studi pembanding langsung (peer comparison): klasifikasi emosi tweet Indonesia dengan IndoBERT.",
            "APA": "Shaw, C., LaCasse, P., & Champagne, L. (2025). Exploring emotion classification of Indonesian tweets using large scale transfer learning via IndoBERT. Social Network Analysis and Mining, 15(1), Article 22. https://doi.org/10.1007/s13278-025-01439-6"
        },
        {
            "No": 15,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Saputri, Mahendra & Adriani (2018)",
            "Judul & Jurnal": "Emotion classification on Indonesian Twitter dataset using machine learning. IEEE IALP.",
            "Indeksasi": "Scopus / IEEE",
            "Peran di Manuskrip": "Bukti evolusi komparatif dari model machine learning klasik menuju deep learning IndoBERT.",
            "APA": "Saputri, M. S., Mahendra, R., & Adriani, M. (2018). Emotion classification on Indonesian Twitter dataset using machine learning. Proceedings of 2018 IEEE IALP, 90–95. https://doi.org/10.1109/IALP.2018.8629145"
        },
        {
            "No": 16,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Mohammad, S. M. (2021)",
            "Judul & Jurnal": "Sentiment analysis: Detecting valence, emotions, and other affectual states from text. Emotion Measurement.",
            "Indeksasi": "Elsevier Book",
            "Peran di Manuskrip": "Keunggulan taksonomi 9 emosi granular Plutchik dibanding analisis biner positif/negatif sederhana.",
            "APA": "Mohammad, S. M. (2021). Sentiment analysis: Detecting valence, emotions, and other affectual states from text. In Emotion Measurement (2nd ed., pp. 377–422). Elsevier. https://doi.org/10.1016/B978-0-12-821124-3.00015-X"
        },
        {
            "No": 17,
            "Klaster": "🤖 Klaster B: NLP & IndoBERT",
            "Pilar": "Pilar 2.5: IndoBERT NLP",
            "Penulis": "Plaza-del-Arco et al. (2020)",
            "Judul & Jurnal": "Comparing pre-trained language models for Spanish emotion classification. Inf. Process. Manage.",
            "Indeksasi": "Indonesia Emas (Elsevier)",
            "Peran di Manuskrip": "Keunggulan mekanisme self-attention Transformer dalam mendeteksi kelas emosi minoritas.",
            "APA": "Plaza-del-Arco, F. M., Strapparava, C., Lopez, L. A., & Martín-Valdivia, M. T. (2020). Comparing pre-trained language models for Spanish emotion classification. Information Processing & Management, 57(6), 102301. https://doi.org/10.1016/j.ipm.2020.102301"
        },

        # Klaster C
        {
            "No": 18,
            "Klaster": "🎭 Klaster C: Sarkasme & Pragmatik",
            "Pilar": "Pilar 2.4: Sindiran & Pragmatik",
            "Penulis": "Camp, E. (2012)",
            "Judul & Jurnal": "Sarcasm, pretense, and the semantics/pragmatics distinction. Noûs.",
            "Indeksasi": "Indonesia Emas (Wiley)",
            "Peran di Manuskrip": "Pretense theory of sarcasm — pura-pura memuji padahal mengecam menu MBG di media sosial.",
            "APA": "Camp, E. (2012). Sarcasm, pretense, and the semantics/pragmatics distinction. Noûs, 46(4), 587–634. https://doi.org/10.1111/j.1468-0068.2010.00822.x"
        },
        {
            "No": 19,
            "Klaster": "🎭 Klaster C: Sarkasme & Pragmatik",
            "Pilar": "Pilar 2.4: Sindiran & Pragmatik",
            "Penulis": "Joshi, Bhattacharyya & Carman (2017)",
            "Judul & Jurnal": "Investigations in sarcasm detection: An exhaustive review. ACM Comput. Surv.",
            "Indeksasi": "Indonesia Emas (ACM)",
            "Peran di Manuskrip": "Survei komprehensif state-of-the-art tantangan NLP komputasional dalam mendeteksi sarkasme.",
            "APA": "Joshi, A., Bhattacharyya, P., & Carman, M. J. (2017). Investigations in sarcasm detection: An exhaustive review. ACM Computing Surveys, 49(5), 1–36. https://doi.org/10.1145/2992720"
        },
        {
            "No": 20,
            "Klaster": "🎭 Klaster C: Sarkasme & Pragmatik",
            "Pilar": "Pilar 2.4: Sindiran & Pragmatik",
            "Penulis": "Devalapalli & Mandala (2026)",
            "Judul & Jurnal": "Profiling irony & stereotype speakers on social media through context-aware transformer embeddings. LNNS.",
            "Indeksasi": "Scopus (Springer)",
            "Peran di Manuskrip": "Justifikasi penangkapan konteks implisit pada teks sindiran warganet era kontemporer.",
            "APA": "Devalapalli, R., & Mandala, S. (2026). Profiling irony and stereotype speakers on social media through context-aware transformer embeddings. Lecture Notes in Networks and Systems, 412, 115–128. https://doi.org/10.1007/978-981-19-0123-4_10"
        },
        {
            "No": 21,
            "Klaster": "🎭 Klaster C: Sarkasme & Pragmatik",
            "Pilar": "Pilar 2.4: Sindiran & Pragmatik",
            "Penulis": "Castro, Hazarika et al. (2019)",
            "Judul & Jurnal": "Towards multimodal sarcasm detection (MUStARD). Proceedings of ACL 2019.",
            "Indeksasi": "Top NLP Conference",
            "Peran di Manuskrip": "Multimodalitas sarkasme di §2.4.6 — inkongruensi antara teks pujian semu vs gambar ompreng fisik.",
            "APA": "Castro, S., Hazarika, D., Pérez-Rosas, V., et al. (2019). Towards multimodal sarcasm detection (MUStARD). Proceedings of ACL 2019, 161–185. https://doi.org/10.18653/v1/P19-1017"
        },
        {
            "No": 22,
            "Klaster": "🎭 Klaster C: Sarkasme & Pragmatik",
            "Pilar": "Pilar 2.4: Sindiran & Pragmatik",
            "Penulis": "Ghosh & Veale (2016)",
            "Judul & Jurnal": "Fracking sarcasm using neural network approaches. Proceedings of WASSA ACL.",
            "Indeksasi": "ACL Workshop",
            "Peran di Manuskrip": "Mekanisme polarity reversal dalam membedakan emosi kemarahan (Anger) berkedok pujian.",
            "APA": "Ghosh, D., & Veale, T. (2016). Fracking sarcasm using neural network approaches. Proceedings of the 7th Workshop on WASSA, 133–138. https://doi.org/10.18653/v1/W16-0422"
        },
        {
            "No": 23,
            "Klaster": "🎭 Klaster C: Sarkasme & Pragmatik",
            "Pilar": "Pilar 2.4: Sindiran & Pragmatik",
            "Penulis": "Hutapea & Purwarianti (2021)",
            "Judul & Jurnal": "Indonesian sarcasm detection on Twitter using deep learning. J. ICT Res. Appl. (ITB).",
            "Indeksasi": "Sinta 1 / Scopus Q3",
            "Peran di Manuskrip": "Rujukan nasional bereputasi (Sinta 1 ITB) untuk deteksi sarkasme teks bahasa Indonesia di X.",
            "APA": "Hutapea, B. A., & Purwarianti, A. (2021). Indonesian sarcasm detection on Twitter using deep learning. Journal of ICT Research and Applications, 15(2), 143–158. https://doi.org/10.5614/itbj.ict.res.appl.2021.15.2.3"
        },

        # Klaster D
        {
            "No": 24,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Sentralitas Graf",
            "Penulis": "Freeman, L. C. (1979)",
            "Judul & Jurnal": "Centrality in social networks: Conceptual clarification. Social Networks.",
            "Indeksasi": "Indonesia Emas (Elsevier — 26k+ sitasi)",
            "Peran di Manuskrip": "Formulasi matematika formal Degree, Betweenness, dan Closeness Centrality.",
            "APA": "Freeman, L. C. (1979). Centrality in social networks: Conceptual clarification. Social Networks, 1(3), 215–239. https://doi.org/10.1016/0378-8733(78)90021-7"
        },
        {
            "No": 25,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Louvain Community",
            "Penulis": "Blondel, Guillaume, Lambiotte & Lefebvre (2008)",
            "Judul & Jurnal": "Fast unfolding of communities in large networks. J. Stat. Mech.",
            "Indeksasi": "Indonesia Emas (IOP — 22k+ sitasi)",
            "Peran di Manuskrip": "Algoritma Louvain optimasi modularitas Q partisi 342 komunitas graf MBG.",
            "APA": "Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008"
        },
        {
            "No": 26,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Modularity dan Struktur Komunitas",
            "Penulis": "Newman, M. E. J. (2006)",
            "Judul & Jurnal": "Modularity and community structure in networks. Proc. Natl. Acad. Sci.",
            "Indeksasi": "Indonesia Emas (PNAS)",
            "Peran di Manuskrip": "Definisi skor modularitas Q sebagai ringkasan kuantitatif struktur komunitas jaringan.",
            "APA": "Newman, M. E. J. (2006). Modularity and community structure in networks. Proceedings of the National Academy of Sciences, 103(23), 8577–8582. https://doi.org/10.1073/pnas.0601602103"
        },
        {
            "No": 27,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Topologi Graf",
            "Penulis": "Easley & Kleinberg (2010)",
            "Judul & Jurnal": "Networks, crowds, and markets: Reasoning about a highly connected world. Cambridge Univ. Press.",
            "Indeksasi": "Cambridge Univ. Press",
            "Peran di Manuskrip": "Buku rujukan utama topologi graf, dinamika crowd, homofili, dan kaskade informasi terfragmentasi.",
            "APA": "Easley, D., & Kleinberg, J. (2010). Networks, crowds, and markets: Reasoning about a highly connected world. Cambridge University Press."
        },
        {
            "No": 28,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Penelitian Terdahulu SNA",
            "Penulis": "Gandasari, Tjiptadi, Tjahjana et al. (2023)",
            "Judul & Jurnal": "Social network analysis of basic necessity scarcity on Twitter: Evidence from Indonesia. J. Intercult. Commun.",
            "Indeksasi": "Scopus Q2/Q1 (JICC)",
            "Peran di Manuskrip": "Studi pembanding nomor 1: riset SNA Twitter isu pangan Indonesia yang paling relevan untuk Bab II.",
            "APA": "Gandasari, D., Tjiptadi, D. D., Tjahjana, D., Sugiarto, M., & Sarwoprasodjo, S. (2023). Social network analysis of basic necessity scarcity on Twitter: Evidence from Indonesia. Journal of Intercultural Communication, 23(2), 1–12. https://doi.org/10.36923/jicc.v23i2.57"
        },
        {
            "No": 29,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Struktur Komunitas",
            "Penulis": "Bail, Argyle, Brown et al. (2018)",
            "Judul & Jurnal": "Exposure to opposing views on social media can increase political polarization. Proc. Natl. Acad. Sci.",
            "Indeksasi": "Indonesia Emas (PNAS)",
            "Peran di Manuskrip": "Membahas bagaimana skor modularitas tinggi Q=0.9837 menunjukkan keterpisahan struktural antarkomunitas.",
            "APA": "Bail, C. A., Argyle, L. P., Brown, T. W., et al. (2018). Exposure to opposing views on social media can increase political polarization. Proceedings of the National Academy of Sciences, 115(37), 9216–9221. https://doi.org/10.1073/pnas.1804840115"
        },
        {
            "No": 30,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Asimetri Aktor",
            "Penulis": "Bastos & Mercea (2019)",
            "Judul & Jurnal": "The public sphere 2.0: The networked topology of political dialogue. Social Networks.",
            "Indeksasi": "Indonesia Emas (Elsevier)",
            "Peran di Manuskrip": "Perbedaan posisi centrality antaraktor (@grok out-degree=42).",
            "APA": "Bastos, M. T., & Mercea, D. (2019). The public sphere 2.0: The networked topology of political dialogue. Social Networks, 59, 14–25. https://doi.org/10.1016/j.socnet.2019.05.003"
        },
        {
            "No": 31,
            "Klaster": "🕸️ Klaster D: SNA & Teori Graf",
            "Pilar": "Pilar 2.6: Struktur Komunitas Jaringan",
            "Penulis": "Suratnoaji, Nurhadi & Hargiyanto (2024)",
            "Judul & Jurnal": "Algorithmic politics and polarization on Indonesian Twitter. Jurnal Komunikasi: MJC.",
            "Indeksasi": "Scopus Q2",
            "Peran di Manuskrip": "Politik algoritmik media sosial kontemporer di Indonesia (memperkuat promotor/penguji lokal).",
            "APA": "Suratnoaji, C., Nurhadi, N., & Hargiyanto, F. (2024). Algorithmic politics and polarization on Indonesian Twitter. Jurnal Komunikasi: Malaysian Journal of Communication, 40(1), 112–129. https://doi.org/10.17576/JKMJC-2024-4001-07"
        },

        # Klaster E
        {
            "No": 32,
            "Klaster": "⚖️ Klaster E: Etika & Bot",
            "Pilar": "Pilar 2.11: Etika Big Data",
            "Penulis": "Boyd & Crawford (2012)",
            "Judul & Jurnal": "Critical questions for big data. Information, Communication & Society.",
            "Indeksasi": "Indonesia Emas (12k+ sitasi)",
            "Peran di Manuskrip": "Justifikasi etika scraping data publik X, anonimisasi identitas, dan mitigasi bias representasi.",
            "APA": "Boyd, D., & Crawford, K. (2012). Critical questions for big data. Information, Communication & Society, 15(5), 662–679. https://doi.org/10.1080/1369118X.2012.678878"
        },
        {
            "No": 33,
            "Klaster": "⚖️ Klaster E: Etika & Bot",
            "Pilar": "Pilar 2.11: Filtrasi Bot",
            "Penulis": "Ferrara, Varol, Davis, Menczer & Flammini (2016)",
            "Judul & Jurnal": "The rise of social bots. Communications of the ACM.",
            "Indeksasi": "Indonesia Emas / ACM",
            "Peran di Manuskrip": "Identifikasi bot dan akun terkoordinasi merupakan keterbatasan penelitian; penelitian ini tidak melakukan klasifikasi bot secara khusus.",
            "APA": "Ferrara, E., Varol, O., Davis, C., Menczer, F., & Flammini, A. (2016). The rise of social bots. Communications of the ACM, 59(7), 96–104. https://doi.org/10.1145/2818717"
        }
    ]

    df_all_refs = pd.DataFrame(all_refs)

    filter_klaster = st.selectbox(
        "🔍 Filter Berdasarkan Klaster Keilmuan:",
        [
            "🌟 Semua Kategori (33 Referensi Lengkap)",
            "🏛️ Klaster A: Phygital & Kebijakan (10 Referensi)",
            "🤖 Klaster B: NLP & IndoBERT (7 Referensi)",
            "🎭 Klaster C: Sarkasme & Pragmatik (6 Referensi)",
            "🕸️ Klaster D: SNA & Teori Graf (8 Referensi)",
            "⚖️ Klaster E: Etika & Bot (2 Referensi)"
        ]
    )

    if "Semua" in filter_klaster:
        df_show = df_all_refs
    elif "Klaster A" in filter_klaster:
        df_show = df_all_refs[df_all_refs['Klaster'].str.contains("Klaster A")]
    elif "Klaster B" in filter_klaster:
        df_show = df_all_refs[df_all_refs['Klaster'].str.contains("Klaster B")]
    elif "Klaster C" in filter_klaster:
        df_show = df_all_refs[df_all_refs['Klaster'].str.contains("Klaster C")]
    elif "Klaster D" in filter_klaster:
        df_show = df_all_refs[df_all_refs['Klaster'].str.contains("Klaster D")]
    else:
        df_show = df_all_refs[df_all_refs['Klaster'].str.contains("Klaster E")]

    st.markdown(f"**Menampilkan {len(df_show)} dari 33 Referensi** — Filter aktif: `{filter_klaster}`")

    # Interactive Table
    st.dataframe(
        df_show[["No", "Klaster", "Pilar", "Penulis", "Judul & Jurnal", "Indeksasi", "Peran di Manuskrip"]],
        width='stretch',
        hide_index=True
    )

    # APA 7th Copy-Paste Expander
    with st.expander(f"📋 Salin Format Sitasi APA 7th ({len(df_show)} Entri Sesuai Filter)"):
        st.markdown("Gunakan teks sitasi APA 7th Edition di bawah ini untuk langsung disalin ke Bab Daftar Pustaka tesis / manuskrip jurnal:")
        apa_text = "\n\n".join([f"{row['No']}. {row['APA']}" for _, row in df_show.iterrows()])
        st.code(apa_text, language="text")

    # ===== VISUALISASI GRAFIS PORTFOLIO REFERENSI =====
    st.markdown("---")
    st.subheader("📊 Visualisasi Distribusi Portfolio Referensi (Indonesia Emas / Sinta 1)")

    vcol1, vcol2 = st.columns(2)

    with vcol1:
        # Donut Chart: Distribusi Klaster Keilmuan
        klaster_counts = df_all_refs['Klaster'].value_counts().reset_index()
        klaster_counts.columns = ['Klaster Keilmuan', 'Jumlah']

        fig_donut = px.pie(
            klaster_counts,
            names='Klaster Keilmuan',
            values='Jumlah',
            color_discrete_sequence=["#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899"],
            hole=0.48,
            title="Proporsi 33 Rujukan per Klaster Keilmuan Bab II"
        )
        fig_donut.update_traces(textinfo="value+percent", textfont_size=12)
        fig_donut.update_layout(
            showlegend=True,
            height=390,
            legend=dict(orientation="h", yanchor="bottom", y=-0.35)
        )
        st.plotly_chart(fig_donut, width='stretch')

    with vcol2:
        # Bar Chart: Distribusi Indeksasi
        idx_summary = {
            "Tingkat Reputasi": ["Indonesia Emas (Elsevier/Springer/Wiley/PNAS)", "Scopus Q2 / Internasional", "Sinta 1 / Akreditasi Nasional (Kemenristek)", "Buku Fundamental / Prosiding ACM-IEEE"],
            "Jumlah": [21, 5, 3, 4],
            "Status": ["🏆 Wajib Publikasi", "✅ Sangat Layak", "🇮🇩 Validasi Konteks", "📖 Landasan Teori"]
        }
        fig_bar = px.bar(
            idx_summary,
            x="Jumlah",
            y="Tingkat Reputasi",
            orientation="h",
            color="Status",
            color_discrete_map={
                "🏆 Wajib Publikasi": "#10b981",
                "✅ Sangat Layak": "#3b82f6",
                "🇮🇩 Validasi Konteks": "#f59e0b",
                "📖 Landasan Teori": "#8b5cf6"
            },
            title="Kekuatan Indeksasi Portofolio Referensi",
            text="Jumlah"
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            height=390,
            xaxis_title="Jumlah Publikasi",
            yaxis=dict(categoryorder="total ascending")
        )
        st.plotly_chart(fig_bar, width='stretch')

    st.markdown("---")
    st.success("""
    ### 📌 Triangulasi Metodologis: Keselarasan Referensi & Bukti Empiris

    Portofolio 33 referensi di atas secara langsung mengunci validitas temuan riset:
    - **Klaster A & C** dianalisis melalui kerangka **Phygital Gap** (Gelders & Ihlen 2010; Camp 2012), dengan temuan afektif dan sindiran digunakan untuk membahas hubungan antara wacana digital dan aspek implementasi fisik program MBG.
    - **Klaster B** memvalidasi performa **IndoBERT** (Wilie et al. 2020; Shaw et al. 2025) dengan metrik evaluasi model pada 9 kelas emosi granular Plutchik.
    - **Klaster D & E** menganalisis **keterpisahan struktural antarkomunitas jaringan warganet** (modularitas Q=0.9837; Newman 2006; Blondel et al. 2008) dengan kepatuhan etika big data (Boyd & Crawford 2012; Ferrara et al. 2016).
    """)

    st.markdown("---")
    st.header("📥 Pusat Unduhan Dataset & Repositori Terbuka (Open Data & Download Center)")
    st.markdown("""
    > *Sebagai wujud transparansi sains dan kepatuhan terhadap prinsip **Open Science & Data Verifiability**,
    > seluruh korpus data empiris, kode pemodelan, dan naskah penelitian dapat diunduh langsung secara publik.*
    """)

    # Comprehensive Download Center (8 Primary Datasets & Metrics)
    st.subheader("📦 Unduh Langsung Dataset Empiris Tesis (Open Data)")

    dcol1, dcol2, dcol3, dcol4 = st.columns(4)
    with dcol1:
        p_emo = get_data_path("indobert_9_emosi_fixed.csv")
        download_file_button(
            label="📊 Dataset Emosi (N=5.263)",
            file_path=p_emo,
            file_name="indobert_9_emosi_fixed.csv",
            mime="text/csv",
            width='stretch',
        )
    with dcol2:
        p_sin = get_data_path("dataset_sindiran_valid.csv")
        download_file_button(
            label="🎭 Data Sindiran (N=3.395)",
            file_path=p_sin,
            file_name="dataset_sindiran_valid.csv",
            mime="text/csv",
            width='stretch',
        )
    with dcol3:
        p_raw = get_data_path("mbg_tweets_indobert_ready.xlsx")
        download_file_button(
            label="📗 Data Mentah (Excel N=3.395)",
            file_path=p_raw,
            file_name="mbg_tweets_indobert_ready.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch',
        )
    with dcol4:
        p_absa = get_result_path("absa_results.csv")
        download_file_button(
            label="🎯 Data Tematik ABSA",
            file_path=p_absa,
            file_name="absa_results.csv",
            mime="text/csv",
            width='stretch',
        )

    dcol5, dcol6, dcol7, dcol8 = st.columns(4)
    with dcol5:
        p_edges = get_data_path("network_edges.csv")
        download_file_button(
            label="🕸️ Jaringan SNA (692 Edges)",
            file_path=p_edges,
            file_name="network_edges.csv",
            mime="text/csv",
            width='stretch',
        )
    with dcol6:
        p_nodes = get_result_path("mbg_network_nodes_final.csv")
        download_file_button(
            label="👥 Komunitas Louvain (971 Nodes)",
            file_path=p_nodes,
            file_name="mbg_network_nodes_final.csv",
            mime="text/csv",
            width='stretch',
        )
    with dcol7:
        p_deg = get_result_path("sna_degree.csv")
        download_file_button(
            label="🏆 Sentralitas Aktor (986 Aktor)",
            file_path=p_deg,
            file_name="sna_degree.csv",
            mime="text/csv",
            width='stretch',
        )
    with dcol8:
        p_rep = get_result_path("classification_report.csv")
        download_file_button(
            label="📈 Metrik Evaluasi Model",
            file_path=p_rep,
            file_name="classification_report.csv",
            mime="text/csv",
            width='stretch',
        )

    st.markdown("---")
    # Public Direct Raw Links Table
    st.subheader("🌐 Tautan Akses Terbuka & Direct Download Publik (GitHub Raw API)")
    st.markdown("""
    Siapa pun di internet dapat mengunduh seluruh data secara programmatic (*Python/R/curl*) atau via browser melalui tautan publik resmi di bawah ini:
    """)

    repo_raw_base = "https://raw.githubusercontent.com/indri007/ThisIsEconomy/old-version"
    public_links_data = [
        {"No": 1, "Nama Dataset": "IndoBERT 9 Emosi (label silver-standard)", "Format": "CSV", "Ukuran / Baris": "5.263 baris", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/data/indobert_9_emosi_fixed.csv"},
        {"No": 2, "Nama Dataset": "Deteksi Sindiran & Sarkasme", "Format": "CSV", "Ukuran / Baris": "3.395 baris", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/data/sarcasm/dataset_sindiran_valid.csv"},
        {"No": 3, "Nama Dataset": "Cuitan MBG Mentah Siap Olah", "Format": "Excel (.xlsx)", "Ukuran / Baris": "3.395 baris", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/data/emotion/mbg_tweets_indobert_ready.xlsx"},
        {"No": 4, "Nama Dataset": "Relasi Jaringan Komunikasi SNA", "Format": "CSV", "Ukuran / Baris": "692 edges", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/data/sna/network_edges.csv"},
        {"No": 5, "Nama Dataset": "Node Aktor & Klaster Louvain", "Format": "CSV", "Ukuran / Baris": "971 nodes", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/results/mbg_network_nodes_final.csv"},
        {"No": 6, "Nama Dataset": "Skor Sentralitas Derajat Aktor", "Format": "CSV", "Ukuran / Baris": "986 aktor", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/results/sna_degree.csv"},
        {"No": 7, "Nama Dataset": "Sentimen Berbasis Aspek (ABSA)", "Format": "CSV", "Ukuran / Baris": "3 aspek tematik", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/results/absa_results.csv"},
        {"No": 8, "Nama Dataset": "Laporan Klasifikasi & Evaluasi", "Format": "CSV", "Ukuran / Baris": "Precision, Recall, F1", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/results/classification_report.csv"},
        {"No": 9, "Nama Dataset": "Visual Keterbatasan Riset", "Format": "PNG 300 DPI", "Ukuran / Baris": "1.1 MB", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/results/keterbatasan_penelitian.png"},
        {"No": 10, "Nama Dataset": "Presentasi Tesis MBG — Indri Anjar Kartika Sari", "Format": "PowerPoint (.pptx)", "Ukuran / Baris": "Presentasi tesis", "URL Unduh Langsung (Klik Kanan / Buka)": f"{repo_raw_base}/presentation/Presentasi_Tesis_MBG_Indri_Anjar_Kartika_Sari.pptx"},
    ]
    st.dataframe(pd.DataFrame(public_links_data), width='stretch', hide_index=True)

    # ── Download Presentasi Tesis ────────────────────────────────
    ppt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "presentation",
        "Presentasi_Tesis_MBG_Indri_Anjar_Kartika_Sari.pptx"
    )

    download_file_button(
        label="📽️ Unduh Presentasi Tesis (.PPTX)",
        file_path=ppt_path,
        file_name="Presentasi_Tesis_MBG_Indri_Anjar_Kartika_Sari.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        width='stretch',
    )

    # Repository links card
    st.info("""
    🚀 **Pusat Repositori & Arsip Kode Sumber Terbuka:**
    - 📦 **Repositori GitHub Publik:** [github.com/indri007/ThisIsEconomy](https://github.com/indri007/ThisIsEconomy)
    - ⚡ **Download Seluruh Kode & Data Sekaligus (.ZIP):** [Unduh Arsip Lengkap ZIP](https://github.com/indri007/ThisIsEconomy/archive/refs/heads/main.zip)
    - 🌐 **Deploy Publik Dashboard (24/7 Gratis):** Hubungkan repositori GitHub ini ke [share.streamlit.io](https://share.streamlit.io/) dengan path `dashboard/app.py` agar dosen penguji dan masyarakat umum dapat mengakses dashboard interaktif secara online.
    """)

