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
        padding: 2rem;
        border-radius: 15px;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    ">
        <h3 style="color: white; margin: 0;">📤 Upload Dataset</h3>
        <p style="color: rgba(255,255,255,0.8); margin-top: 0.5rem;">
            Upload 1-3 file CSV komentar YouTube untuk dianalisis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pilihan jumlah file (di tengah)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        num_files = st.selectbox(
            "Jumlah File",
            options=[1, 2, 3],
            index=0,
            help="Pilih berapa file yang ingin diupload"
        )
    
    uploaded_files = []
    
    # Render uploader sesuai jumlah
    cols = st.columns(num_files)
    
    for i in range(num_files):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: #1E1E1E;
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #333;
                margin-bottom: 1rem;
            ">
                <p style="color: #667eea; font-weight: bold; margin: 0;">
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
    
    # Info format CSV
    with st.expander("ℹ️ Format CSV yang Dibutuhkan"):
        st.markdown("""
        File CSV harus memiliki kolom berikut:
        - `publishedAt` - Waktu komentar dipublish
        - `authorDisplayName` - Nama author/user
        - `textDisplay` - Isi komentar
        - `likeCount` - Jumlah like
        
        **Contoh:**
        ```
        publishedAt,authorDisplayName,textDisplay,likeCount
        2025-11-09T13:20:35Z,@username,Ini adalah komentar,5
        ```
        """)
    
    # Return files jika sudah sesuai jumlah
    if len(uploaded_files) == num_files:
        return uploaded_files
    elif len(uploaded_files) > 0:
        st.warning(f"⚠️ Upload {num_files - len(uploaded_files)} file lagi")
    
    return None
