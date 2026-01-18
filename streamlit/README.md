# 🔍 Deteksi Buzzer - YouTube Comments Analyzer

Aplikasi untuk mendeteksi aktivitas **buzzer** pada komentar YouTube menggunakan kombinasi **Rule-Based Detection** dan **Machine Learning (Isolation Forest)**.

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Requirements](#-requirements)
- [Instalasi](#-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Penggunaan](#-penggunaan)
- [Struktur Project](#-struktur-project)
- [Metodologi](#-metodologi)
- [Tim Pengembang](#-tim-pengembang)

## ✨ Fitur

- Upload 1-3 file CSV komentar YouTube
- Preprocessing otomatis (cleaning, normalisasi)
- Social Network Analysis (SNA)
- Rule-Based Detection dengan 6 kriteria
- Machine Learning dengan Isolation Forest
- Visualisasi interaktif (pie chart, scatter plot)
- Export hasil ke CSV
- Dokumentasi lengkap di dalam aplikasi

## 📦 Requirements

- Python 3.8 atau lebih baru
- pip (Python package manager)

### Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
networkx>=3.1
plotly>=5.18.0
```

## 🛠️ Instalasi

### 1. Clone atau Download Project

```bash
# Jika menggunakan git
git clone <https://github.com/Reyn12/deteksi-buzzer>
cd streamlit

# Atau extract file zip dan masuk ke folder streamlit
cd path/to/streamlit
```

### 2. (Opsional) Buat Virtual Environment

Disarankan menggunakan virtual environment untuk menghindari konflik dependencies.

```bash
# Buat virtual environment
python3 -m venv venv

# Aktivasi virtual environment
# MacOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Menggunakan pip3 (MacOS/Linux)
pip3 install -r requirements.txt

# Atau menggunakan pip (Windows/jika pip3 tidak tersedia)
pip install -r requirements.txt
```

Jika terjadi error, install satu per satu:

```bash
pip3 install streamlit pandas numpy scikit-learn networkx plotly
```

## 🚀 Cara Menjalankan

### Opsi 1: Menggunakan streamlit langsung

```bash
streamlit run main.py
```

### Opsi 2: Menggunakan python module

```bash
python3 -m streamlit run main.py
```

Aplikasi akan terbuka di browser pada alamat: `http://localhost:8501`

### Troubleshooting

**Error: `command not found: streamlit`**
```bash
# Gunakan python module
python3 -m streamlit run main.py
```

**Error: `command not found: pip`**
```bash
# Gunakan pip3
pip3 install -r requirements.txt
```

**Error: `ModuleNotFoundError`**
```bash
# Pastikan sudah install semua dependencies
pip3 install streamlit pandas numpy scikit-learn networkx plotly
```

## 📖 Penggunaan

### 1. Pilih Menu

Di sidebar kiri, pilih:
- **🚀 Main Feature** - Untuk deteksi buzzer
- **📚 Dokumentasi** - Untuk melihat penjelasan metodologi

### 2. Upload File CSV

1. Pilih jumlah file (1, 2, atau 3)
2. Upload file CSV komentar YouTube
3. Format CSV yang dibutuhkan:
   - `publishedAt` - Waktu komentar dipublish
   - `authorDisplayName` - Nama user/author
   - `textDisplay` - Isi komentar
   - `likeCount` - Jumlah like

### 3. Jalankan Deteksi

1. Klik tombol **🚀 Deteksi Buzzer**
2. Tunggu proses selesai
3. Lihat hasil analisis

### 4. Analisis Hasil

- **Summary Cards** - Ringkasan jumlah user per kategori
- **Pie Charts** - Distribusi kategori buzzer
- **Scatter Plot** - Visualisasi posting rate vs text similarity
- **Tabel** - Detail top suspected buzzers

### 5. Export Hasil

Klik tombol **📥 Download CSV** untuk mengunduh hasil deteksi.

## 📁 Struktur Project

```
streamlit/
├── main.py                    # Entry point aplikasi
├── config.py                  # Konfigurasi & konstanta
├── requirements.txt           # Dependencies
├── README.md                  # Dokumentasi ini
├── components/
│   ├── __init__.py
│   ├── file_uploader.py      # Komponen upload file
│   ├── results_display.py    # Komponen tampilan hasil
│   └── docs_page.py          # Halaman dokumentasi
├── services/
│   ├── __init__.py
│   ├── data_loader.py        # Load & merge CSV
│   ├── data_cleaner.py       # Preprocessing data
│   ├── feature_extractor.py  # Ekstraksi fitur
│   ├── network_analyzer.py   # Social Network Analysis
│   └── buzzer_detector.py    # Deteksi buzzer
└── utils/
    ├── __init__.py
    └── helpers.py            # Fungsi helper
```

## 🔬 Metodologi

### Rule-Based Detection

Sistem scoring dengan 6 kriteria:

| Kriteria | Threshold | Skor |
|----------|-----------|------|
| Posting Rate | > 2 komentar/jam | +1 |
| Text Similarity | > 0.7 | +2 |
| Comment Count | > 10 komentar | +1 |
| Std Text Length | < 2 | +1 |
| Duplicate Ratio | > 0 | +2 |
| Degree Centrality | > Q75 | +1 |

**Klasifikasi:**
- **High Suspicion**: Skor ≥ 4
- **Medium Suspicion**: Skor 2-3
- **Low Suspicion**: Skor 0-1

### Machine Learning (Isolation Forest)

- Algoritma: Isolation Forest
- Contamination: 10% (estimasi proporsi buzzer)
- Fitur: comment_count, posting_rate, avg_text_similarity, std_text_length, duplicate_ratio, degree_centrality

### High Confidence Buzzers

User yang terdeteksi oleh **kedua metode**:
- Rule-Based: High Suspicion
- Machine Learning: Suspected Buzzer

## 👥 Tim Pengembang

**Kelompok 3**

| Nama | NIM | Role |
|------|-----|------|
| Muhamad Hilmi F | 10122028 | Project Manager |
| Renaldi Maulana | 10122002 | Member |
| Muhammad Rizky F | 10122007 | Member |
| Alif Vidya | 10122029 | Member |
| Hamid Abdul Aziz | 10122038 | Member |

---

Made with ❤️ for PSD TUBES - Deteksi Buzzer YouTube Comments
