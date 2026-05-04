"""
Tests for L-KDI metrics module.
"""

import pytest
from lkdi.metrics import detect_dormancy, calculate_rif, diffusion_distance, breakthrough_score


class TestDetectDormancy:
    """Tests for the detect_dormancy function."""
    
    def test_no_dormancy_short_timeline(self):
        """Test that short timelines don't trigger dormancy."""
        timeline = {2020: 10, 2021: 15, 2022: 12, 2023: 20}
        result = detect_dormancy(timeline, min_dormancy_years=10)
        assert result == (None, None)
    
    def test_dormancy_detected(self):
        """Test dormancy detection with clear dormant period."""
        timeline = {
            1980: 50, 1981: 45,  # Active period
            1982: 2, 1983: 1, 1984: 0, 1985: 1, 1986: 0,  # Start of dormancy
            1987: 1, 1988: 0, 1989: 2, 1990: 1, 1991: 0,  # Dormancy continues
            1992: 30, 1993: 50, 1994: 80  # Revival
        }
        result = detect_dormancy(timeline, min_dormancy_years=10, threshold=0.1)
        assert result[0] is not None
        assert result[1] is not None
    
    def test_empty_timeline(self):
        """Test with empty timeline."""
        result = detect_dormancy({})
        assert result == (None, None)
    
    def test_zero_citations(self):
        """Test with all zero citations."""
        timeline = {2020: 0, 2021: 0, 2022: 0}
        result = detect_dormancy(timeline)
        assert result == (None, None)


class TestCalculateRIF:
    """Tests for the calculate_rif function."""
    
    def test_no_dormancy_zero_rif(self):
        """Test that no dormancy results in zero RIF."""
        timeline = {2020: 10, 2021: 15, 2022: 20}
        rif = calculate_rif(timeline, (None, None))
        assert rif == 0.0
    
    def test_revival_detected(self):
        """Test RIF calculation with revival pattern."""
        timeline = {
            1980: 50, 1981: 45,
            1982: 1, 1983: 0, 1984: 1, 1985: 0, 1986: 1,
            1987: 0, 1988: 1, 1989: 0, 1990: 1, 1991: 0,
            1992: 100, 1993: 150, 1994: 200
        }
        dormant_period = (1982, 1991)
        rif = calculate_rif(timeline, dormant_period)
        assert rif > 0.0
    
    def test_empty_timeline_rif(self):
        """Test RIF with empty timeline."""
        rif = calculate_rif({}, (None, None))
        assert rif == 0.0


class TestDiffusionDistance:
    """Tests for the diffusion_distance function."""
    
    def test_nodes_not_in_graph(self):
        """Test distance when nodes are not in graph."""
        import networkx as nx
        graph = nx.DiGraph()
        graph.add_node('A')
        
        distance = diffusion_distance(graph, 'A', 'B')
        assert distance == float('inf')
    
    def test_same_node_distance(self):
        """Test distance from node to itself."""
        import networkx as nx
        graph = nx.DiGraph()
        graph.add_node('A')
        
        distance = diffusion_distance(graph, 'A', 'A')
        assert distance == 0


class TestBreakthroughScore:
    """Tests for the breakthrough_score function."""
    
    def test_single_field(self):
        """Test breakthrough score with single field."""
        citations = [{'field': 'AI'}, {'field': 'AI'}, {'field': 'AI'}]
        field_boundaries = {'AI': {'ml', 'dl'}, 'Physics': {'quantum', 'relativity'}}
        
        score = breakthrough_score(citations, field_boundaries)
        assert 0.0 <= score <= 1.0
    
    def test_multiple_fields(self):
        """Test breakthrough score with multiple fields."""
        citations = [
            {'field': 'AI'},
            {'field': 'Physics'},
            {'field': 'Biology'}
        ]
        field_boundaries = {
            'AI': {'ml', 'dl'},
            'Physics': {'quantum', 'relativity'},
            'Biology': {'genetics', 'ecology'}
        }
        
        score = breakthrough_score(citations, field_boundaries)
        assert score == 1.0  # All fields represented
    
    def test_empty_citations(self):
        """Test breakthrough score with no citations."""
        score = breakthrough_score([], {})
        assert score == 0.0


class TestIntegration:
    """Integration tests for metrics working together."""
    
    def test_full_revival_analysis(self):
        """Test complete revival analysis workflow."""
        # Create a realistic citation timeline with dormancy and revival
        timeline = {}
        
        # Initial interest (1970s)
        for year in range(1970, 1975):
            timeline[year] = 30 + (year - 1970) * 5
        
        # Dormancy period (1975-1995)
        for year in range(1975, 1995):
            timeline[year] = 1 if year % 3 == 0 else 0
        
        # Revival (1995-2010)
        for year in range(1995, 2010):
            timeline[year] = 20 + (year - 1995) * 10
        
        # Detect dormancy
        dormant_period = detect_dormancy(timeline, min_dormancy_years=10)
        
        # Should detect dormancy
        assert dormant_period[0] is not None
        assert dormant_period[1] is not None
        
        # Calculate RIF
        rif = calculate_rif(timeline, dormant_period)
        
        # Should have positive RIF due to revival
        assert rif > 0.0
