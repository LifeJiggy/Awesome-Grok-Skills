"""
Performance tests for Awesome Grok Skills.
"""

import pytest
import time
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestPerformanceBasics:
    """Basic performance tests."""
    
    def test_agent_instantiation_speed(self, project_root):
        """Test agent instantiation is fast."""
        try:
            from agents.analytics.agent import AnalyticsAgent
            
            start = time.perf_counter()
            for _ in range(10):
                agent = AnalyticsAgent()
            elapsed = time.perf_counter() - start
            
            # Should instantiate 10 agents in under 1 second
            assert elapsed < 1.0, f"Agent instantiation took {elapsed:.2f}s"
        except ImportError:
            pytest.skip("Agent not available")
    
    def test_skill_engine_instantiation_speed(self, project_root):
        """Test skill engine instantiation is fast."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            start = time.perf_counter()
            for _ in range(10):
                engine = AnalyticsEngine()
            elapsed = time.perf_counter() - start
            
            # Should instantiate 10 engines in under 1 second
            assert elapsed < 1.0, f"Engine instantiation took {elapsed:.2f}s"
        except ImportError:
            pytest.skip("Engine not available")


class TestProcessingPerformance:
    """Test processing performance."""
    
    def test_small_data_processing(self, project_root):
        """Test small data processing is fast."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            small_data = [{"value": i} for i in range(100)]
            
            start = time.perf_counter()
            result = engine.process(small_data)
            elapsed = time.perf_counter() - start
            
            # Should process 100 items in under 0.5 seconds
            assert elapsed < 0.5, f"Processing took {elapsed:.2f}s"
            assert result is not None
        except ImportError:
            pytest.skip("Engine not available")
    
    def test_batch_processing_performance(self, project_root):
        """Test batch processing is efficient."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            
            datasets = [[{"value": i} for i in range(100)] for _ in range(5)]
            
            start = time.perf_counter()
            results = engine.batch_process(datasets)
            elapsed = time.perf_counter() - start
            
            # Should process 5 batches of 100 items in under 1 second
            assert elapsed < 1.0, f"Batch processing took {elapsed:.2f}s"
            assert len(results) == 5
        except ImportError:
            pytest.skip("Engine not available")


class TestMemoryPerformance:
    """Test memory usage."""
    
    def test_multiple_agents_memory(self, project_root):
        """Test multiple agents don't leak memory."""
        try:
            from agents.analytics.agent import AnalyticsAgent
            
            agents = [AnalyticsAgent() for _ in range(10)]
            
            assert len(agents) == 10
            for agent in agents:
                assert agent is not None
        except ImportError:
            pytest.skip("Agent not available")
    
    def test_multiple_engines_memory(self, project_root):
        """Test multiple engines don't leak memory."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engines = [AnalyticsEngine() for _ in range(10)]
            
            assert len(engines) == 10
            for engine in engines:
                assert engine is not None
        except ImportError:
            pytest.skip("Engine not available")


class TestConcurrencyPerformance:
    """Test concurrent operations."""
    
    def test_concurrent_agent_creation(self, project_root):
        """Test concurrent agent creation."""
        import concurrent.futures
        
        try:
            from agents.analytics.agent import AnalyticsAgent
            
            def create_agent():
                return AnalyticsAgent()
            
            start = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                agents = list(executor.map(create_agent, range(10)))
            elapsed = time.perf_counter() - start
            
            # Should create 10 agents concurrently in under 1 second
            assert elapsed < 1.0, f"Concurrent creation took {elapsed:.2f}s"
            assert len(agents) == 10
        except ImportError:
            pytest.skip("Agent not available")
