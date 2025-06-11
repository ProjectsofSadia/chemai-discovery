"""
Test Suite for ChemAI Discovery Platform
Comprehensive testing for all components
"""

import pytest
import asyncio
import numpy as np
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestMolecularAnalysis:
    """Test molecular analysis functionality"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "optimal"
        assert "version" in data
    
    def test_analyze_molecule_valid(self):
        """Test molecule analysis with valid SMILES"""
        response = client.post("/api/v2/analyze-molecule", 
                             json={"smiles": "CCO"})
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert "overall_confidence" in data
        assert data["smiles"] == "CCO"
    
    def test_analyze_molecule_invalid(self):
        """Test molecule analysis with invalid SMILES"""
        response = client.post("/api/v2/analyze-molecule", 
                             json={"smiles": "INVALID"})
        assert response.status_code == 400
    
    def test_analyze_molecule_empty(self):
        """Test molecule analysis with empty SMILES"""
        response = client.post("/api/v2/analyze-molecule", 
                             json={"smiles": ""})
        assert response.status_code == 400

class TestMolecularGeneration:
    """Test molecular generation functionality"""
    
    def test_generate_molecules_valid(self):
        """Test molecule generation with valid parameters"""
        response = client.post("/api/v2/generate-molecules", 
                             json={
                                 "target_properties": {
                                     "solubility": -2.0,
                                     "bioavailability": 70.0
                                 },
                                 "count": 5
                             })
        assert response.status_code == 200
        data = response.json()
        assert "molecules" in data
        assert len(data["molecules"]) == 5
        assert "statistics" in data
    
    def test_generate_molecules_no_targets(self):
        """Test molecule generation without target properties"""
        response = client.post("/api/v2/generate-molecules", 
                             json={"count": 5})
        assert response.status_code == 400
    
    def test_generate_molecules_large_count(self):
        """Test molecule generation with large count"""
        response = client.post("/api/v2/generate-molecules", 
                             json={
                                 "target_properties": {"solubility": -2.0},
                                 "count": 200  # Should be capped at MAX_MOLECULES_PER_REQUEST
                             })
        assert response.status_code == 200
        data = response.json()
        assert len(data["molecules"]) <= 100  # Should be capped

class TestAPI:
    """Test API functionality"""
    
    def test_stats_endpoint(self):
        """Test statistics endpoint"""
        response = client.get("/api/v2/stats")
        assert response.status_code == 200
        data = response.json()
        assert "platform_stats" in data
        assert "model_performance" in data
    
    def test_landing_page(self):
        """Test landing page access"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_platform_page(self):
        """Test platform page access"""
        response = client.get("/platform")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

class TestModelValidation:
    """Test AI model validation"""
    
    @pytest.mark.asyncio
    async def test_model_initialization(self):
        """Test that AI models initialize correctly"""
        from src.main import molecular_ai, molecular_generator
        
        # Wait for initialization if needed
        await asyncio.sleep(1)
        
        assert molecular_ai.is_initialized
        assert molecular_generator.is_initialized
    
    def test_prediction_consistency(self):
        """Test prediction consistency"""
        # Test same molecule multiple times
        smiles = "CCO"
        results = []
        
        for _ in range(3):
            response = client.post("/api/v2/analyze-molecule", 
                                 json={"smiles": smiles})
            assert response.status_code == 200
            results.append(response.json())
        
        # Check that predictions are consistent (within tolerance)
        for prop in results[0]["predictions"]:
            values = [r["predictions"][prop]["value"] for r in results]
            std_dev = np.std(values)
            assert std_dev < 0.1  # Should be very consistent

class TestPerformance:
    """Test performance characteristics"""
    
    def test_analysis_speed(self):
        """Test that analysis completes quickly"""
        import time
        
        start_time = time.time()
        response = client.post("/api/v2/analyze-molecule", 
                             json={"smiles": "CCO"})
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 5.0  # Should complete in under 5 seconds
    
    def test_generation_speed(self):
        """Test that generation completes reasonably quickly"""
        import time
        
        start_time = time.time()
        response = client.post("/api/v2/generate-molecules", 
                             json={
                                 "target_properties": {"solubility": -2.0},
                                 "count": 5
                             })
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 10.0  # Should complete in under 10 seconds

class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_extreme_property_values(self):
        """Test handling of extreme property values"""
        response = client.post("/api/v2/generate-molecules", 
                             json={
                                 "target_properties": {
                                     "solubility": -20.0,  # Extreme value
                                     "bioavailability": 150.0  # Invalid value
                                 },
                                 "count": 3
                             })
        assert response.status_code == 200  # Should handle gracefully
    
    def test_unicode_smiles(self):
        """Test handling of unicode characters in SMILES"""
        response = client.post("/api/v2/analyze-molecule", 
                             json={"smiles": "CCO🧬"})  # Unicode character
        assert response.status_code == 400  # Should reject invalid characters

# Fixtures for test data
@pytest.fixture
def sample_molecules():
    """Sample molecules for testing"""
    return [
        "CCO",  # Ethanol
        "CC(=O)O",  # Acetic acid
        "c1ccccc1",  # Benzene
        "CCN(CC)CC",  # Triethylamine
        "CC(C)(C)c1ccc(O)cc1"  # 4-tert-butylphenol
    ]

@pytest.fixture
def sample_properties():
    """Sample target properties for testing"""
    return {
        "solubility": -2.0,
        "bioavailability": 70.0,
        "drug_likeness": 0.8,
        "toxicity": 0.2
    }

# Run tests with: pytest tests/ -v
