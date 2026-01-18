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
    st.markdown("### 📊 Ringkasan Hasil")
    
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
            <h2 style="color: white; margin: 0;">{summary['high_suspicion']}</h2>
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
    st.markdown("### 📈 Distribusi Kategori")
    
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
            font_color='white'
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
            font_color='white'
        )
        st.plotly_chart(fig2)


def render_scatter_plot(user_activity: pd.DataFrame):
    """Render scatter plot posting rate vs text similarity."""
    st.markdown("### 🎯 Analisis Pola Buzzer")
    
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
        font_color='white',
        xaxis_title="Posting Rate (komentar/jam)",
        yaxis_title="Avg Text Similarity"
    )
    st.plotly_chart(fig)


def render_top_buzzers(user_activity: pd.DataFrame):
    """Render tabel top suspected buzzers."""
    # Container dengan padding horizontal
    st.markdown("""
    <div style="padding: 0 2rem;">
        <h3>🚨 Top Suspected Buzzers</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Wrapper dengan padding
    st.markdown('<div style="padding: 0 2rem;">', unsafe_allow_html=True)
    
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


def render_download_button(user_activity: pd.DataFrame):
    """Render tombol download hasil."""
    st.markdown("### 💾 Export Hasil")
    
    export_cols = [
        'author', 'comment_count', 'posting_rate',
        'avg_text_similarity', 'duplicate_ratio',
        'buzzer_score', 'buzzer_category',
        'isolation_forest_score', 'ml_buzzer_label'
    ]
    
    csv = user_activity[export_cols].to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="buzzer_detection_results.csv",
        mime="text/csv"
    )


def render_results(user_activity: pd.DataFrame, summary: dict):
    """
    Render semua komponen hasil deteksi.
    
    Args:
        user_activity: DataFrame hasil deteksi
        summary: Dictionary ringkasan
    """
    render_summary_cards(summary)
    st.markdown("---")
    render_distribution_chart(user_activity)
    st.markdown("---")
    render_scatter_plot(user_activity)
    st.markdown("---")
    render_top_buzzers(user_activity)
    st.markdown("---")
    render_download_button(user_activity)
