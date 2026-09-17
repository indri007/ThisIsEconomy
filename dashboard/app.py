import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Configuration
st.set_page_config(
    page_title="Tesis MBG: Phygital Gap Analysis",
    page_icon="📊",
    layout="wide"
)

def apply_material3_theme():
    st.markdown('''
    <style>
    /* Google Fonts: Roboto (Material 3 standard) */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Material 3 Card Elevation & Radius for Images */
    img {
        border-radius: 16px !important;
        box-shadow: 0 4px 8px 3px rgba(0,0,0,0.15) !important;
        transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1) !important;
        margin-bottom: 20px !important;
    }
    img:hover {
        transform: scale(1.02) !important;
    }
    
    /* Material 3 Buttons (Filled tonal / Primary) */
    .stButton>button {
        border-radius: 100px !important;
        border: none !important;
        background-color: #6750A4 !important;
        color: #FFFFFF !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 3px 1px rgba(0,0,0,0.15), 0 1px 2px 0 rgba(0,0,0,0.3) !important;
        transition: all 0.2s cubic-bezier(0.2, 0, 0, 1) !important;
    }
    .stButton>button:hover {
        background-color: #4F378B !important;
        box-shadow: 0 2px 6px 2px rgba(0,0,0,0.15), 0 1px 2px 0 rgba(0,0,0,0.3) !important;
    }
    
    /* Info boxes (Alerts) styled as M3 Surface Containers */
    div[data-testid="stMarkdownContainer"] > div.stAlert {
        border-radius: 16px !important;
        border: none !important;
        background-color: #F4EFF4 !important;
        color: #1C1B1F !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    /* Header Typography M3 styling */
    h1, h2, h3 {
        color: #1C1B1F !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Main Background & Sidebar */
    .stApp {
        background-color: #FFFBFE !important;
    }
    [data-testid="stSidebar"] {
        background-color: #F4EFF4 !important;
        border-right: none !important;
    }
    </style>
    ''', unsafe_allow_html=True)

apply_material3_theme()

# Cache data loading
@st.cache_data(ttl=3600)
def load_emotion_data():
    # Adjust path assuming run from root 'tesis_mbg'
    path = "data/results/indobert_9_emosi_fixed.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    # Fallback if run inside 'dashboard' folder
    return pd.read_csv("../data/results/indobert_9_emosi_fixed.csv")

@st.cache_data(ttl=3600)
def load_network_data():
    edge_path = "data/sna/network_edges.csv"
    node_path = "data/results/sna_degree.csv"
    if not os.path.exists(edge_path):
        edge_path = "../data/sna/network_edges.csv"
        node_path = "../data/results/sna_degree.csv"
        
    edges = pd.read_csv(edge_path)
    nodes = pd.read_csv(node_path) if os.path.exists(node_path) else None
    return edges, nodes

# Sidebar Navigation
st.sidebar.title("Navigasi Dashboard")
st.sidebar.markdown("Silakan pilih menu analisis:")
page = st.sidebar.radio("Menu", ["🏠 Beranda", "😊 Analisis Emosi (NLP)", "🕸️ Analisis Jaringan (SNA)", "🖼️ Visual Storytelling"])

st.sidebar.markdown("---")
st.sidebar.info(
    "**Tesis MBG Analysis**\n\n"
    "Phygital Gap in Public Policy: "
    "A Computational Social Science Approach."
)

