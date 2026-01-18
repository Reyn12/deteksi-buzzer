"""
Konfigurasi dan konstanta untuk aplikasi Deteksi Buzzer
"""

# Kolom yang dibutuhkan dari CSV
REQUIRED_COLUMNS = ['publishedAt', 'authorDisplayName', 'textDisplay', 'likeCount']

# Thresholds untuk rule-based detection
THRESHOLDS = {
    'posting_rate': 2,           # Komentar per jam
    'text_similarity': 0.7,      # Cosine similarity
    'comment_count': 10,         # Jumlah komentar
    'std_text_length': 2,        # Standar deviasi panjang teks
    'duplicate_ratio': 0,        # Rasio duplikat
    'degree_centrality_quantile': 0.75  # Quantile untuk degree centrality
}

# Skor untuk setiap kriteria
SCORE_WEIGHTS = {
    'posting_rate': 1,
    'text_similarity': 2,
    'comment_count': 1,
    'std_text_length': 1,
    'duplicate_ratio': 2,
    'degree_centrality': 1
}

# Kategori buzzer berdasarkan skor
BUZZER_CATEGORIES = {
    'bins': [-1, 1, 3, 10],
    'labels': ['Low Suspicion', 'Medium Suspicion', 'High Suspicion']
}

# Isolation Forest parameters
ISOLATION_FOREST_CONFIG = {
    'contamination': 0.1,
    'random_state': 42,
    'n_estimators': 100
}

# Fitur untuk ML model
ML_FEATURES = [
    'comment_count',
    'posting_rate',
    'avg_text_similarity',
    'std_text_length',
    'duplicate_ratio',
    'degree_centrality'
]

# Custom stopwords Bahasa Indonesia
INDONESIAN_STOPWORDS = [
    'dan', 'di', 'ke', 'dari', 'yang', 'ini', 'itu', 'untuk', 'dengan',
    'adalah', 'pada', 'juga', 'tidak', 'akan', 'atau', 'ada', 'mereka',
    'sudah', 'saya', 'aku', 'kamu', 'dia', 'kita', 'kami', 'kalian',
    'nya', 'bisa', 'hanya', 'lebih', 'sangat', 'seperti', 'karena',
    'tapi', 'jadi', 'ya', 'kan', 'aja', 'dong', 'sih', 'nih', 'deh',
    'loh', 'wah', 'oh', 'ah', 'eh', 'lah', 'mah', 'gak', 'ga', 'ngga',
    'nggak', 'enggak', 'yg', 'yaa', 'yaaa', 'udah', 'udh', 'udahh'
]

# Warna untuk visualisasi
COLORS = {
    'high_suspicion': '#FF4B4B',
    'medium_suspicion': '#FFA500',
    'low_suspicion': '#00CC96',
    'primary': '#667eea',
    'secondary': '#764ba2',
    'background': '#0E1117',
    'card': '#1E1E1E'
}
