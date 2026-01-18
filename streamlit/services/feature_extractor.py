"""
Service untuk ekstraksi fitur dari data
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import INDONESIAN_STOPWORDS


class FeatureExtractor:
    """Handler untuk ekstraksi fitur dari data komentar."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.tfidf_matrix = None
        self.vectorizer = None
    
    def extract_time_features(self) -> 'FeatureExtractor':
        """
        Ekstrak fitur waktu dari publishedAt.
        
        Returns:
            Self untuk method chaining
        """
        self.data['year'] = self.data['publishedAt'].dt.year
        self.data['month'] = self.data['publishedAt'].dt.month
        self.data['day'] = self.data['publishedAt'].dt.day
        self.data['day_of_week'] = self.data['publishedAt'].dt.dayofweek
        self.data['hour'] = self.data['publishedAt'].dt.hour
        return self
    
    def extract_text_features(self) -> 'FeatureExtractor':
        """
        Ekstrak fitur dari teks komentar.
        
        Returns:
            Self untuk method chaining
        """
        self.data['text_length_chars'] = self.data['textDisplay'].apply(
            lambda x: len(str(x))
        )
        return self
    
    def create_author_labels(self) -> 'FeatureExtractor':
        """
        Buat label numerik untuk setiap author.
        
        Returns:
            Self untuk method chaining
        """
        self.data['author_label'] = self.data['authorDisplayName'].astype(
            'category'
        ).cat.codes
        return self
    
    def create_tfidf_matrix(self) -> 'FeatureExtractor':
        """
        Buat TF-IDF matrix dari teks komentar.
        
        Returns:
            Self untuk method chaining
        """
        self.vectorizer = TfidfVectorizer(
            stop_words=INDONESIAN_STOPWORDS,
            max_features=1000,
            ngram_range=(1, 2)
        )
        
        # Filter teks yang tidak kosong
        valid_texts = self.data['textDisplay'].fillna('').astype(str)
        self.tfidf_matrix = self.vectorizer.fit_transform(valid_texts)
        
        return self
    
    def calculate_user_text_similarity(self, author_name: str) -> float:
        """
        Hitung rata-rata similarity teks untuk satu user.
        
        Args:
            author_name: Nama author
            
        Returns:
            Rata-rata cosine similarity
        """
        user_comments = self.data[
            self.data['authorDisplayName'] == author_name
        ]['textDisplay'].values
        
        if len(user_comments) < 2:
            return 0.0
        
        try:
            vectorizer_temp = TfidfVectorizer()
            X_temp = vectorizer_temp.fit_transform(user_comments)
            similarity = cosine_similarity(X_temp)
            
            # Ambil rata-rata similarity (exclude diagonal)
            mask = ~np.eye(similarity.shape[0], dtype=bool)
            avg_similarity = similarity[mask].mean()
            return float(avg_similarity)
        except Exception:
            return 0.0
    
    def extract_all(self) -> pd.DataFrame:
        """
        Jalankan semua proses ekstraksi fitur.
        
        Returns:
            DataFrame dengan fitur lengkap
        """
        return (self
                .extract_time_features()
                .extract_text_features()
                .create_author_labels()
                .create_tfidf_matrix()
                .data)
    
    def get_tfidf_matrix(self):
        """Mendapatkan TF-IDF matrix."""
        return self.tfidf_matrix
    
    def get_vectorizer(self):
        """Mendapatkan TF-IDF vectorizer."""
        return self.vectorizer
