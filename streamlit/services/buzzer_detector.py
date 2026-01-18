"""
Service untuk deteksi buzzer menggunakan Rule-based dan Machine Learning
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import (
    THRESHOLDS, SCORE_WEIGHTS, BUZZER_CATEGORIES,
    ISOLATION_FOREST_CONFIG, ML_FEATURES
)


class BuzzerDetector:
    """Handler untuk deteksi buzzer."""
    
    def __init__(self, data: pd.DataFrame, centrality_df: pd.DataFrame):
        self.data = data.copy()
        self.centrality_df = centrality_df
        self.user_activity = None
        self.scaler = StandardScaler()
    
    def aggregate_user_activity(self) -> 'BuzzerDetector':
        """
        Agregasi aktivitas per user.
        
        Returns:
            Self untuk method chaining
        """
        # Aggregasi dasar
        self.user_activity = self.data.groupby('authorDisplayName').agg({
            'publishedAt': ['count', 'min', 'max'],
            'likeCount': 'mean'
        }).reset_index()
        
        self.user_activity.columns = [
            'author', 'comment_count', 'first_post', 
            'last_post', 'avg_likes'
        ]
        
        # Hitung time span dan posting rate
        time_span = (
            self.user_activity['last_post'] - self.user_activity['first_post']
        ).dt.total_seconds() / 3600
        
        self.user_activity['time_span_hours'] = time_span
        self.user_activity['posting_rate'] = (
            self.user_activity['comment_count'] / 
            (self.user_activity['time_span_hours'] + 1)
        )
        
        return self
    
    def calculate_text_similarity(self) -> 'BuzzerDetector':
        """
        Hitung rata-rata text similarity per user.
        
        Returns:
            Self untuk method chaining
        """
        similarities = []
        
        for author in self.user_activity['author']:
            user_comments = self.data[
                self.data['authorDisplayName'] == author
            ]['textDisplay'].values
            
            if len(user_comments) < 2:
                similarities.append(0.0)
                continue
            
            try:
                vectorizer = TfidfVectorizer()
                X = vectorizer.fit_transform(user_comments)
                sim_matrix = cosine_similarity(X)
                mask = ~np.eye(sim_matrix.shape[0], dtype=bool)
                avg_sim = sim_matrix[mask].mean()
                similarities.append(float(avg_sim))
            except Exception:
                similarities.append(0.0)
        
        self.user_activity['avg_text_similarity'] = similarities
        return self
    
    def calculate_text_stats(self) -> 'BuzzerDetector':
        """
        Hitung statistik panjang teks per user.
        
        Returns:
            Self untuk method chaining
        """
        text_stats = self.data.groupby('authorDisplayName')['textLength'].agg([
            'mean', 'std', 'min', 'max'
        ]).reset_index()
        
        text_stats.columns = [
            'author', 'avg_text_length', 'std_text_length',
            'min_text_length', 'max_text_length'
        ]
        
        self.user_activity = self.user_activity.merge(
            text_stats, on='author', how='left'
        )
        self.user_activity['std_text_length'] = (
            self.user_activity['std_text_length'].fillna(0)
        )
        
        return self
    
    def calculate_duplicate_ratio(self) -> 'BuzzerDetector':
        """
        Hitung rasio komentar duplikat per user.
        
        Returns:
            Self untuk method chaining
        """
        dup_ratio = self.data.groupby('authorDisplayName').apply(
            lambda x: x.duplicated(subset=['textDisplay']).sum() / len(x)
        ).reset_index()
        
        dup_ratio.columns = ['author', 'duplicate_ratio']
        
        self.user_activity = self.user_activity.merge(
            dup_ratio, on='author', how='left'
        )
        
        return self
    
    def merge_centrality(self) -> 'BuzzerDetector':
        """
        Merge degree centrality ke user activity.
        
        Returns:
            Self untuk method chaining
        """
        centrality = self.centrality_df[
            self.centrality_df['author'].isin(self.user_activity['author'])
        ]
        
        self.user_activity = self.user_activity.merge(
            centrality, on='author', how='left'
        )
        self.user_activity['degree_centrality'] = (
            self.user_activity['degree_centrality'].fillna(0)
        )
        
        return self
    
    def apply_rule_based_detection(self) -> 'BuzzerDetector':
        """
        Terapkan rule-based detection dengan scoring system.
        
        Returns:
            Self untuk method chaining
        """
        self.user_activity['buzzer_score'] = 0
        
        # Kriteria 1: Posting rate tinggi
        mask = self.user_activity['posting_rate'] > THRESHOLDS['posting_rate']
        self.user_activity.loc[mask, 'buzzer_score'] += SCORE_WEIGHTS['posting_rate']
        
        # Kriteria 2: Text similarity tinggi
        mask = self.user_activity['avg_text_similarity'] > THRESHOLDS['text_similarity']
        self.user_activity.loc[mask, 'buzzer_score'] += SCORE_WEIGHTS['text_similarity']
        
        # Kriteria 3: Banyak komentar
        mask = self.user_activity['comment_count'] > THRESHOLDS['comment_count']
        self.user_activity.loc[mask, 'buzzer_score'] += SCORE_WEIGHTS['comment_count']
        
        # Kriteria 4: Variasi teks rendah
        mask = self.user_activity['std_text_length'] < THRESHOLDS['std_text_length']
        self.user_activity.loc[mask, 'buzzer_score'] += SCORE_WEIGHTS['std_text_length']
        
        # Kriteria 5: Ada duplikat
        mask = self.user_activity['duplicate_ratio'] > THRESHOLDS['duplicate_ratio']
        self.user_activity.loc[mask, 'buzzer_score'] += SCORE_WEIGHTS['duplicate_ratio']
        
        # Kriteria 6: Degree centrality tinggi
        quantile = self.user_activity['degree_centrality'].quantile(
            THRESHOLDS['degree_centrality_quantile']
        )
        mask = self.user_activity['degree_centrality'] > quantile
        self.user_activity.loc[mask, 'buzzer_score'] += SCORE_WEIGHTS['degree_centrality']
        
        # Kategorisasi
        self.user_activity['buzzer_category'] = pd.cut(
            self.user_activity['buzzer_score'],
            bins=BUZZER_CATEGORIES['bins'],
            labels=BUZZER_CATEGORIES['labels']
        )
        
        return self
    
    def apply_ml_detection(self) -> 'BuzzerDetector':
        """
        Terapkan Isolation Forest untuk anomaly detection.
        
        Returns:
            Self untuk method chaining
        """
        # Siapkan fitur
        X = self.user_activity[ML_FEATURES].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        iso_forest = IsolationForest(
            contamination=ISOLATION_FOREST_CONFIG['contamination'],
            random_state=ISOLATION_FOREST_CONFIG['random_state'],
            n_estimators=ISOLATION_FOREST_CONFIG['n_estimators']
        )
        
        # Predict
        predictions = iso_forest.fit_predict(X_scaled)
        scores = iso_forest.score_samples(X_scaled)
        
        self.user_activity['isolation_forest_prediction'] = predictions
        self.user_activity['isolation_forest_score'] = scores
        self.user_activity['ml_buzzer_label'] = (
            self.user_activity['isolation_forest_prediction'].map({
                -1: 'Suspected Buzzer',
                1: 'Normal User'
            })
        )
        
        return self
    
    def detect(self) -> pd.DataFrame:
        """
        Jalankan semua proses deteksi.
        
        Returns:
            DataFrame dengan hasil deteksi
        """
        return (self
                .aggregate_user_activity()
                .calculate_text_similarity()
                .calculate_text_stats()
                .calculate_duplicate_ratio()
                .merge_centrality()
                .apply_rule_based_detection()
                .apply_ml_detection()
                .user_activity)
    
    def get_summary(self) -> dict:
        """
        Mendapatkan ringkasan hasil deteksi.
        
        Returns:
            Dictionary berisi ringkasan
        """
        if self.user_activity is None:
            return {}
        
        return {
            'total_users': len(self.user_activity),
            'high_suspicion': len(self.user_activity[
                self.user_activity['buzzer_category'] == 'High Suspicion'
            ]),
            'medium_suspicion': len(self.user_activity[
                self.user_activity['buzzer_category'] == 'Medium Suspicion'
            ]),
            'low_suspicion': len(self.user_activity[
                self.user_activity['buzzer_category'] == 'Low Suspicion'
            ]),
            'ml_suspected': len(self.user_activity[
                self.user_activity['ml_buzzer_label'] == 'Suspected Buzzer'
            ]),
            'ml_normal': len(self.user_activity[
                self.user_activity['ml_buzzer_label'] == 'Normal User'
            ]),
            'high_confidence': len(self.user_activity[
                (self.user_activity['buzzer_category'] == 'High Suspicion') &
                (self.user_activity['ml_buzzer_label'] == 'Suspected Buzzer')
            ])
        }
