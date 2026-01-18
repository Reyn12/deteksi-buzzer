"""
Service untuk load dan merge data CSV
"""
import pandas as pd
from typing import List, Optional
from config import REQUIRED_COLUMNS


class DataLoader:
    """Handler untuk load dan merge multiple CSV files."""
    
    def __init__(self):
        self.dataframes: List[pd.DataFrame] = []
        self.merged_data: Optional[pd.DataFrame] = None
    
    def load_csv(self, uploaded_file, video_id: str) -> pd.DataFrame:
        """
        Load single CSV file dan tambahkan video_id.
        
        Args:
            uploaded_file: File yang diupload dari Streamlit
            video_id: ID untuk identifikasi video
            
        Returns:
            DataFrame yang sudah ditambahkan video_id
        """
        df = pd.read_csv(uploaded_file)
        df['video_id'] = video_id
        return df
    
    def validate_columns(self, df: pd.DataFrame) -> bool:
        """
        Validasi apakah CSV memiliki kolom yang dibutuhkan.
        
        Args:
            df: DataFrame untuk divalidasi
            
        Returns:
            True jika valid, False jika tidak
        """
        return all(col in df.columns for col in REQUIRED_COLUMNS)
    
    def load_multiple_files(self, files: List) -> pd.DataFrame:
        """
        Load multiple CSV files dan merge jadi satu DataFrame.
        
        Args:
            files: List file yang diupload
            
        Returns:
            DataFrame hasil merge
        """
        self.dataframes = []
        
        for idx, file in enumerate(files, 1):
            video_id = f"video_{idx}"
            df = self.load_csv(file, video_id)
            
            if not self.validate_columns(df):
                raise ValueError(
                    f"File {file.name} tidak memiliki kolom yang dibutuhkan. "
                    f"Kolom wajib: {REQUIRED_COLUMNS}"
                )
            
            self.dataframes.append(df)
        
        # Merge semua dataframes
        self.merged_data = pd.concat(self.dataframes, ignore_index=True)
        return self.merged_data
    
    def get_stats(self) -> dict:
        """
        Mendapatkan statistik data yang sudah di-load.
        
        Returns:
            Dictionary berisi statistik data
        """
        if self.merged_data is None:
            return {}
        
        return {
            'total_rows': len(self.merged_data),
            'total_files': len(self.dataframes),
            'total_authors': self.merged_data['authorDisplayName'].nunique(),
            'columns': list(self.merged_data.columns),
            'per_video': self.merged_data.groupby('video_id').size().to_dict()
        }
