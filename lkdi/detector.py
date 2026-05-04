"""
RevivalDetector: Main class for detecting Revival Impact Factor (RIF) in scientific literature.
"""

import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from lkdi.graph_builder import CitationGraphBuilder
from lkdi.metrics import calculate_rif, detect_dormancy


@dataclass
class RevivalResult:
    """Container for revival analysis results."""
    paper_id: str
    rif_score: float
    dormant_period: tuple
    key_concepts: List[str]
    citation_timeline: Dict[int, int]
    revival_year: Optional[int]
    spike_magnitude: float


class RevivalDetector:
    """
    Detects revival patterns in scientific literature.
    
    This class analyzes citation patterns to identify papers that experienced
    a period of dormancy followed by a resurgence of attention.
    """
    
    def __init__(self, data_source: str = "openalex", api_key: Optional[str] = None):
        """
        Initialize the RevivalDetector.
        
        Args:
            data_source: Source for bibliographic data ("openalex", "semantic_scholar", "local")
            api_key: API key for the data source (optional for OpenAlex)
        """
        self.data_source = data_source
        self.api_key = api_key
        self.graph_builder = CitationGraphBuilder()
        self.cache: Dict[str, dict] = {}
        
        # API endpoints
        self.openalex_base_url = "https://api.openalex.org/works"
    
    def fetch_paper_data(self, doi: str) -> Optional[dict]:
        """
        Fetch paper data from the configured data source.
        
        Args:
            doi: Digital Object Identifier of the paper
        
        Returns:
            Dictionary with paper metadata or None if not found
        """
        if doi in self.cache:
            return self.cache[doi]
        
        if self.data_source == "openalex":
            return self._fetch_from_openalex(doi)
        elif self.data_source == "semantic_scholar":
            return self._fetch_from_semantic_scholar(doi)
        else:
            raise ValueError(f"Unsupported data source: {self.data_source}")
    
    def _fetch_from_openalex(self, doi: str) -> Optional[dict]:
        """Fetch paper data from OpenAlex API."""
        url = f"{self.openalex_base_url}/https://doi.org/{doi}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                paper_data = {
                    'id': data.get('id', ''),
                    'doi': data.get('doi', ''),
                    'title': data.get('title', ''),
                    'year': data.get('publication_year'),
                    'authors': [
                        author.get('author', {}).get('display_name', '')
                        for author in data.get('authorships', [])
                    ],
                    'citations_count': data.get('cited_by_count', 0),
                    'concepts': [
                        concept.get('display_name', '')
                        for concept in data.get('concepts', [])
                    ],
                    'raw_data': data
                }
                
                self.cache[doi] = paper_data
                return paper_data
        
        except (requests.RequestException, Exception) as e:
            print(f"Error fetching from OpenAlex: {e}")
            return None
        
        return None
    
    def _fetch_from_semantic_scholar(self, doi: str) -> Optional[dict]:
        """Fetch paper data from Semantic Scholar API."""
        url = f"https://api.semanticscholar.org/v1/paper/DOI:{doi}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                paper_data = {
                    'id': data.get('paperId', ''),
                    'doi': data.get('doi', ''),
                    'title': data.get('title', ''),
                    'year': data.get('year'),
                    'authors': data.get('authors', []),
                    'citations_count': data.get('numCitingPapers', 0),
                    'raw_data': data
                }
                
                self.cache[doi] = paper_data
                return paper_data
        
        except requests.RequestException as e:
            print(f"Error fetching from Semantic Scholar: {e}")
            return None
        
        return None
    
    def fetch_citations(self, doi: str, limit: int = 1000) -> List[dict]:
        """
        Fetch papers that cite the given paper.
        
        Args:
            doi: DOI of the paper to get citations for
            limit: Maximum number of citing papers to fetch
        
        Returns:
            List of citing paper dictionaries
        """
        if self.data_source == "openalex":
            return self._fetch_citations_openalex(doi, limit)
        else:
            return []
    
    def _fetch_citations_openalex(self, doi: str, limit: int) -> List[dict]:
        """Fetch citations from OpenAlex."""
        url = f"{self.openalex_base_url}"
        params = {
            'filter': f'cites:{self.openalex_base_url}/https://doi.org/{doi}',
            'per_page': min(limit, 200),
            'select': 'id,doi,title,publication_year,authorships'
        }
        
        citations = []
        
        try:
            while len(citations) < limit:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                results = data.get('results', [])
                if not results:
                    break
                
                for work in results:
                    citations.append({
                        'id': work.get('id', ''),
                        'doi': work.get('doi', ''),
                        'title': work.get('title', ''),
                        'year': work.get('publication_year'),
                        'authors': [
                            author.get('author', {}).get('display_name', '')
                            for author in work.get('authorships', [])
                        ]
                    })
                
                # Pagination
                next_page = data.get('meta', {}).get('next_cursor')
                if not next_page:
                    break
                params['cursor'] = next_page
        
        except requests.RequestException as e:
            print(f"Error fetching citations: {e}")
        
        return citations[:limit]
    
    def analyze(self, doi: str) -> RevivalResult:
        """
        Analyze a paper for revival patterns.
        
        Args:
            doi: DOI of the paper to analyze
        
        Returns:
            RevivalResult with RIF score and related metrics
        """
        # Fetch paper data
        paper_data = self.fetch_paper_data(doi)
        if not paper_data:
            return RevivalResult(
                paper_id=doi,
                rif_score=0.0,
                dormant_period=(None, None),
                key_concepts=[],
                citation_timeline={},
                revival_year=None,
                spike_magnitude=0.0
            )
        
        # Fetch citing papers
        citations = self.fetch_citations(doi)
        
        # Build citation timeline
        citation_timeline: Dict[int, int] = {}
        for citation in citations:
            year = citation.get('year')
            if year:
                citation_timeline[year] = citation_timeline.get(year, 0) + 1
        
        # Add years with zero citations for gap detection
        if citation_timeline:
            min_year = min(citation_timeline.keys())
            max_year = max(citation_timeline.keys())
            for year in range(min_year, max_year + 1):
                if year not in citation_timeline:
                    citation_timeline[year] = 0
        
        # Detect dormancy
        dormant_period = detect_dormancy(citation_timeline)
        
        # Calculate RIF
        rif_score = calculate_rif(citation_timeline, dormant_period)
        
        # Find revival year (first year after dormancy with significant citations)
        revival_year = None
        if dormant_period[1] is not None:
            post_dormancy_years = [
                y for y in sorted(citation_timeline.keys())
                if y > dormant_period[1] and citation_timeline[y] > 0
            ]
            if post_dormancy_years:
                revival_year = post_dormancy_years[0]
        
        # Calculate spike magnitude
        spike_magnitude = 0.0
        if dormant_period[1] and revival_year:
            pre_dormancy_avg = sum(
                citation_timeline.get(y, 0)
                for y in range(min(citation_timeline.keys()), dormant_period[0])
            ) / max(1, dormant_period[0] - min(citation_timeline.keys()))
            
            post_dormancy_max = max(
                citation_timeline.get(y, 0)
                for y in citation_timeline.keys()
                if y > dormant_period[1]
            )
            
            if pre_dormancy_avg > 0:
                spike_magnitude = post_dormancy_max / pre_dormancy_avg
            else:
                spike_magnitude = float(post_dormancy_max)
        
        return RevivalResult(
            paper_id=doi,
            rif_score=rif_score,
            dormant_period=dormant_period,
            key_concepts=paper_data.get('concepts', []),
            citation_timeline=citation_timeline,
            revival_year=revival_year,
            spike_magnitude=spike_magnitude
        )
    
    def build_citation_graph(self, seed_dois: List[str], depth: int = 1) -> None:
        """
        Build a citation graph starting from seed papers.
        
        Args:
            seed_dois: List of DOIs to start from
            depth: How many citation hops to follow
        """
        papers_to_process = set(seed_dois)
        processed = set()
        
        while papers_to_process:
            doi = papers_to_process.pop()
            if doi in processed:
                continue
            
            paper_data = self.fetch_paper_data(doi)
            if paper_data:
                self.graph_builder.add_paper(
                    paper_id=doi,
                    title=paper_data.get('title', ''),
                    year=paper_data.get('year'),
                    authors=paper_data.get('authors', []),
                    field=', '.join(paper_data.get('concepts', [])[:3])
                )
                
                # Fetch references (papers this one cites)
                if depth > 0:
                    references = paper_data.get('raw_data', {}).get('referenced_works', [])
                    for ref in references[:10]:  # Limit references
                        ref_doi = ref.split('/')[-1] if '/' in ref else ref
                        if ref_doi not in processed:
                            papers_to_process.add(ref_doi)
                            self.graph_builder.add_citation(doi, ref_doi)
            
            processed.add(doi)
