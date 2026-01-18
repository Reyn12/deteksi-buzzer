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
    
    # Custom CSS untuk UI modern
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: linear-gradient(180deg, #0E1117 0%, #1a1a2e 100%);
        }
        
        /* Hide default header */
        header[data-testid="stHeader"] {
            background: transparent;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #0E1117 100%);
            border-right: 1px solid #333;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: white;
            font-weight: bold;
        }
        
        /* Cards styling */
        .stMetric {
            background: #1E1E1E;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #333;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 10px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* File uploader */
        .stFileUploader {
            background: #1E1E1E;
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #888;
            border-radius: 10px 10px 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Dataframe */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: #1E1E1E;
            border-radius: 10px;
        }
        
        /* Success/Warning/Info boxes */
        .stAlert {
            border-radius: 10px;
        }
        
        /* Sidebar radio buttons */
        .stRadio > div {
            gap: 0.5rem;
        }
        
        .stRadio > div > label {
            background: #1E1E1E;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            border: 1px solid #333;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stRadio > div > label:hover {
            border-color: #667eea;
        }
        
        .stRadio > div > label[data-checked="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: transparent;
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
        
        # Info box
        st.markdown("""
        <div style="
            background: #1E1E1E;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #333;
            margin-top: 1rem;
        ">
            <p style="color: #888; font-size: 0.85rem; margin: 0;">
                <b style="color: #667eea;">Kelompok 3</b><br><br>
                Muhamad Hilmi F<br>
                Renaldi Maulana<br>
                Muhammad Rizky F<br>
                Alif Vidya<br>
                Hamid Abdul Aziz
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
            color: #888;
            font-size: 1.1rem;
        ">
            Analisis komentar YouTube untuk mendeteksi aktivitas buzzer
            <br>
            menggunakan Rule-Based Detection & Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)


def process_detection(files):
    """
    Proses deteksi buzzer dari files yang diupload.
    
    Args:
        files: List file CSV yang diupload
        
    Returns:
        Tuple (user_activity DataFrame, summary dict)
    """
    progress = st.progress(0, "Memulai proses...")
    
    try:
        # Step 1: Load data
        progress.progress(10, "📂 Memuat data...")
        loader = DataLoader()
        merged_data = loader.load_multiple_files(files)
        load_stats = loader.get_stats()
        
        # Step 2: Clean data
        progress.progress(25, "🧹 Membersihkan data...")
        cleaner = DataCleaner(merged_data)
        cleaned_data = cleaner.process_all()
        clean_stats = cleaner.get_cleaning_stats()
        
        # Step 3: Extract features
        progress.progress(40, "⚙️ Ekstraksi fitur...")
        extractor = FeatureExtractor(cleaned_data)
        featured_data = extractor.extract_all()
        tfidf_matrix = extractor.get_tfidf_matrix()
        
        # Step 4: Network analysis
        progress.progress(55, "🕸️ Analisis jaringan...")
        network = NetworkAnalyzer(featured_data, tfidf_matrix)
        centrality_df = network.analyze(threshold=0.3)
        network_stats = network.get_network_stats()
        
        # Step 5: Detect buzzers
        progress.progress(75, "🔍 Mendeteksi buzzer...")
        detector = BuzzerDetector(featured_data, centrality_df)
        user_activity = detector.detect()
        summary = detector.get_summary()
        
        # Add additional stats to summary
        summary['load_stats'] = load_stats
        summary['clean_stats'] = clean_stats
        summary['network_stats'] = network_stats
        
        progress.progress(100, "✅ Selesai!")
        
        return user_activity, summary
        
    except Exception as e:
        progress.empty()
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
        with st.spinner("Memproses..."):
            results, summary = process_detection(uploaded_files)
            
            if results is not None:
                st.session_state.results = results
                st.session_state.summary = summary
    
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
