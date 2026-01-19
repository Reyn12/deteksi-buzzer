"""
Komponen UI untuk menampilkan hasil deteksi
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
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
        styled_df = top_rule.style.background_gradient(
            subset=['buzzer_score'],
            cmap='Reds'
        ).set_properties(**{'color': '#333', 'background-color': '#fff'})
        st.dataframe(styled_df, hide_index=True)
    
    with tabs[1]:
        ml_buzzers = user_activity[
            user_activity['ml_buzzer_label'] == 'Suspected Buzzer'
        ].nsmallest(20, 'isolation_forest_score')[[
            'author', 'comment_count', 'posting_rate',
            'avg_text_similarity', 'duplicate_ratio',
            'isolation_forest_score', 'ml_buzzer_label'
        ]]
        styled_ml = ml_buzzers.style.background_gradient(
            subset=['isolation_forest_score'],
            cmap='Reds_r'
        ).set_properties(**{'color': '#333', 'background-color': '#fff'})
        st.dataframe(styled_ml, hide_index=True)
    
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
            styled_high = high_conf.style.background_gradient(
                subset=['buzzer_score'],
                cmap='Reds'
            ).set_properties(**{'color': '#333', 'background-color': '#fff'})
            st.dataframe(styled_high, hide_index=True)
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


def render_network_graph(user_activity: pd.DataFrame, graph: nx.Graph):
    """Render visualisasi Social Network Analysis."""
    st.markdown('<h3 style="color: #333;">🕸️ Social Network Analysis</h3>', unsafe_allow_html=True)
    
    if graph is None or graph.number_of_nodes() == 0:
        st.info("Network graph tidak tersedia.")
        return
    
    # Limit nodes untuk performa (max 100 nodes)
    max_nodes = 100
    if graph.number_of_nodes() > max_nodes:
        # Ambil nodes dengan degree tertinggi
        degrees = dict(graph.degree())
        top_nodes = sorted(degrees.keys(), key=lambda x: degrees[x], reverse=True)[:max_nodes]
        graph = graph.subgraph(top_nodes).copy()
        st.caption(f"⚠️ Menampilkan {max_nodes} nodes dengan koneksi tertinggi (dari {len(degrees)} total)")
    
    # Get positions using spring layout
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node traces
    node_x = []
    node_y = []
    node_colors = []
    node_sizes = []
    node_text = []
    
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Get user data
        if node in user_activity['author'].values:
            user_data = user_activity[user_activity['author'] == node].iloc[0]
            category = user_data['buzzer_category']
            ml_label = user_data['ml_buzzer_label']
            score = user_data['buzzer_score']
            
            # Color based on category
            if category == 'High Suspicion':
                node_colors.append('#FF4B4B')
                node_sizes.append(20)
            elif category == 'Medium Suspicion':
                node_colors.append('#FFA500')
                node_sizes.append(15)
            else:
                node_colors.append('#00CC96')
                node_sizes.append(10)
            
            node_text.append(
                f"<b>{node}</b><br>"
                f"Category: {category}<br>"
                f"ML: {ml_label}<br>"
                f"Score: {score}"
            )
        else:
            node_colors.append('#888')
            node_sizes.append(8)
            node_text.append(node)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            color=node_colors,
            size=node_sizes,
            line=dict(width=1, color='white')
        )
    )
    
    # Create tabs for different views
    tabs = st.tabs(["Rule-Based View", "Machine Learning View"])
    
    with tabs[0]:
        # Rule-based view
        fig1 = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=dict(
                                text='Network Buzzer Detection (Rule-Based)',
                                font=dict(color='#333', size=16)
                            ),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=20, r=20, t=50),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            annotations=[
                                dict(
                                    text="🔴 High Suspicion | 🟠 Medium | 🟢 Low",
                                    showarrow=False,
                                    xref="paper", yref="paper",
                                    x=0.5, y=-0.05,
                                    font=dict(size=12, color='#666')
                                )
                            ]
                        ))
        st.plotly_chart(fig1, use_container_width=True)
    
    with tabs[1]:
        # ML view - recolor nodes
        ml_colors = []
        ml_sizes = []
        ml_text = []
        
        for node in graph.nodes():
            if node in user_activity['author'].values:
                user_data = user_activity[user_activity['author'] == node].iloc[0]
                ml_label = user_data['ml_buzzer_label']
                score = user_data['isolation_forest_score']
                
                if ml_label == 'Suspected Buzzer':
                    ml_colors.append('#9C27B0')  # Purple
                    ml_sizes.append(20)
                else:
                    ml_colors.append('#00CC96')  # Green
                    ml_sizes.append(10)
                
                ml_text.append(
                    f"<b>{node}</b><br>"
                    f"ML Label: {ml_label}<br>"
                    f"IF Score: {score:.4f}"
                )
            else:
                ml_colors.append('#888')
                ml_sizes.append(8)
                ml_text.append(node)
        
        ml_node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=ml_text,
            marker=dict(
                color=ml_colors,
                size=ml_sizes,
                line=dict(width=1, color='white')
            )
        )
        
        fig2 = go.Figure(data=[edge_trace, ml_node_trace],
                        layout=go.Layout(
                            title=dict(
                                text='Network Buzzer Detection (Machine Learning)',
                                font=dict(color='#333', size=16)
                            ),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=20, r=20, t=50),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            annotations=[
                                dict(
                                    text="🟣 Suspected Buzzer | 🟢 Normal User",
                                    showarrow=False,
                                    xref="paper", yref="paper",
                                    x=0.5, y=-0.05,
                                    font=dict(size=12, color='#666')
                                )
                            ]
                        ))
        st.plotly_chart(fig2, use_container_width=True)
    
    # Network stats
    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 10px; padding: 1rem; margin-top: 1rem;">
        <p style="color: #666; margin: 0; text-align: center;">
            <b>Cara Baca:</b> Node yang lebih besar dan berwarna merah/ungu adalah suspected buzzer. 
            Garis menghubungkan user dengan komentar serupa (text similarity > 0.3).
        </p>
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
    
    # Network visualization
    graph = summary.get('graph', None)
    if graph is not None:
        render_network_graph(user_activity, graph)
        st.markdown("---")
    
    render_top_buzzers(user_activity)
    st.markdown("---")
    render_download_button(user_activity)
