"""Tests for analyzer module"""

import pytest
from core.analyzer import Analyzer

@pytest.fixture
def analyzer():
    return Analyzer()

def test_analyzer_initialization(analyzer):
    """Test analyzer initialization"""
    assert analyzer is not None
    assert analyzer.confidence_engine is not None
    assert analyzer.risk_engine is not None

def test_price_expansion_analysis(analyzer):
    """Test price expansion analysis"""
    closes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110] * 2
    
    result = analyzer._analyze_price_expansion(closes, 110)
    
    assert result['score'] > 0
    assert len(result['reasons']) > 0
