"""
Komponen UI untuk upload file
"""
import streamlit as st
from typing import List, Optional


def render_file_uploader() -> Optional[List]:
    """
    Render komponen upload file dengan opsi 1-3 file.
    
    Returns:
        List file yang diupload atau None
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        text-align: center;
        max-width: 500px;
        margin: 0 auto 1.5rem auto;
    ">
        <h3 style="color: white; margin: 0;">📤 Upload Dataset</h3>
        <p style="color: rgba(255,255,255,0.8); margin-top: 0.5rem; margin-bottom: 0;">
            Upload 1-3 file CSV komentar YouTube
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pilihan jumlah file (di tengah)
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col2:
        num_files = st.selectbox(
            "Jumlah File",
            options=[1, 2, 3],
            index=0,
            help="Pilih berapa file yang ingin diupload"
        )
    
    uploaded_files = []
    
    # Layout berdasarkan jumlah file
    if num_files == 1:
        # Kalau 1 file, width kecil di tengah
        col1, col2, col3 = st.columns([1, 2, 1])
        cols = [col2]
    elif num_files == 2:
        # Kalau 2 file, bagi 2
        col1, col2, col3, col4 = st.columns([0.5, 1, 1, 0.5])
        cols = [col2, col3]
    else:
        # Kalau 3 file, bagi 3
        cols = st.columns(3)
    
    for i in range(num_files):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: #1E1E1E;
                padding: 0.75rem 1rem;
                border-radius: 10px;
                border: 1px solid #333;
                margin-bottom: 0.5rem;
                text-align: center;
            ">
                <p style="color: #667eea; font-weight: bold; margin: 0; font-size: 0.9rem;">
                    📁 Video {i + 1}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            file = st.file_uploader(
                f"Upload CSV Video {i + 1}",
                type=['csv'],
                key=f"uploader_{i}",
                label_visibility="collapsed"
            )
            
            if file:
                uploaded_files.append(file)
                st.success(f"✅ {file.name}")
    
    # Info format CSV (di tengah)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.expander("ℹ️ Format CSV yang Dibutuhkan"):
            st.markdown("""
            File CSV harus memiliki kolom:
            - `publishedAt` - Waktu publish
            - `authorDisplayName` - Nama user
            - `textDisplay` - Isi komentar
            - `likeCount` - Jumlah like
            """)
    
    # Return files jika sudah sesuai jumlah
    if len(uploaded_files) == num_files:
        return uploaded_files
    elif len(uploaded_files) > 0:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.warning(f"⚠️ Upload {num_files - len(uploaded_files)} file lagi")
    
    return None
