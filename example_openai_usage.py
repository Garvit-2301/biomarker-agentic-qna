#!/usr/bin/env python3
"""
Example usage of OpenAI client with the biomarker Q&A system
"""

import os
from orchestrator import AgentOrchestrator

def main():
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("=" * 60)
    print("OPENAI CLIENT EXAMPLE")
    print("=" * 60)
    
    # Initialize orchestrator with OpenAI client
    print("Initializing OpenAI client...")
    qa = AgentOrchestrator("openai", model="gpt-4")
    
    # Show system info
    print(f"LLM Info: {qa.get_llm_info()}")
    print(f"Available users: {qa.get_available_users()}")
    
    # Sample data
    demographics = {"age": 35, "sex": "F"}
    baseline = {
        "mean_health_score": 0.12,
        "mean_similarity_score": 0.15,
        "mean_shannon_diversity": 3.5,
        "mean_species_richness": 160
    }
    
    # Example queries
    example_queries = [
        ("user_001", "Can you explain my gut health report?"),
        ("user_005", "What recommendations do you have for me?"),
        ("user_003", "How do I compare to others?"),
        ("user_008", "What is health_score?")
    ]
    
    for user_id, query in example_queries:
        print(f"\n{'='*20} USER: {user_id} {'='*20}")
        print(f"Query: {query}")
        print("-" * 60)
        
        try:
            response = qa.handle_user_query(user_id, query, 
                                          demographics=demographics, 
                                          baseline=baseline)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    main() 