"""
Service untuk analisis Social Network Analysis (SNA)
"""
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity


class NetworkAnalyzer:
    """Handler untuk Social Network Analysis."""
    
    def __init__(self, data: pd.DataFrame, tfidf_matrix):
        self.data = data.copy()
        self.tfidf_matrix = tfidf_matrix
        self.graph = None
        self.degree_centrality = {}
    
    def build_similarity_network(self, threshold: float = 0.3) -> 'NetworkAnalyzer':
        """
        Bangun network berdasarkan text similarity.
        
        Args:
            threshold: Minimum similarity untuk membuat edge
            
        Returns:
            Self untuk method chaining
        """
        self.graph = nx.Graph()
        
        # Tambah nodes (authors)
        authors = self.data['authorDisplayName'].unique()
        self.graph.add_nodes_from(authors)
        
        # Hitung similarity matrix
        if self.tfidf_matrix is not None:
            sim_matrix = cosine_similarity(self.tfidf_matrix)
            
            # Tambah edges berdasarkan similarity
            for i in range(len(self.data)):
                for j in range(i + 1, len(self.data)):
                    if sim_matrix[i, j] > threshold:
                        author_i = self.data.iloc[i]['authorDisplayName']
                        author_j = self.data.iloc[j]['authorDisplayName']
                        
                        if author_i != author_j:
                            if self.graph.has_edge(author_i, author_j):
                                self.graph[author_i][author_j]['weight'] += sim_matrix[i, j]
                            else:
                                self.graph.add_edge(
                                    author_i, author_j,
                                    weight=sim_matrix[i, j]
                                )
        
        return self
    
    def calculate_centrality(self) -> 'NetworkAnalyzer':
        """
        Hitung degree centrality untuk setiap node.
        
        Returns:
            Self untuk method chaining
        """
        if self.graph is not None:
            self.degree_centrality = nx.degree_centrality(self.graph)
        return self
    
    def get_centrality_df(self) -> pd.DataFrame:
        """
        Mendapatkan degree centrality sebagai DataFrame.
        
        Returns:
            DataFrame dengan author dan degree_centrality
        """
        return pd.DataFrame(
            list(self.degree_centrality.items()),
            columns=['author', 'degree_centrality']
        )
    
    def analyze(self, threshold: float = 0.3) -> pd.DataFrame:
        """
        Jalankan analisis network lengkap.
        
        Args:
            threshold: Minimum similarity untuk edge
            
        Returns:
            DataFrame dengan degree centrality
        """
        return (self
                .build_similarity_network(threshold)
                .calculate_centrality()
                .get_centrality_df())
    
    def get_network_stats(self) -> dict:
        """
        Mendapatkan statistik network.
        
        Returns:
            Dictionary berisi statistik network
        """
        if self.graph is None:
            return {}
        
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph) if self.graph.number_of_nodes() > 1 else 0,
            'avg_degree': sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
            if self.graph.number_of_nodes() > 0 else 0
        }
