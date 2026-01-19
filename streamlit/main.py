"""
Deteksi Buzzer - Streamlit Application
Entry point untuk aplikasi deteksi buzzer YouTube comments

Author: PSD TUBES Team
"""
import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from components.file_uploader import render_file_uploader
from components.results_display import render_results
from components.docs_page import render_docs
from services.data_loader import DataLoader
from services.data_cleaner import DataCleaner
from services.feature_extractor import FeatureExtractor
from services.network_analyzer import NetworkAnalyzer
from services.buzzer_detector import BuzzerDetector


def setup_page():
    """Setup konfigurasi halaman Streamlit."""
    st.set_page_config(
        page_title="Deteksi Buzzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS untuk UI modern (Light Mode)
    st.markdown("""
    <style>
        /* Main background - Light Mode */
        .stApp {
            background: #f8f9fa;
        }
        
        /* Hide default header */
        header[data-testid="stHeader"] {
            background: #ffffff;
            border-bottom: 1px solid #e0e0e0;
        }
        
        /* Sidebar styling - Light Mode */
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e0e0e0;
            min-width: 280px;
            max-width: 280px;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            width: 280px;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: #333;
            font-weight: bold;
        }
        
        /* Cards styling - Light Mode */
        .stMetric {
            background: #ffffff;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 2rem !important;
            border-radius: 10px !important;
            font-weight: bold !important;
            transition: all 0.3s ease;
        }
        
        .stButton > button p,
        .stButton > button span {
            color: white !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* File uploader - Light Mode */
        .stFileUploader {
            background: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            border: 1px solid #e0e0e0;
        }
        
        .stFileUploader label,
        .stFileUploader span,
        .stFileUploader p,
        .stFileUploader div,
        .stFileUploader small {
            color: #333 !important;
        }
        
        [data-testid="stFileUploader"] section {
            background: #f8f9fa !important;
            border: 1px dashed #ccc !important;
        }
        
        [data-testid="stFileUploader"] section span,
        [data-testid="stFileUploader"] section small {
            color: #666 !important;
        }
        
        /* Uploaded file name */
        [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] small {
            color: #333 !important;
        }
        
        /* Browse Files button - Light Mode */
        [data-testid="stFileUploader"] button {
            background: #ffffff !important;
            color: #333 !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        [data-testid="stFileUploader"] button:hover {
            background: #f0f0f0 !important;
            border-color: #667eea !important;
        }
        
        /* Download button - Light Mode */
        [data-testid="stDownloadButton"] button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.5rem 1rem !important;
        }
        
        [data-testid="stDownloadButton"] button:hover {
            opacity: 0.9 !important;
            transform: translateY(-1px);
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Tabs - Light Mode */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #666;
            border-radius: 10px 10px 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Dataframe - Light Mode */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        
        .stDataFrame [data-testid="stDataFrameResizable"] {
            background: #ffffff !important;
        }
        
        .stDataFrame th {
            background: #667eea !important;
            color: white !important;
        }
        
        .stDataFrame td {
            color: #333 !important;
        }
        
        [data-testid="stDataFrame"] div[class*="glideDataEditor"] {
            background: #ffffff !important;
        }
        
        [data-testid="stDataFrame"] [data-testid="glide-cell"] {
            color: #333 !important;
        }
        
        /* Dataframe header - Glide Data Grid */
        [data-testid="stDataFrame"] [class*="header"] {
            background: #667eea !important;
            color: #fff !important;
        }
        
        [data-testid="stDataFrame"] canvas + div {
            color: #fff !important;
        }
        
        [data-testid="stDataFrame"] [class*="dvn-scroller"] [class*="header"] span,
        [data-testid="stDataFrame"] [role="columnheader"] {
            color: #fff !important;
        }
        
        /* Expander - Light Mode */
        .streamlit-expanderHeader {
            background: #ffffff !important;
            border-radius: 10px;
            border: 1px solid #e0e0e0 !important;
            color: #333 !important;
        }
        
        .streamlit-expanderHeader p,
        .streamlit-expanderHeader span,
        .streamlit-expanderHeader svg {
            color: #333 !important;
            fill: #333 !important;
        }
        
        [data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 10px !important;
        }
        
        [data-testid="stExpander"] details {
            background: #ffffff !important;
        }
        
        [data-testid="stExpander"] summary {
            color: #333 !important;
        }
        
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary svg {
            color: #333 !important;
            fill: #333 !important;
        }
        
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
            color: #333 !important;
        }
        
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] ul {
            color: #333 !important;
        }
        
        /* Code/backtick tetap putih dengan background gelap */
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] code {
            color: #fff !important;
            background: #667eea !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
        }
        
        /* Expander header text - hitam saat collapsed, tetap readable saat expanded */
        [data-testid="stExpander"] summary {
            background: #ffffff !important;
        }
        
        [data-testid="stExpander"] summary span {
            color: #333 !important;
        }
        
        /* Success/Warning/Info boxes */
        .stAlert {
            border-radius: 10px;
        }
        
        /* Markdown tables - Light Mode */
        [data-testid="stMarkdownContainer"] table {
            color: #333 !important;
        }
        
        [data-testid="stMarkdownContainer"] table th {
            background: #667eea !important;
            color: #fff !important;
            padding: 0.5rem 1rem !important;
        }
        
        [data-testid="stMarkdownContainer"] table td {
            color: #333 !important;
            background: #fff !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        /* Code blocks - Light Mode */
        [data-testid="stCode"] {
            background: #1e1e1e !important;
            border-radius: 10px !important;
        }
        
        [data-testid="stCode"] code {
            color: #d4d4d4 !important;
        }
        
        /* Markdown general - Light Mode (tanpa !important biar inline style bisa override) */
        [data-testid="stMarkdownContainer"] {
            color: #333;
        }
        
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] ul,
        [data-testid="stMarkdownContainer"] ol {
            color: #333;
        }
        
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 {
            color: #333;
        }
        
        /* Horizontal rule */
        [data-testid="stMarkdownContainer"] hr {
            border-color: #e0e0e0 !important;
        }
        
        /* Caption - Light Mode */
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        .stCaption,
        .stCaption p {
            color: #666 !important;
        }
        
        /* Selectbox - Light Mode */
        .stSelectbox label {
            color: #333 !important;
        }
        
        .stSelectbox > div > div {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: #ffffff;
        }
        
        .stSelectbox [data-baseweb="select"] > div {
            background: #ffffff;
            border-color: #e0e0e0;
            color: #333 !important;
        }
        
        /* Selectbox text & icon */
        .stSelectbox [data-baseweb="select"] span {
            color: #333 !important;
        }
        
        .stSelectbox [data-baseweb="select"] svg {
            fill: #333 !important;
        }
        
        /* Dropdown menu - Light Mode */
        [data-baseweb="popover"] {
            background: #ffffff !important;
        }
        
        [data-baseweb="menu"] {
            background: #ffffff !important;
        }
        
        [data-baseweb="menu"] li {
            background: #ffffff !important;
            color: #333 !important;
        }
        
        [data-baseweb="menu"] li:hover {
            background: #f0f0f0 !important;
        }
        
        /* Sidebar radio buttons - Light Mode */
        [data-testid="stSidebar"] .stRadio > div {
            gap: 0.5rem;
            flex-direction: column;
        }
        
        [data-testid="stSidebar"] .stRadio > div > label {
            background: #f8f9fa !important;
            padding: 1rem 1.5rem !important;
            border-radius: 10px !important;
            border: 1px solid #e0e0e0 !important;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] .stRadio > div > label p,
        [data-testid="stSidebar"] .stRadio > div > label span,
        [data-testid="stSidebar"] .stRadio > div > label div {
            color: #333 !important;
        }
        
        [data-testid="stSidebar"] .stRadio > div > label:hover {
            border-color: #667eea !important;
            background: #eef0f5 !important;
        }
        
        [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
        [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border-color: transparent !important;
        }
        
        [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] p,
        [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] span,
        [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] div,
        [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) p,
        [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) span,
        [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) div {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <h2 style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            ">🔍 Menu</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        page = st.radio(
            "Navigation",
            options=["🚀 Main Feature", "📚 Dokumentasi"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Info box - Light Mode
        st.markdown("""
        <div style="
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin-top: 1rem;
        ">
            <p style="color: #333; font-size: 0.85rem; margin: 0;">
                <b style="color: #667eea;">Kelompok 3</b><br><br>
                Muhamad Hilmi F - 10122028 (PM)<br>
                Renaldi Maulana - 10122002<br>
                Muhammad Rizky F - 10122007<br>
                Alif Vidya - 10122029<br>
                Hamid Abdul Aziz - 10122038
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return page


def render_main_header():
    """Render header untuk main feature."""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    ">
        <h1 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        ">
            🔍 Deteksi Buzzer
        </h1>
        <p style="
            color: #666;
            font-size: 1.1rem;
        ">
            Analisis komentar YouTube untuk mendeteksi aktivitas buzzer
            <br>
            menggunakan Rule-Based Detection & Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)


def process_detection(files, progress_container):
    """
    Proses deteksi buzzer dari files yang diupload.
    
    Args:
        files: List file CSV yang diupload
        progress_container: Container untuk progress UI
        
    Returns:
        Tuple (user_activity DataFrame, summary dict)
    """
    try:
        with progress_container:
            # Progress UI - Light Mode
            st.markdown("""
            <div style="
                background: #ffffff;
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                max-width: 500px;
                margin: 0 auto;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <h4 style="color: #667eea; margin: 0 0 1rem 0; text-align: center;">
                    ⏳ Memproses Data...
                </h4>
            """, unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Step 1: Load data
            status_text.markdown("📂 **Memuat data...**")
            progress_bar.progress(10)
            loader = DataLoader()
            merged_data = loader.load_multiple_files(files)
            load_stats = loader.get_stats()
            
            # Step 2: Clean data
            status_text.markdown("🧹 **Membersihkan data...**")
            progress_bar.progress(25)
            cleaner = DataCleaner(merged_data)
            cleaned_data = cleaner.process_all()
            clean_stats = cleaner.get_cleaning_stats()
            
            # Step 3: Extract features
            status_text.markdown("⚙️ **Ekstraksi fitur...**")
            progress_bar.progress(40)
            extractor = FeatureExtractor(cleaned_data)
            featured_data = extractor.extract_all()
            tfidf_matrix = extractor.get_tfidf_matrix()
            
            # Step 4: Network analysis
            status_text.markdown("🕸️ **Analisis jaringan...**")
            progress_bar.progress(55)
            network = NetworkAnalyzer(featured_data, tfidf_matrix)
            centrality_df = network.analyze(threshold=0.3)
            network_stats = network.get_network_stats()
            graph = network.get_graph()
            
            # Step 5: Detect buzzers
            status_text.markdown("🔍 **Mendeteksi buzzer...**")
            progress_bar.progress(75)
            detector = BuzzerDetector(featured_data, centrality_df)
            user_activity = detector.detect()
            summary = detector.get_summary()
            
            # Add additional stats to summary
            summary['load_stats'] = load_stats
            summary['clean_stats'] = clean_stats
            summary['network_stats'] = network_stats
            summary['graph'] = graph
            
            # Done
            status_text.markdown("✅ **Selesai!**")
            progress_bar.progress(100)
        
        return user_activity, summary
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None, None


def render_main_feature():
    """Render halaman main feature (deteksi buzzer)."""
    render_main_header()
    
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    
    # File upload section
    uploaded_files = render_file_uploader()
    
    # Detection button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        detect_button = st.button(
            "🚀 Deteksi Buzzer",
            disabled=uploaded_files is None,
            use_container_width=True
        )
    
    # Process detection
    if detect_button and uploaded_files:
        # Container untuk progress
        progress_container = st.empty()
        
        results, summary = process_detection(uploaded_files, progress_container)
        
        # Clear progress setelah selesai
        progress_container.empty()
        
        if results is not None:
            st.session_state.results = results
            st.session_state.summary = summary
            st.rerun()
    
    # Display results
    if st.session_state.results is not None:
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show processing stats
        with st.expander("📊 Statistik Pemrosesan", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Komentar",
                    st.session_state.summary['load_stats']['total_rows']
                )
            with col2:
                st.metric(
                    "Duplikat Dihapus",
                    st.session_state.summary['clean_stats']['duplicates_removed']
                )
            with col3:
                st.metric(
                    "Network Edges",
                    st.session_state.summary['network_stats'].get('edges', 0)
                )
        
        # Render main results
        render_results(
            st.session_state.results,
            st.session_state.summary
        )


def main():
    """Main function untuk aplikasi."""
    setup_page()
    
    # Render sidebar dan dapatkan halaman yang dipilih
    selected_page = render_sidebar()
    
    # Render halaman sesuai pilihan
    if selected_page == "🚀 Main Feature":
        render_main_feature()
    elif selected_page == "📚 Dokumentasi":
        render_docs()


if __name__ == "__main__":
    main()