if page == "🏠 Beranda":
    st.title("📊 Phygital Gap in Public Policy")
    st.subheader("Makan Bergizi Gratis (MBG) Crisis on Platform X")
    
    st.markdown("""
    Selamat datang di Dashboard Interaktif Tesis MBG. Aplikasi ini merupakan suplemen visual dari 
    riset *Computational Social Science* yang membedah krisis komunikasi publik akibat kegagalan 
    operasional fisik (*Phygital Gap*).
    
    ### 🎯 Objektif Riset
    Menginvestigasi struktur jaringan diskursus MBG dan membuktikan eksistensi *Phygital Gap* melalui
    kombinasi **Natural Language Processing (IndoBERT 9 Kelas Emosi)** dan **Social Network Analysis (Algoritma Louvain)**.
    
    ### 📈 Temuan Kunci
    - **Hyper-Fragmentation:** Publik terpecah menjadi 333 klaster (Modularity 0.9837) bukan 2 kubu polarisasi biner.
    - **Dominasi Emosi Jijik (Disgust):** Netizen bereaksi menggunakan slang/sarkasme atas kegagalan fisik (makanan beracun, logistik).
    - **Algorithmic Trust:** Akun AI (@grok) mengambil alih otoritas kebenaran (Eigenvector tertinggi) mengalahkan politisi/institusi.
    """)
    
    st.markdown("---")
    st.subheader("🧹 Karakteristik & Pembersihan Data (Preprocessing)")
    st.markdown("Sebelum dilakukan analisis NLP dan Jaringan (SNA), data mentah yang ditarik dari **Twitter API** disaring dengan ketat untuk menjaga validitas ilmiah tesis.")
    
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.metric(label="Data Mentah (Twitter API)", value="5.310", delta="Cuitan Awal")
    with mcol2:
        st.metric(label="Data Terbuang (Noise)", value="1.915", delta="-36%", delta_color="inverse")
    with mcol3:
        st.metric(label="Data Bersih (Final NLP)", value="3.395", delta="Lolos Validasi")
        
    st.info(
        "**Faktor-Faktor Penyortiran (Data Cleaning):**\n"
        "1. **Bot Removal:** Penghapusan akun otomatis tak wajar (aktivitas tinggi tak natural).\n"
        "2. **Spam Filtering:** Membuang tautan promosi, iklan, atau *spam*.\n"
        "3. **De-duplication:** Menghilangkan teks cuitan yang identik 100% (duplikat murni).\n"
        "4. **Text Cleansing:** Memotong URL, *Mentions* (@), dan *Hashtag* (#) agar AI fokus membaca struktur bahasa (*semantics*)."
    )
    st.markdown("---")
    
    st.markdown("Silakan gunakan menu navigasi di sebelah kiri untuk mengeksplorasi data secara interaktif!")
    
