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
        initial_sidebar_state="collapsed"
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
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render header aplikasi."""
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


def main():
    """Main function untuk aplikasi."""
    setup_page()
    render_header()
    
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="
        text-align: center;
        color: #666;
        padding: 1rem;
    ">
        <p style="font-weight: bold; color: #ffffff;">Kelompok 3</p>
        <p style="font-size: 0.9rem; line-height: 1.8; color: #ffffff;">
            Muhamad Hilmi F - 10122028 (PM)<br>
            Renaldi Maulana - 10122002<br>
            Muhammad Rizky F - 10122007<br>
            Alif Vidya - 10122029<br>
            Hamid Abdul Aziz - 10122038
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
