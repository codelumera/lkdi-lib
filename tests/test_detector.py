"""
Tests for L-KDI detector module.
"""

import pytest
from unittest.mock import Mock, patch
from lkdi.detector import RevivalDetector, RevivalResult


class TestRevivalDetector:
    """Tests for the RevivalDetector class."""
    
    def test_init_default(self):
        """Test default initialization."""
        detector = RevivalDetector()
        assert detector.data_source == "openalex"
        assert detector.api_key is None
    
    def test_init_custom(self):
        """Test custom initialization."""
        detector = RevivalDetector(data_source="semantic_scholar", api_key="test_key")
        assert detector.data_source == "semantic_scholar"
        assert detector.api_key == "test_key"
    
    def test_unsupported_data_source(self):
        """Test error on unsupported data source."""
        detector = RevivalDetector(data_source="unsupported")
        with pytest.raises(ValueError):
            detector.fetch_paper_data("10.1234/test")
    
    @patch('lkdi.detector.requests.get')
    def test_fetch_from_openalex_success(self, mock_get):
        """Test successful fetch from OpenAlex."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 'https://openalex.org/W1234',
            'doi': 'https://doi.org/10.1234/test',
            'title': 'Test Paper',
            'publication_year': 2020,
            'authorships': [
                {'author': {'display_name': 'Author A'}},
                {'author': {'display_name': 'Author B'}}
            ],
            'cited_by_count': 50,
            'concepts': [
                {'display_name': 'Machine Learning'},
                {'display_name': 'AI'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        detector = RevivalDetector()
        result = detector.fetch_paper_data("10.1234/test")
        
        assert result is not None
        assert result['title'] == 'Test Paper'
        assert result['year'] == 2020
        assert len(result['authors']) == 2
    
    @patch('lkdi.detector.requests.get')
    def test_fetch_from_openalex_error(self, mock_get):
        """Test fetch error from OpenAlex."""
        mock_get.side_effect = Exception("Connection error")
        
        detector = RevivalDetector()
        result = detector.fetch_paper_data("10.1234/test")
        
        assert result is None
    
    def test_cache_hit(self):
        """Test that cached data is returned."""
        detector = RevivalDetector()
        detector.cache["10.1234/test"] = {'title': 'Cached Paper'}
        
        result = detector.fetch_paper_data("10.1234/test")
        
        assert result['title'] == 'Cached Paper'
    
    def test_analyze_no_data(self):
        """Test analyze when no data is available."""
        detector = RevivalDetector()
        
        # Mock fetch_paper_data to return None
        detector.fetch_paper_data = Mock(return_value=None)
        
        result = detector.analyze("10.1234/test")
        
        assert isinstance(result, RevivalResult)
        assert result.rif_score == 0.0
        assert result.paper_id == "10.1234/test"


class TestRevivalResult:
    """Tests for the RevivalResult dataclass."""
    
    def test_create_result(self):
        """Test creating a RevivalResult."""
        result = RevivalResult(
            paper_id="10.1234/test",
            rif_score=15.5,
            dormant_period=(1980, 1995),
            key_concepts=["AI", "ML"],
            citation_timeline={2020: 10, 2021: 20},
            revival_year=2000,
            spike_magnitude=5.0
        )
        
        assert result.rif_score == 15.5
        assert result.dormant_period == (1980, 1995)
        assert result.revival_year == 2000
    
    def test_empty_result(self):
        """Test creating an empty result."""
        result = RevivalResult(
            paper_id="10.1234/test",
            rif_score=0.0,
            dormant_period=(None, None),
            key_concepts=[],
            citation_timeline={},
            revival_year=None,
            spike_magnitude=0.0
        )
        
        assert result.rif_score == 0.0
        assert result.dormant_period == (None, None)


class TestIntegration:
    """Integration tests for the detector module."""
    
    @patch('lkdi.detector.requests.get')
    def test_full_analysis_workflow(self, mock_get):
        """Test complete analysis workflow with mocked API."""
        # Mock paper data response
        paper_response = Mock()
        paper_response.json.return_value = {
            'id': 'https://openalex.org/W1234',
            'doi': 'https://doi.org/10.1234/backprop',
            'title': 'Learning representations by back-propagating errors',
            'publication_year': 1986,
            'authorships': [{'author': {'display_name': 'Rumelhart'}}],
            'cited_by_count': 50000,
            'concepts': [{'display_name': 'Neural Networks'}]
        }
        paper_response.raise_for_status = Mock()
        
        # Mock citations response
        citations_response = Mock()
        citations_response.json.return_value = {
            'results': [],
            'meta': {}
        }
        citations_response.raise_for_status = Mock()
        
        mock_get.side_effect = [paper_response, citations_response]
        
        detector = RevivalDetector()
        result = detector.analyze("10.1234/backprop")
        
        assert isinstance(result, RevivalResult)
        assert result.paper_id == "10.1234/backprop"