elif page == "😊 Analisis Emosi (NLP)":
    st.title("Distribusi Emosi Netizen (IndoBERT)")
    
    df_emotion = load_emotion_data()
    
    # Emotion counts
    emotion_counts = df_emotion['predicted_emotion'].value_counts().reset_index()
    emotion_counts.columns = ['Emosi', 'Jumlah']
    
    # Enforce all 9 categories even if count is 0
    all_emotions = ['Marah', 'Jijik', 'Takut', 'Sedih', 'Bahagia/Senang', 'Netral', 'Percaya', 'Kaget', 'Tertarik']
    missing_emotions = set(all_emotions) - set(emotion_counts['Emosi'])
    if missing_emotions:
        missing_df = pd.DataFrame({'Emosi': list(missing_emotions), 'Jumlah': 0})
        emotion_counts = pd.concat([emotion_counts, missing_df], ignore_index=True)
        
    # Sort for consistent display
    emotion_counts = emotion_counts.sort_values(by='Jumlah', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Grafik Distribusi Emosi (9 Kelas)")
        fig = px.bar(
            emotion_counts, 
            x='Emosi', 
            y='Jumlah',
            color='Emosi',
            title="Frekuensi Kemunculan Emosi",
            text='Jumlah'
        )
        fig.update_layout(xaxis_title="Kategori Emosi", yaxis_title="Jumlah Cuitan")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Persentase Emosi")
        fig_pie = px.pie(
            emotion_counts, 
            names='Emosi', 
            values='Jumlah', 
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Filter & Sampel Cuitan")
    
    selected_emotion = st.selectbox("Pilih Emosi untuk melihat sampel data:", emotion_counts['Emosi'].tolist())
    
    filtered_df = df_emotion[df_emotion['predicted_emotion'] == selected_emotion].sample(n=min(5, len(df_emotion[df_emotion['predicted_emotion'] == selected_emotion])))
    
    st.markdown(f"**Menampilkan 5 sampel acak dari kelas '{selected_emotion}':**")
    for idx, row in filtered_df.iterrows():
        st.info(row['text'])
        
elif page == "🕸️ Analisis Jaringan (SNA)":
    st.title("Pemetaan Jaringan SNA (Louvain)")
    st.markdown("Visualisasi graf interaktif dari wacana MBG di platform X.")
    
    edges, nodes_data = load_network_data()
    
    st.info("💡 **Tips:** Anda bisa melakukan *scroll* untuk Zoom In/Out, dan men-drag *node*.")
    
    # Generate PyVis graph
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.force_atlas_2based()
    
    # To prevent browser from freezing, we will sample the top nodes by degree
    # Assuming nodes_data has a 'Degree' column
    if nodes_data is not None and 'Degree' in nodes_data.columns:
        top_nodes = nodes_data.sort_values(by='Degree', ascending=False).head(150)['Id'].tolist()
    else:
        # Fallback to taking top edges
        G_temp = nx.from_pandas_edgelist(edges, 'Source', 'Target')
        degree_dict = dict(G_temp.degree())
        top_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)[:150]
        
    filtered_edges = edges[edges['Source'].isin(top_nodes) | edges['Target'].isin(top_nodes)]
    
    G = nx.from_pandas_edgelist(filtered_edges, 'Source', 'Target')
    
    # Add nodes and edges to pyvis
    for node in G.nodes():
        # Set node size based on degree
        size = dict(G.degree()).get(node, 1) * 2
        net.add_node(node, label=str(node), title=f"User: {node}", size=size)
        
    for source, target in G.edges():
        net.add_edge(source, target)
        
    # Save graph to HTML
    try:
        path = 'html_files'
        if not os.path.exists(path):
            os.makedirs(path)
        net.save_graph(f'{path}/network.html')
        
        HtmlFile = open(f'{path}/network.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height=650, scrolling=True)
    except Exception as e:
        st.error(f"Gagal memuat visualisasi PyVis: {e}")
        
    st.markdown("---")
    st.subheader("Top Aktor (Centrality)")
    if nodes_data is not None:
        if 'Eigenvector Centrality' in nodes_data.columns:
            st.dataframe(nodes_data[['Id', 'Degree', 'Eigenvector Centrality']].sort_values(by='Eigenvector Centrality', ascending=False).head(10))
        else:
            st.dataframe(nodes_data.head(10))
    else:
        st.warning("Data metrics tidak ditemukan.")

elif page == "🖼️ Visual Storytelling":
    st.title("Galeri Visual Storytelling")
    st.markdown("Berikut adalah 10 visual utama (dari hulu ke hilir) yang merangkum keseluruhan temuan tesis.")
    
    # Define paths (handling local vs cloud execution differences)
    def get_image_path(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        path = os.path.join(project_root, "results", filename)
        return path

    st.subheader("1. Research Pipeline")
    st.image(get_image_path("1_pipeline.png"), use_container_width=True, caption="Figure 1. The Computational Social Science Pipeline for MBG Analysis.")
    st.markdown("---")
    
    st.subheader("2. Dataset Characteristics")
    st.image(get_image_path("2_dataset_characteristics.png"), use_container_width=True, caption="Figure 2. Dataset Preprocessing Funnel.")
    st.markdown("---")
    
    st.subheader("3. Nine-Emotion Distribution")
    st.image(get_image_path("emotion_distribution.png"), use_container_width=True, caption="Figure 3. Distribution of Nine Emotion Classes Predicted by IndoBERT.")
    st.markdown("---")
    
    st.subheader("4. Sarcasm Distribution")
    st.image(get_image_path("3_sarcasm.png"), use_container_width=True, caption="Figure 4. Proportion of Sarcastic and Slang Expressions in Public Discourse.")
    st.markdown("---")
    
    st.subheader("5. IndoBERT Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.image(get_image_path("f1_scores.png"), use_container_width=True, caption="Figure 5A. Performance Metrics (Macro-F1 83%).")
    with col2:
        st.image(get_image_path("confusion_matrix.png"), use_container_width=True, caption="Figure 5B. Confusion Matrix.")
    st.markdown("---")
    
    st.subheader("6. Global Network Structure")
    st.image(get_image_path("6_global_network.png"), use_container_width=True, caption="Figure 6. Global Topological Structure of MBG Discourse on Platform X.")
    st.markdown("---")
    
    st.subheader("7. Community Structure (Louvain)")
    st.image(get_image_path("network_graph.png"), use_container_width=True, caption="Figure 7. Hyper-Fragmented Community Structure (Modularity = 0.9837).")
    st.markdown("---")
    
    st.subheader("8. Top Central Actors")
    st.image(get_image_path("top_actors.png"), use_container_width=True, caption="Figure 8. Top 10 Influential Actors by Network Centrality.")
    st.markdown("---")
    
    st.subheader("9. Emotion × Network (Phygital Overlay)")
    st.image(get_image_path("9_emotion_network.png"), use_container_width=True, caption="Figure 9. Distribution of Emotions Across Dominant Network Communities.")
    st.markdown("---")
    
    st.subheader("10. ABSA Thematic Structure")
    st.image(get_image_path("10_absa_thematic.png"), use_container_width=True, caption="Figure 10. Aspect-Based Sentiments Regarding MBG Implementation.")
    st.markdown("---")
    
    st.subheader("🌟 Visual Masterpiece: Integrated Phygital Gap Analysis")
    st.image(get_image_path("integrated_sna_nlp.png"), use_container_width=True, caption="Master Visual: Integrasi SNA x NLP membuktikan fenomena Phygital Gap.")
