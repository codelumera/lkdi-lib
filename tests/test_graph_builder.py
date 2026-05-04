"""
Tests for L-KDI graph builder module.
"""

import pytest
from lkdi.graph_builder import CitationGraphBuilder


class TestCitationGraphBuilder:
    """Tests for the CitationGraphBuilder class."""
    
    def test_add_paper(self):
        """Test adding a paper to the graph."""
        builder = CitationGraphBuilder()
        builder.add_paper(
            paper_id="10.1234/test",
            title="Test Paper",
            year=2020,
            authors=["Author A", "Author B"],
            field="AI"
        )
        
        assert "10.1234/test" in builder.graph.nodes()
        node_data = builder.graph.nodes["10.1234/test"]
        assert node_data['title'] == "Test Paper"
        assert node_data['year'] == 2020
    
    def test_add_citation(self):
        """Test adding a citation edge."""
        builder = CitationGraphBuilder()
        builder.add_paper(paper_id="paper1", year=2020)
        builder.add_paper(paper_id="paper2", year=2019)
        
        builder.add_citation("paper1", "paper2")
        
        assert builder.graph.has_edge("paper1", "paper2")
    
    def test_add_citation_missing_paper(self):
        """Test adding citation with missing paper raises error."""
        builder = CitationGraphBuilder()
        builder.add_paper(paper_id="paper1", year=2020)
        
        with pytest.raises(ValueError):
            builder.add_citation("paper1", "missing_paper")
    
    def test_build_from_papers(self):
        """Test building graph from list of papers."""
        builder = CitationGraphBuilder()
        
        papers = [
            {
                'id': 'paper1',
                'title': 'Paper 1',
                'year': 2020,
                'citations': ['paper2']
            },
            {
                'id': 'paper2',
                'title': 'Paper 2',
                'year': 2019,
                'citations': []
            }
        ]
        
        graph = builder.build_from_papers(papers)
        
        assert len(graph.nodes()) == 2
        assert graph.has_edge('paper1', 'paper2')
    
    def test_get_citation_timeline(self):
        """Test getting citation timeline for a paper."""
        builder = CitationGraphBuilder()
        
        # Add cited paper
        builder.add_paper(paper_id="cited", year=2010)
        
        # Add citing papers
        builder.add_paper(paper_id="citer1", year=2015)
        builder.add_paper(paper_id="citer2", year=2015)
        builder.add_paper(paper_id="citer3", year=2016)
        
        # Add citations
        builder.add_citation("citer1", "cited")
        builder.add_citation("citer2", "cited")
        builder.add_citation("citer3", "cited")
        
        timeline = builder.get_citation_timeline("cited")
        
        assert timeline[2015] == 2
        assert timeline[2016] == 1
    
    def test_get_subgraph_by_year_range(self):
        """Test extracting subgraph by year range."""
        builder = CitationGraphBuilder()
        
        builder.add_paper(paper_id="p2018", year=2018)
        builder.add_paper(paper_id="p2019", year=2019)
        builder.add_paper(paper_id="p2020", year=2020)
        builder.add_paper(paper_id="p2021", year=2021)
        
        subgraph = builder.get_subgraph_by_year_range(2019, 2020)
        
        assert len(subgraph.nodes()) == 2
        assert "p2019" in subgraph.nodes()
        assert "p2020" in subgraph.nodes()
        assert "p2018" not in subgraph.nodes()
        assert "p2021" not in subgraph.nodes()
    
    def test_calculate_centrality_metrics(self):
        """Test calculating centrality metrics."""
        builder = CitationGraphBuilder()
        
        # Create a simple citation network
        builder.add_paper(paper_id="p1", year=2020)
        builder.add_paper(paper_id="p2", year=2019)
        builder.add_paper(paper_id="p3", year=2018)
        
        builder.add_citation("p2", "p1")
        builder.add_citation("p3", "p1")
        builder.add_citation("p3", "p2")
        
        metrics = builder.calculate_centrality_metrics()
        
        assert len(metrics) == 3
        assert "degree_centrality" in metrics["p1"]
        assert "pagerank" in metrics["p1"]
        assert "betweenness_centrality" in metrics["p1"]


class TestTemporalWeighting:
    """Tests for temporal weighting in citations."""
    
    def test_temporal_weight_calculation(self):
        """Test that temporal weights are calculated correctly."""
        builder = CitationGraphBuilder()
        
        builder.add_paper(paper_id="old", year=2000)
        builder.add_paper(paper_id="new", year=2020)
        
        builder.add_citation("new", "old")
        
        edge_data = builder.graph.edges["new", "old"]
        assert "weight" in edge_data
        assert edge_data["time_diff"] == 20
    
    def test_custom_weight(self):
        """Test adding citation with custom weight."""
        builder = CitationGraphBuilder()
        
        builder.add_paper(paper_id="p1", year=2020)
        builder.add_paper(paper_id="p2", year=2019)
        
        builder.add_citation("p1", "p2", weight=0.5)
        
        edge_data = builder.graph.edges["p1", "p2"]
        assert edge_data["weight"] == 0.5
