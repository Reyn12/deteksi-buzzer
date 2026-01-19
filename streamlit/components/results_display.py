"""
Komponen UI untuk menampilkan hasil deteksi
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS
from utils.helpers import calculate_percentage


def render_summary_cards(summary: dict):
    """Render kartu ringkasan hasil deteksi."""
    st.markdown('<h3 style="color: #333;">📊 Ringkasan Hasil</h3>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h2 style="color: white; margin: 0;">{summary['total_users']:,}</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h2 style="color: #333; margin: 0;">{summary['high_suspicion']}</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">High Suspicion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #FFA500, #FFB347);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h2 style="color: white; margin: 0;">{summary['medium_suspicion']}</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">Medium Suspicion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #00CC96, #00E5AA);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h2 style="color: white; margin: 0;">{summary['high_confidence']}</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">High Confidence</p>
        </div>
        """, unsafe_allow_html=True)


def render_distribution_chart(user_activity: pd.DataFrame):
    """Render chart distribusi kategori buzzer."""
    st.markdown('<h3 style="color: #333;">📈 Distribusi Kategori</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rule-based distribution
        rule_counts = user_activity['buzzer_category'].value_counts()
        fig1 = px.pie(
            values=rule_counts.values,
            names=rule_counts.index,
            title="Rule-Based Detection",
            color=rule_counts.index,
            color_discrete_map={
                'High Suspicion': COLORS['high_suspicion'],
                'Medium Suspicion': COLORS['medium_suspicion'],
                'Low Suspicion': COLORS['low_suspicion']
            }
        )
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#333',
            legend=dict(font=dict(color='#333'))
        )
        st.plotly_chart(fig1)
    
    with col2:
        # ML distribution
        ml_counts = user_activity['ml_buzzer_label'].value_counts()
        fig2 = px.pie(
            values=ml_counts.values,
            names=ml_counts.index,
            title="Machine Learning Detection",
            color=ml_counts.index,
            color_discrete_map={
                'Suspected Buzzer': COLORS['high_suspicion'],
                'Normal User': COLORS['low_suspicion']
            }
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#333',
            legend=dict(font=dict(color='#333'))
        )
        st.plotly_chart(fig2)


def render_scatter_plot(user_activity: pd.DataFrame):
    """Render scatter plot posting rate vs text similarity."""
    st.markdown('<h3 style="color: #333;">🎯 Analisis Pola Buzzer</h3>', unsafe_allow_html=True)
    
    fig = px.scatter(
        user_activity,
        x='posting_rate',
        y='avg_text_similarity',
        color='buzzer_category',
        size='comment_count',
        hover_data=['author', 'duplicate_ratio', 'buzzer_score'],
        title="Posting Rate vs Text Similarity",
        color_discrete_map={
            'High Suspicion': COLORS['high_suspicion'],
            'Medium Suspicion': COLORS['medium_suspicion'],
            'Low Suspicion': COLORS['low_suspicion']
        }
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#333',
        xaxis_title="Posting Rate (komentar/jam)",
        yaxis_title="Avg Text Similarity",
        legend=dict(font=dict(color='#333')),
        xaxis=dict(
            tickfont=dict(color='#333'),
            title=dict(font=dict(color='#333')),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            tickfont=dict(color='#333'),
            title=dict(font=dict(color='#333')),
            gridcolor='rgba(0,0,0,0.1)'
        )
    )
    st.plotly_chart(fig)


