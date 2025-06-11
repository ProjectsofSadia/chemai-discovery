"""
Performance and Load Testing for ChemAI Discovery
"""

import pytest
import time
import asyncio
import concurrent.futures
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestPerformanceBenchmarks:
    """Performance benchmark tests"""
    
    def test_single_analysis_performance(self):
        """Benchmark single molecule analysis"""
        smiles = "CC(C)(C)c1ccc(O)cc1"
        
        times = []
        for _ in range(10):
            start = time.time()
            response = client.post("/api/v2/analyze-molecule", 
                                 json={"smiles": smiles})
            end = time.time()
            
            assert response.status_code == 200
            times.append(end - start)
        
        avg_time = sum(times) / len(times)
        print(f"Average analysis time: {avg_time:.3f}s")
        assert avg_time < 2.0  # Should be under 2 seconds
    
    def test_concurrent_analysis(self):
        """Test concurrent analysis performance"""
        smiles_list = ["CCO", "CC(=O)O", "c1ccccc1", "CCN(CC)CC"]
        
        def analyze_molecule(smiles):
            start = time.time()
            response = client.post("/api/v2/analyze-molecule", 
                                 json={"smiles": smiles})
            end = time.time()
            return response.status_code, end - start
        
        start_total = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(analyze_molecule, smiles) 
                      for smiles in smiles_list]
            results = [future.result() for future in futures]
        end_total = time.time()
        
        # All should succeed
        assert all(status == 200 for status, _ in results)
        
        # Should be faster than sequential
        total_time = end_total - start_total
        sequential_time = sum(time for _, time in results)
        print(f"Concurrent time: {total_time:.3f}s vs Sequential: {sequential_time:.3f}s")
        assert total_time < sequential_time
    
    def test_generation_performance(self):
        """Benchmark molecule generation"""
        target_props = {"solubility": -2.0, "bioavailability": 70.0}
        
        times = []
        for count in [1, 5, 10]:
            start = time.time()
            response = client.post("/api/v2/generate-molecules", 
                                 json={
                                     "target_properties": target_props,
                                     "count": count
                                 })
            end = time.time()
            
            assert response.status_code == 200
            times.append((count, end - start))
        
        # Time should scale reasonably with count
        for count, time_taken in times:
            rate = count / time_taken
            print(f"Generation rate: {rate:.2f} molecules/second for {count} molecules")
            assert rate > 0.5  # At least 0.5 molecules per second

class TestLoadTesting:
    """Load testing scenarios"""
    
    def test_rapid_requests(self):
        """Test handling of rapid successive requests"""
        smiles = "CCO"
        success_count = 0
        
        for i in range(20):
            response = client.post("/api/v2/analyze-molecule", 
                                 json={"smiles": smiles})
            if response.status_code == 200:
                success_count += 1
        
        # Should handle most requests successfully
        success_rate = success_count / 20
        print(f"Success rate: {success_rate:.2%}")
        assert success_rate > 0.8  # At least 80% success rate
    
    def test_memory_usage(self):
        """Test that memory usage doesn't grow excessively"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform many operations
        for i in range(50):
            response = client.post("/api/v2/analyze-molecule", 
                                 json={"smiles": f"{'C' * (i % 10 + 1)}O"})
            assert response.status_code in [200, 400]  # Valid or invalid SMILES
        
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory
        
        print(f"Memory growth: {memory_growth / 1024 / 1024:.2f} MB")
        # Memory growth should be reasonable (less than 100MB)
        assert memory_growth < 100 * 1024 * 1024

class TestScalability:
    """Test scalability characteristics"""
    
    def test_batch_processing_efficiency(self):
        """Test efficiency of processing multiple molecules"""
        molecules = [f"{'C' * i}O" for i in range(1, 11)]
        
        # Test sequential processing
        start_sequential = time.time()
        for smiles in molecules:
            response = client.post("/api/v2/analyze-molecule", 
                                 json={"smiles": smiles})
            # Don't assert here as some may be invalid
        end_sequential = time.time()
        
        sequential_time = end_sequential - start_sequential
        print(f"Sequential processing: {sequential_time:.3f}s for {len(molecules)} molecules")
        
        # Should process at reasonable rate
        rate = len(molecules) / sequential_time
        assert rate > 0.5  # At least 0.5 molecules per second

# Benchmark utilities
class PerformanceProfiler:
    """Utility class for performance profiling"""
    
    def __init__(self):
        self.results = {}
    
    def profile_endpoint(self, endpoint_func, name, iterations=10):
        """Profile an endpoint function"""
        times = []
        
        for _ in range(iterations):
            start = time.time()
            try:
                result = endpoint_func()
                success = True
            except Exception:
                success = False
            end = time.time()
            
            times.append({
                'time': end - start,
                'success': success
            })
        
        self.results[name] = {
            'avg_time': sum(t['time'] for t in times) / len(times),
            'min_time': min(t['time'] for t in times),
            'max_time': max(t['time'] for t in times),
            'success_rate': sum(1 for t in times if t['success']) / len(times)
        }
        
        return self.results[name]
    
    def print_summary(self):
        """Print performance summary"""
        print("\n" + "=" * 60)
        print("PERFORMANCE SUMMARY")
        print("=" * 60)
        
        for name, stats in self.results.items():
            print(f"\n{name}:")
            print(f"  Average Time: {stats['avg_time']:.3f}s")
            print(f"  Min Time: {stats['min_time']:.3f}s")
            print(f"  Max Time: {stats['max_time']:.3f}s")
            print(f"  Success Rate: {stats['success_rate']:.1%}")

# Run with: pytest tests/test_performance.py -v -s
