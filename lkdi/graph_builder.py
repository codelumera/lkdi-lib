"""
Citation graph builder for constructing temporal citation networks.
"""

import networkx as nx
from typing import Dict, List, Optional, Any
from datetime import datetime


class CitationGraphBuilder:
    """
    Builder for creating temporal citation graphs from bibliographic data.
    
    The graph includes:
    - Nodes: Papers with metadata (year, title, authors, field)
    - Edges: Citations with temporal weights
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.paper_cache: Dict[str, dict] = {}
    
    def add_paper(
        self,
        paper_id: str,
        title: str = "",
        year: int = None,
        authors: List[str] = None,
        field: str = "",
        **kwargs
    ) -> None:
        """
        Add a paper node to the graph.
        
        Args:
            paper_id: Unique identifier (DOI, arXiv ID, etc.)
            title: Paper title
            year: Publication year
            authors: List of author names
            field: Research field/category
            **kwargs: Additional metadata
        """
        node_data = {
            'paper_id': paper_id,
            'title': title,
            'year': year,
            'authors': authors or [],
            'field': field,
            **kwargs
        }
        
        self.graph.add_node(paper_id, **node_data)
        self.paper_cache[paper_id] = node_data
    
    def add_citation(
        self,
        citing_paper_id: str,
        cited_paper_id: str,
        weight: float = 1.0
    ) -> None:
        """
        Add a citation edge between two papers.
        
        Args:
            citing_paper_id: ID of the paper that cites
            cited_paper_id: ID of the paper being cited
            weight: Edge weight (can be based on time difference, context similarity, etc.)
        """
        if citing_paper_id not in self.graph:
            raise ValueError(f"Citing paper {citing_paper_id} not in graph")
        if cited_paper_id not in self.graph:
            raise ValueError(f"Cited paper {cited_paper_id} not in graph")
        
        # Get years for time difference calculation
        citing_year = self.graph.nodes[citing_paper_id].get('year')
        cited_year = self.graph.nodes[cited_paper_id].get('year')
        
        # Calculate temporal weight if not provided
        if weight == 1.0:
            if citing_year and cited_year:
                time_diff = citing_year - cited_year
                # More recent citations get higher weight
                weight = 1.0 / (1.0 + time_diff * 0.1)
        
        # Calculate time difference for storage
        time_diff = citing_year - cited_year if citing_year and cited_year else None
        
        self.graph.add_edge(
            citing_paper_id,
            cited_paper_id,
            weight=weight,
            time_diff=time_diff
        )
    
    def build_from_papers(self, papers: List[dict]) -> nx.DiGraph:
        """
        Build graph from a list of paper dictionaries.
        
        Each paper dict should have:
        - id: Paper identifier
        - title, year, authors, field (optional)
        - citations: List of paper IDs this paper cites
        
        Args:
            papers: List of paper dictionaries
        
        Returns:
            NetworkX DiGraph
        """
        # First pass: add all papers
        for paper in papers:
            self.add_paper(
                paper_id=paper.get('id', paper.get('doi', '')),
                title=paper.get('title', ''),
                year=paper.get('year'),
                authors=paper.get('authors', []),
                field=paper.get('field', ''),
                **{k: v for k, v in paper.items() 
                   if k not in ['id', 'doi', 'title', 'year', 'authors', 'field', 'citations']}
            )
        
        # Second pass: add citation edges
        for paper in papers:
            paper_id = paper.get('id', paper.get('doi', ''))
            citations = paper.get('citations', [])
            
            for cited_id in citations:
                if cited_id in self.graph:
                    self.add_citation(paper_id, cited_id)
        
        return self.graph
    
    def get_subgraph_by_year_range(
        self,
        start_year: int,
        end_year: int
    ) -> nx.DiGraph:
        """
        Extract subgraph for a specific year range.
        
        Args:
            start_year: Start year (inclusive)
            end_year: End year (inclusive)
        
        Returns:
            Subgraph containing only papers in the year range
        """
        nodes_in_range = [
            node for node, data in self.graph.nodes(data=True)
            if data.get('year') and start_year <= data['year'] <= end_year
        ]
        
        return self.graph.subgraph(nodes_in_range).copy()
    
    def get_citation_timeline(self, paper_id: str) -> Dict[int, int]:
        """
        Get citation timeline for a specific paper.
        
        Args:
            paper_id: ID of the paper to analyze
        
        Returns:
            Dictionary mapping year to citation count
        """
        if paper_id not in self.graph:
            return {}
        
        # Get all papers that cite this one
        citing_papers = self.graph.predecessors(paper_id)
        
        timeline: Dict[int, int] = {}
        for citer_id in citing_papers:
            year = self.graph.nodes[citer_id].get('year')
            if year:
                timeline[year] = timeline.get(year, 0) + 1
        
        return timeline
    
    def calculate_centrality_metrics(self) -> Dict[str, dict]:
        """
        Calculate various centrality metrics for all nodes.
        
        Returns:
            Dictionary mapping paper_id to centrality scores
        """
        metrics = {}
        
        # Degree centrality
        degree_cent = nx.degree_centrality(self.graph)
        
        # PageRank (important for citation networks)
        pagerank = nx.pagerank(self.graph, max_iter=100)
        
        # Betweenness centrality (computationally expensive for large graphs)
        try:
            betweenness = nx.betweenness_centrality(self.graph, sample=100)
        except:
            betweenness = {}
        
        for node in self.graph.nodes():
            metrics[node] = {
                'degree_centrality': degree_cent.get(node, 0),
                'pagerank': pagerank.get(node, 0),
                'betweenness_centrality': betweenness.get(node, 0)
            }
        
        return metrics