def render_top_buzzers(user_activity: pd.DataFrame):
    """Render tabel top suspected buzzers."""
    # Container dengan padding horizontal - Light Mode
    st.markdown("""
    <div style="padding: 0 1rem;">
        <h3 style="color: #333;">🚨 Top Suspected Buzzers</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Wrapper dengan padding
    st.markdown('<div style="padding: 0 1rem;">', unsafe_allow_html=True)
    
    tabs = st.tabs(["Rule-Based", "Machine Learning", "High Confidence"])
    
    with tabs[0]:
        top_rule = user_activity.nlargest(20, 'buzzer_score')[[
            'author', 'comment_count', 'posting_rate', 
            'avg_text_similarity', 'duplicate_ratio', 
            'buzzer_score', 'buzzer_category'
        ]]
        st.dataframe(
            top_rule.style.background_gradient(
                subset=['buzzer_score'],
                cmap='Reds'
            ),
            hide_index=True
        )
    
    with tabs[1]:
        ml_buzzers = user_activity[
            user_activity['ml_buzzer_label'] == 'Suspected Buzzer'
        ].nsmallest(20, 'isolation_forest_score')[[
            'author', 'comment_count', 'posting_rate',
            'avg_text_similarity', 'duplicate_ratio',
            'isolation_forest_score', 'ml_buzzer_label'
        ]]
        st.dataframe(
            ml_buzzers.style.background_gradient(
                subset=['isolation_forest_score'],
                cmap='Reds_r'
            ),
            hide_index=True
        )
    
    with tabs[2]:
        high_conf = user_activity[
            (user_activity['buzzer_category'] == 'High Suspicion') &
            (user_activity['ml_buzzer_label'] == 'Suspected Buzzer')
        ][[
            'author', 'comment_count', 'posting_rate',
            'avg_text_similarity', 'duplicate_ratio',
            'buzzer_score', 'isolation_forest_score'
        ]]
        
        if len(high_conf) > 0:
            st.dataframe(
                high_conf.style.background_gradient(
                    subset=['buzzer_score'],
                    cmap='Reds'
                ),
                hide_index=True
            )
        else:
            st.info("Tidak ada user dengan High Confidence")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_conclusion(user_activity: pd.DataFrame, summary: dict):
    """Render kesimpulan hasil deteksi."""
    st.markdown('<h3 style="color: #333;">📝 Kesimpulan</h3>', unsafe_allow_html=True)
    
    total = summary['total_users']
    
    # Hitung persentase
    ml_suspected = summary['ml_suspected']
    ml_normal = summary['ml_normal']
    high_conf = summary['high_confidence']
    
    pct_suspected = (ml_suspected / total * 100) if total > 0 else 0
    pct_normal = (ml_normal / total * 100) if total > 0 else 0
    pct_high_conf = (high_conf / total * 100) if total > 0 else 0
    
    # Main conclusion box - Light Mode
    st.markdown(f"""
<div style="background: #ffffff; border: 1px solid #e0e0e0; border-radius: 20px; padding: 2rem; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
<h2 style="text-align: center; color: #667eea; margin-bottom: 1.5rem;">📊 Hasil Analisis</h2>
<div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
<div style="background: linear-gradient(135deg, #FF4B4B, #FF6B6B); border-radius: 15px; padding: 1.5rem 2rem; text-align: center; min-width: 200px; box-shadow: 0 4px 15px rgba(255,75,75,0.3);">
<h1 style="color: white; margin: 0; font-size: 2.5rem;">{pct_suspected:.1f}%</h1>
<p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-weight: bold;">Suspected Buzzer</p>
<p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.85rem;">({ml_suspected:,} dari {total:,} users)</p>
</div>
<div style="background: linear-gradient(135deg, #00CC96, #00E5AA); border-radius: 15px; padding: 1.5rem 2rem; text-align: center; min-width: 200px; box-shadow: 0 4px 15px rgba(0,204,150,0.3);">
<h1 style="color: white; margin: 0; font-size: 2.5rem;">{pct_normal:.1f}%</h1>
<p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-weight: bold;">Normal User</p>
<p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.85rem;">({ml_normal:,} dari {total:,} users)</p>
</div>
</div>
<div style="background: rgba(255, 75, 75, 0.1); border: 1px solid #FF4B4B; border-radius: 10px; padding: 1rem; margin-top: 1.5rem; text-align: center;">
<p style="color: #e53935; margin: 0; font-size: 1.1rem;">🚨 <b>High Confidence Buzzer:</b> {high_conf} users ({pct_high_conf:.1f}%)</p>
<p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.85rem;">Terdeteksi oleh kedua metode (Rule-Based & Machine Learning)</p>
</div>
</div>
    """, unsafe_allow_html=True)
    
    # Interpretasi - Light Mode
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
<div style="background: #ffffff; border-radius: 15px; padding: 1.5rem; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<h4 style="color: #667eea; margin: 0 0 1rem 0;">💡 Interpretasi</h4>
<ul style="color: #444; margin: 0; padding-left: 1.2rem; line-height: 1.8;">
<li>Buzzer menunjukkan pola posting tidak natural</li>
<li>Copy-paste konten adalah indikator kuat</li>
<li>Kombinasi kedua metode meningkatkan akurasi</li>
<li>Validasi manual tetap diperlukan</li>
</ul>
</div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
<div style="background: #ffffff; border-radius: 15px; padding: 1.5rem; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<h4 style="color: #00CC96; margin: 0 0 1rem 0;">✅ Rekomendasi</h4>
<ul style="color: #444; margin: 0; padding-left: 1.2rem; line-height: 1.8;">
<li>Review manual High Confidence Buzzers</li>
<li>Analisis temporal pattern lebih detail</li>
<li>Validasi dengan ground truth jika ada</li>
<li>Monitoring berkelanjutan</li>
</ul>
</div>
        """, unsafe_allow_html=True)


def render_download_button(user_activity: pd.DataFrame):
    """Render tombol download hasil."""
    st.markdown('<h3 style="color: #333;">💾 Export Hasil</h3>', unsafe_allow_html=True)
    
    export_cols = [
        'author', 'comment_count', 'posting_rate',
        'avg_text_similarity', 'duplicate_ratio',
        'buzzer_score', 'buzzer_category',
        'isolation_forest_score', 'ml_buzzer_label'
    ]
    
    csv = user_activity[export_cols].to_csv(index=False)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="buzzer_detection_results.csv",
            mime="text/csv",
            use_container_width=True
        )


def render_results(user_activity: pd.DataFrame, summary: dict):
    """
    Render semua komponen hasil deteksi.
    
    Args:
        user_activity: DataFrame hasil deteksi
        summary: Dictionary ringkasan
    """
    # Kesimpulan di paling atas
    render_conclusion(user_activity, summary)
    st.markdown("---")
    render_summary_cards(summary)
    st.markdown("---")
    render_distribution_chart(user_activity)
    st.markdown("---")
    render_scatter_plot(user_activity)
    st.markdown("---")
    render_top_buzzers(user_activity)
    st.markdown("---")
    render_download_button(user_activity)
