"""
Helper functions untuk aplikasi Deteksi Buzzer
"""
import re
from config import COLORS


def clean_text(text: str) -> str:
    """
    Membersihkan teks dari karakter khusus, angka, dan normalisasi.
    
    Args:
        text: Teks yang akan dibersihkan
        
    Returns:
        Teks yang sudah dibersihkan
    """
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text)  # Hapus spasi ganda
    text = re.sub(r'[^\w\s]', '', text)  # Hapus tanda baca
    text = re.sub(r'\d+', '', text)  # Hapus angka
    # Normalisasi kata
    text = text.replace('dapet', 'dapat')
    text = text.replace('gak', 'tidak')
    text = text.replace('ga', 'tidak')
    return text.strip()


def format_number(num: float) -> str:
    """
    Format angka untuk tampilan yang lebih readable.
    
    Args:
        num: Angka yang akan diformat
        
    Returns:
        String angka yang sudah diformat
    """
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(int(num))


def get_color_by_category(category: str) -> str:
    """
    Mendapatkan warna berdasarkan kategori buzzer.
    
    Args:
        category: Kategori buzzer (High/Medium/Low Suspicion)
        
    Returns:
        Kode warna hex
    """
    color_map = {
        'High Suspicion': COLORS['high_suspicion'],
        'Medium Suspicion': COLORS['medium_suspicion'],
        'Low Suspicion': COLORS['low_suspicion'],
        'Suspected Buzzer': COLORS['high_suspicion'],
        'Normal User': COLORS['low_suspicion']
    }
    return color_map.get(category, COLORS['primary'])


def calculate_percentage(part: int, total: int) -> float:
    """
    Hitung persentase dengan aman (avoid division by zero).
    
    Args:
        part: Bagian dari total
        total: Total keseluruhan
        
    Returns:
        Persentase dalam float
    """
    if total == 0:
        return 0.0
    return (part / total) * 100
