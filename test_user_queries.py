#!/usr/bin/env python3
"""
Test script to demonstrate user-specific query functionality
"""

from orchestrator import AgentOrchestrator

def test_user_queries():
    # Initialize the orchestrator
    qa = AgentOrchestrator()
    
    # Sample demographics and baseline data
    demographics = {"age": 35, "sex": "F"}
    baseline = {
        "mean_health_score": 0.12,
        "mean_similarity_score": 0.15,
        "mean_shannon_diversity": 3.5,
        "mean_species_richness": 160,
        "healthy_scfa_ranges": {
            "butyrate": {"min": 2.0, "max": 4.0},
            "propionate": {"min": 1.5, "max": 3.0},
            "acetate": {"min": 3.5, "max": 6.0}
        }
    }
    
    print("=" * 60)
    print("BIOMARKER AGENTIC Q&A SYSTEM - USER TESTING")
    print("=" * 60)
    
    # Show available users
    available_users = qa.get_available_users()
    print(f"Available users: {', '.join(available_users)}")
    print()
    
    # Test different users with different queries
    test_cases = [
        ("user_001", "Can you explain my gut health report?"),
        ("user_005", "What recommendations do you have for me?"),
        ("user_003", "How do I compare to others?"),
        ("user_008", "What is health_score?"),
        ("user_002", "Can you explain my microbiome composition?"),
        ("user_006", "What should I eat to improve my gut health?")
    ]
    
    for user_id, query in test_cases:
        print(f"\n{'='*20} USER: {user_id} {'='*20}")
        print(f"Query: {query}")
        print("-" * 60)
        
        try:
            response = qa.handle_user_query(user_id, query, 
                                          demographics=demographics, 
                                          baseline=baseline)
            print(response)
        except Exception as e:
            print(f"Error processing query: {e}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    test_user_queries() 