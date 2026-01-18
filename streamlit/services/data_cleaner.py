"""
Service untuk membersihkan dan preprocessing data
"""
import pandas as pd
import numpy as np
from utils.helpers import clean_text


class DataCleaner:
    """Handler untuk data cleaning dan preprocessing."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.duplicates_removed = 0
        self.missing_filled = 0
    
    def remove_duplicates(self) -> 'DataCleaner':
        """
        Hapus baris duplikat berdasarkan authorDisplayName dan textDisplay.
        
        Returns:
            Self untuk method chaining
        """
        original_len = len(self.data)
        self.data = self.data.drop_duplicates(
            subset=['authorDisplayName', 'textDisplay'],
            keep='first'
        )
        self.duplicates_removed = original_len - len(self.data)
        return self
    
    def handle_missing_values(self) -> 'DataCleaner':
        """
        Handle missing values pada data.
        
        Returns:
            Self untuk method chaining
        """
        # Hitung missing values sebelum dihandle
        self.missing_filled = self.data['authorDisplayName'].isna().sum()
        
        # Drop rows dengan authorDisplayName kosong
        self.data = self.data.dropna(subset=['authorDisplayName'])
        
        # Fill missing likeCount dengan 0
        self.data['likeCount'] = self.data['likeCount'].fillna(0)
        
        return self
    
    def convert_datetime(self) -> 'DataCleaner':
        """
        Konversi kolom publishedAt ke datetime.
        
        Returns:
            Self untuk method chaining
        """
        self.data['publishedAt'] = pd.to_datetime(
            self.data['publishedAt'],
            errors='coerce'
        )
        return self
    
    def clean_text_column(self) -> 'DataCleaner':
        """
        Bersihkan kolom textDisplay.
        
        Returns:
            Self untuk method chaining
        """
        self.data['textDisplay'] = self.data['textDisplay'].apply(clean_text)
        return self
    
    def add_text_length(self) -> 'DataCleaner':
        """
        Tambahkan kolom panjang teks (jumlah kata).
        
        Returns:
            Self untuk method chaining
        """
        self.data['textLength'] = self.data['textDisplay'].apply(
            lambda x: len(str(x).split())
        )
        return self
    
    def process_all(self) -> pd.DataFrame:
        """
        Jalankan semua proses cleaning.
        
        Returns:
            DataFrame yang sudah dibersihkan
        """
        return (self
                .remove_duplicates()
                .handle_missing_values()
                .convert_datetime()
                .clean_text_column()
                .add_text_length()
                .data)
    
    def get_cleaning_stats(self) -> dict:
        """
        Mendapatkan statistik proses cleaning.
        
        Returns:
            Dictionary berisi statistik cleaning
        """
        return {
            'duplicates_removed': self.duplicates_removed,
            'missing_filled': self.missing_filled,
            'final_rows': len(self.data)
        }
