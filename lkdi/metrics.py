"""
Metrics for calculating Revival Impact Factor (RIF) and detecting dormancy periods.
"""

import numpy as np
from typing import Tuple, List, Optional


def detect_dormancy(
    citation_timeline: dict[int, int],
    min_dormancy_years: int = 10,
    threshold: float = 0.1
) -> Tuple[Optional[int], Optional[int]]:
    """
    Detect dormancy period in citation timeline.
    
    A dormancy period is defined as a span of at least `min_dormancy_years` 
    where annual citations remain below the threshold of peak citations.
    
    Args:
        citation_timeline: Dictionary mapping year to citation count
        min_dormancy_years: Minimum number of years for a dormancy period
        threshold: Fraction of peak citations considered as "low activity"
    
    Returns:
        Tuple of (dormant_start, dormant_end) or (None, None) if no dormancy found
    """
    if not citation_timeline:
        return None, None
    
    years = sorted(citation_timeline.keys())
    citations = [citation_timeline[y] for y in years]
    peak_citations = max(citations)
    
    if peak_citations == 0:
        return None, None
    
    low_activity_threshold = peak_citations * threshold
    
    # Find periods of low activity
    dormancy_candidates = []
    in_dormancy = False
    dormancy_start = None
    
    for i, year in enumerate(years):
        cit_count = citation_timeline[year]
        
        if cit_count <= low_activity_threshold:
            if not in_dormancy:
                in_dormancy = True
                dormancy_start = year
        else:
            if in_dormancy:
                dormancy_end = years[i - 1] if i > 0 else year
                dormancy_duration = dormancy_end - dormancy_start + 1
                
                if dormancy_duration >= min_dormancy_years:
                    dormancy_candidates.append((dormancy_start, dormancy_end))
                
                in_dormancy = False
                dormancy_start = None
    
    # Check if dormancy extends to the end of the timeline
    if in_dormancy and len(years) > 0:
        dormancy_end = years[-1]
        dormancy_duration = dormancy_end - dormancy_start + 1
        if dormancy_duration >= min_dormancy_years:
            dormancy_candidates.append((dormancy_start, dormancy_end))
    
    if dormancy_candidates:
        # Return the longest dormancy period
        return max(dormancy_candidates, key=lambda x: x[1] - x[0])
    
    return None, None


def calculate_rif(
    citation_timeline: dict[int, int],
    dormant_period: Tuple[Optional[int], Optional[int]]
) -> float:
    """
    Calculate Revival Impact Factor (RIF).
    
    RIF = spike_magnitude * rarity_factor
    
    Where:
    - spike_magnitude: The height of the citation spike after dormancy
    - rarity_factor: A factor based on how long the dormancy was
    
    Args:
        citation_timeline: Dictionary mapping year to citation count
        dormant_period: Tuple of (dormant_start, dormant_end) from detect_dormancy
    
    Returns:
        RIF score (0.0 if no revival detected)
    """
    dormant_start, dormant_end = dormant_period
    
    if dormant_start is None or dormant_end is None:
        return 0.0
    
    years = sorted(citation_timeline.keys())
    
    # Find citations after dormancy
    post_dormancy_years = [y for y in years if y > dormant_end]
    
    if not post_dormancy_years:
        return 0.0
    
    pre_dormancy_citations = sum(
        citation_timeline.get(y, 0) 
        for y in range(min(years), dormant_start)
    )
    
    post_dormancy_citations = [citation_timeline.get(y, 0) for y in post_dormancy_years]
    
    if not post_dormancy_citations or max(post_dormancy_citations) == 0:
        return 0.0
    
    # Calculate spike magnitude (max post-dormancy / average pre-dormancy)
    avg_pre_dormancy = pre_dormancy_citations / max(1, dormant_start - min(years))
    max_post_dormancy = max(post_dormancy_citations)
    
    if avg_pre_dormancy == 0:
        spike_magnitude = max_post_dormancy
    else:
        spike_magnitude = max_post_dormancy / avg_pre_dormancy
    
    # Calculate rarity factor based on dormancy duration
    dormancy_duration = dormant_end - dormant_start
    rarity_factor = 1.0 + (dormancy_duration / 10.0)  # Linear scaling
    
    # Check if there's a significant revival spike
    if spike_magnitude < 2.0:  # Threshold for significant revival
        return 0.0
    
    rif_score = spike_magnitude * rarity_factor
    
    return rif_score


def diffusion_distance(
    graph,
    source_node: str,
    target_node: str,
    embedding_dim: int = 128
) -> float:
    """
    Calculate diffusion distance between two nodes in a citation graph.
    
    Uses random walk with restart to measure how far knowledge has diffused.
    
    Args:
        graph: NetworkX graph object
        source_node: Starting node
        target_node: Target node
        embedding_dim: Dimension for node embeddings
    
    Returns:
        Diffusion distance (lower means closer in knowledge space)
    """
    import networkx as nx
    from scipy.spatial.distance import cosine
    
    if source_node not in graph or target_node not in graph:
        return float('inf')
    
    # Same node has zero distance
    if source_node == target_node:
        return 0.0
    
    # Check if graph has edges
    if len(graph.edges()) == 0:
        return float('inf')
    
    # Simple approach: use shortest path weighted by edge attributes
    try:
        has_weight = 'weight' in next(iter(graph.edges(data=True)))[2]
        distance = nx.shortest_path_length(
            graph, 
            source_node, 
            target_node,
            weight='weight' if has_weight else None
        )
        return float(distance)
    except nx.NetworkXNoPath:
        return float('inf')


def breakthrough_score(
    paper_citations: List[dict],
    field_boundaries: dict[str, set[str]]
) -> float:
    """
    Calculate how much a paper breaks through field boundaries.
    
    Args:
        paper_citations: List of citing papers with their field information
        field_boundaries: Dictionary mapping field names to sets of subfields
    
    Returns:
        Breakthrough score (0-1, higher means more boundary-crossing)
    """
    if not paper_citations:
        return 0.0
    
    fields_represented = set()
    for citation in paper_citations:
        field = citation.get('field', '')
        if field:
            fields_represented.add(field)
    
    num_fields = len(fields_represented)
    
    # Normalize by total possible fields
    total_fields = len(field_boundaries)
    if total_fields == 0:
        return 0.0
    
    return min(1.0, num_fields / total_fields)
