#!/usr/bin/env python3
"""
Simple test script for Auto-Diligence system
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from agents.base_agent import BaseAgent
        print("✅ BaseAgent imported successfully")
        
        from agents.cto_agent import CTOAgent
        print("✅ CTOAgent imported successfully")
        
        from agents.cfo_agent import CFOAgent
        print("✅ CFOAgent imported successfully")
        
        from agents.ceo_agent import CEOAgent
        print("✅ CEOAgent imported successfully")
        
        from agents.cpo_agent import CPOAgent
        print("✅ CPOAgent imported successfully")
        
        from agents.risk_agent import RiskAgent
        print("✅ RiskAgent imported successfully")
        
        from reasoning.reasoning_engine import reason
        print("✅ Reasoning engine imported successfully")
        
        from alerts.alert_engine import trigger_alert
        print("✅ Alert engine imported successfully")
        
        from storage.vector_store import store_event, search_similar
        print("✅ Vector store imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_agents():
    """Test agent functionality"""
    print("\nTesting agents...")
    
    try:
        from agents.cto_agent import CTOAgent
        
        # Test CTO Agent
        cto = CTOAgent()
        data = cto.fetch_data()
        analysis = cto.analyze(data)
        signal = cto.emit_signal(analysis)
        
        print(f"✅ CTO Agent working: {signal}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        return False

def test_reasoning():
    """Test reasoning engine"""
    print("\nTesting reasoning engine...")
    
    try:
        from reasoning.reasoning_engine import reason
        
        # Mock signals
        test_signals = {
            "CTO": {"severity": "high", "tech_health": "declining"},
            "CFO": {"severity": "medium", "financial_mode": "cost-control"}
        }
        
        result = reason(test_signals)
        print(f"✅ Reasoning engine working: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reasoning test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Auto-Diligence System Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_agents():
        tests_passed += 1
        
    if test_reasoning():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! System is ready.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)