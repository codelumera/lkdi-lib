"""
L-KDI: Latent Knowledge Diffusion Index

A package for detecting Revival Impact Factor (RIF) in scientific literature.
"""

__version__ = "0.1.0"
__author__ = "stipwunaraha"

from lkdi.detector import RevivalDetector
from lkdi.graph_builder import CitationGraphBuilder
from lkdi.metrics import calculate_rif, detect_dormancy

__all__ = [
    "RevivalDetector",
    "CitationGraphBuilder",
    "calculate_rif",
    "detect_dormancy",
]
