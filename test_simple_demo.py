#!/usr/bin/env python3
"""
Simple test script to verify the demo agent works correctly.
"""

import os
import sys
from agents.demo_agent import DemoAgent

def test_single_agent():
    """Test a single demo agent."""
    print("🧪 Testing Demo Agent")
    print("=" * 40)
    
    # Test methylation analysis agent
    print("Testing methylation analysis agent...")
    
    try:
        agent = DemoAgent(domain="methylation", agent_type="analysis", user_id="test_user_001")
        result = agent.process()
        
        if result["success"]:
            print("✅ SUCCESS!")
            print(f"Processing time: {result['processing_time']:.2f} seconds")
            print(f"Response length: {result['response_length']} characters")
            print(f"Prompt length: {result['prompt_length']} characters")
            print("\nResponse preview:")
            print("-" * 40)
            print(result["response"][:200] + "...")
            print("-" * 40)
        else:
            print("❌ FAILED!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False
    
    return True

def test_multiple_agents():
    """Test multiple agents across different domains."""
    print("\n🧪 Testing Multiple Agents")
    print("=" * 40)
    
    test_cases = [
        ("methylation", "analysis"),
        ("methylation", "summary"),
        ("methylation", "recommendation"),
        ("metagenomics", "analysis"),
        ("proteomics", "analysis"),
        ("transcriptomics", "analysis"),
        ("whole_exome", "analysis"),
        ("whole_genome", "analysis")
    ]
    
    passed = 0
    failed = 0
    
    for domain, agent_type in test_cases:
        print(f"\nTesting {agent_type} agent for {domain} domain...")
        
        try:
            agent = DemoAgent(domain=domain, agent_type=agent_type, user_id="test_user_001")
            result = agent.process()
            
            if result["success"]:
                print(f"  ✅ {agent_type} agent for {domain} - SUCCESS")
                print(f"     Processing time: {result['processing_time']:.2f}s")
                print(f"     Response length: {result['response_length']} chars")
                passed += 1
            else:
                print(f"  ❌ {agent_type} agent for {domain} - FAILED")
                print(f"     Error: {result.get('error', 'Unknown error')}")
                failed += 1
                
        except Exception as e:
            print(f"  ❌ {agent_type} agent for {domain} - EXCEPTION")
            print(f"     Error: {e}")
            failed += 1
    
    print(f"\n📊 Summary:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(passed/(passed+failed)*100):.1f}%")
    
    return failed == 0

def main():
    """Main test function."""
    print("🚀 Starting Simple Demo Agent Tests")
    print("=" * 50)
    
    # Test single agent
    single_success = test_single_agent()
    
    # Test multiple agents
    multiple_success = test_multiple_agents()
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    
    if single_success and multiple_success:
        print("🎉 ALL TESTS PASSED!")
        print("The demo agent system is working correctly.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the logs for details.")
    
    print("\nCheck the testing_logs directory for detailed logs.")

if __name__ == "__main__":
    main() 