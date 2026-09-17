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

# Cache data loading
@st.cache_data
def load_emotion_data():
    # Adjust path assuming run from root 'tesis_mbg'
    path = "data/results/indobert_9_emosi_fixed.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    # Fallback if run inside 'dashboard' folder
    return pd.read_csv("../data/results/indobert_9_emosi_fixed.csv")

@st.cache_data
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
page = st.sidebar.radio("Menu", ["🏠 Beranda", "😊 Analisis Emosi (NLP)", "🕸️ Analisis Jaringan (SNA)"])

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
    
    Silakan gunakan menu navigasi di sebelah kiri untuk mengeksplorasi data secara interaktif!
    """)
    
elif page == "😊 Analisis Emosi (NLP)":
    st.title("Distribusi Emosi Netizen (IndoBERT)")
    
    df_emotion = load_emotion_data()
    
    # Emotion counts
    emotion_counts = df_emotion['label'].value_counts().reset_index()
    emotion_counts.columns = ['Emosi', 'Jumlah']
    
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
    
    filtered_df = df_emotion[df_emotion['label'] == selected_emotion].sample(n=min(5, len(df_emotion[df_emotion['label'] == selected_emotion])))
    
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
