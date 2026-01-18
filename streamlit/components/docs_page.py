"""
Halaman dokumentasi untuk menjelaskan metodologi deteksi buzzer
"""
import streamlit as st


def render_docs():
    """Render halaman dokumentasi."""
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">📚 Dokumentasi</h1>
        <p style="color: #888;">Penjelasan metodologi dan implementasi deteksi buzzer</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview
    st.markdown("## 🎯 Overview")
    st.markdown("""
    Aplikasi ini mendeteksi **buzzer** pada komentar YouTube menggunakan 
    kombinasi 2 pendekatan:
    
    1. **Rule-Based Detection** - Scoring system dengan 6 kriteria
    2. **Machine Learning** - Isolation Forest untuk Anomaly Detection
    """)
    
    st.markdown("---")
    
    # Metodologi
    st.markdown("## 📊 Metodologi")
    
    with st.expander("### 1. Data Preprocessing", expanded=True):
        st.markdown("""
        **Tahapan preprocessing data:**
        
        | Tahap | Deskripsi |
        |-------|-----------|
        | Load Data | Membaca 1-3 file CSV komentar YouTube |
        | Merge | Menggabungkan semua data dengan menambahkan `video_id` |
        | Remove Duplicates | Menghapus komentar duplikat berdasarkan author & text |
        | Clean Text | Lowercase, hapus emoji, tanda baca, angka |
        | Handle Missing | Drop rows dengan `authorDisplayName` kosong |
        
        **Kolom yang dibutuhkan:**
        - `publishedAt` - Waktu komentar dipublish
        - `authorDisplayName` - Nama user/author
        - `textDisplay` - Isi komentar
        - `likeCount` - Jumlah like
        """)
    
    with st.expander("### 2. Feature Engineering"):
        st.markdown("""
        **Fitur yang diekstrak:**
        
        | Kategori | Fitur | Deskripsi |
        |----------|-------|-----------|
        | Temporal | `posting_rate` | Jumlah komentar per jam |
        | | `time_span_hours` | Rentang waktu posting |
        | Text | `avg_text_similarity` | Rata-rata cosine similarity antar komentar user |
        | | `avg_text_length` | Rata-rata panjang teks |
        | | `std_text_length` | Standar deviasi panjang teks |
        | Behavioral | `comment_count` | Total komentar per user |
        | | `duplicate_ratio` | Rasio komentar duplikat |
        | Network | `degree_centrality` | Koneksi user dalam network SNA |
        """)
    
    with st.expander("### 3. Social Network Analysis (SNA)"):
        st.markdown("""
        **Membangun network berdasarkan text similarity:**
        
        1. Hitung **TF-IDF** dari semua komentar
        2. Hitung **Cosine Similarity** antar komentar
        3. Buat **edge** jika similarity > threshold (0.3)
        4. Hitung **Degree Centrality** setiap user
        
        > User dengan degree centrality tinggi berarti terhubung dengan banyak 
        > user lain (kemungkinan posting konten serupa)
        """)
    
    st.markdown("---")
    
    # Rule-Based Detection
    st.markdown("## 🔍 Rule-Based Detection")
    
    st.markdown("""
    Sistem scoring dengan **6 kriteria**. Setiap kriteria memberikan skor tertentu:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        | Kriteria | Threshold | Skor |
        |----------|-----------|------|
        | Posting Rate | > 2 komentar/jam | +1 |
        | Text Similarity | > 0.7 | +2 |
        | Comment Count | > 10 komentar | +1 |
        """)
    
    with col2:
        st.markdown("""
        | Kriteria | Threshold | Skor |
        |----------|-----------|------|
        | Std Text Length | < 2 | +1 |
        | Duplicate Ratio | > 0 | +2 |
        | Degree Centrality | > Q75 | +1 |
        """)
    
    st.markdown("""
    **Klasifikasi berdasarkan total skor:**
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: #FF4B4B; padding: 1rem; border-radius: 10px; text-align: center;">
            <b style="color: white;">High Suspicion</b><br>
            <span style="color: rgba(255,255,255,0.8);">Skor ≥ 4</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: #FFA500; padding: 1rem; border-radius: 10px; text-align: center;">
            <b style="color: white;">Medium Suspicion</b><br>
            <span style="color: rgba(255,255,255,0.8);">Skor 2-3</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: #00CC96; padding: 1rem; border-radius: 10px; text-align: center;">
            <b style="color: white;">Low Suspicion</b><br>
            <span style="color: rgba(255,255,255,0.8);">Skor 0-1</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Machine Learning
    st.markdown("## 🤖 Machine Learning Detection")
    
    st.markdown("""
    Menggunakan **Isolation Forest** untuk anomaly detection:
    """)
    
    st.code("""
# Fitur yang digunakan
features = [
    'comment_count',
    'posting_rate',
    'avg_text_similarity',
    'std_text_length',
    'duplicate_ratio',
    'degree_centrality'
]

# Model configuration
IsolationForest(
    contamination=0.1,    # Estimasi 10% adalah buzzer
    n_estimators=100,
    random_state=42
)
    """, language="python")
    
    st.markdown("""
    **Cara kerja Isolation Forest:**
    
    1. Membangun ensemble of trees dengan random splits
    2. Anomali (buzzer) lebih mudah di-isolate → path lebih pendek
    3. Normal users membutuhkan lebih banyak splits → path lebih panjang
    4. Score negatif menandakan anomali
    """)
    
    st.markdown("---")
    
    # High Confidence
    st.markdown("## 🚨 High Confidence Buzzers")
    
    st.markdown("""
    **High Confidence Buzzer** adalah user yang terdeteksi oleh **KEDUA** metode:
    
    - ✅ Rule-Based: **High Suspicion** (skor ≥ 4)
    - ✅ Machine Learning: **Suspected Buzzer** (anomaly)
    
    > Kombinasi kedua metode meningkatkan confidence level deteksi
    """)
    
    st.markdown("---")
    
    # Limitasi
    st.markdown("## ⚠️ Limitasi")
    
    st.warning("""
    **Limitasi sistem deteksi:**
    
    - Data tidak memiliki metadata akun (umur akun, history, dll)
    - Tidak ada informasi reply structure (parent-child comments)
    - Engagement data (likeCount) mayoritas 0
    - Deteksi bersifat **probabilistik**, bukan definitif
    - Validasi manual tetap diperlukan untuk konfirmasi final
    """)
    
    st.markdown("---")
    
    # Interpretasi
    st.markdown("## 💡 Interpretasi Hasil")
    
    st.info("""
    **Indikator kuat aktivitas buzzer:**
    
    - Posting rate tinggi dalam waktu singkat
    - Copy-paste konten (text similarity tinggi)
    - Komentar duplikat persis
    - Variasi teks sangat rendah
    - Terhubung dengan banyak user lain yang posting konten serupa
    """)
    
    st.success("""
    **Rekomendasi:**
    
    1. Review manual untuk High Confidence Buzzers
    2. Analisis temporal pattern lebih detail (burst detection)
    3. Validasi dengan ground truth jika tersedia
    4. Monitoring berkelanjutan untuk pattern baru
    """)
