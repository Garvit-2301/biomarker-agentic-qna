#!/usr/bin/env python3
"""
Test script to demonstrate different LLM clients (OpenAI and Llama3)
"""

import os
from utils.llm_factory import LLMFactory
from orchestrator import AgentOrchestrator

def test_llm_clients():
    print("=" * 60)
    print("LLM CLIENT TESTING")
    print("=" * 60)
    
    # Sample demographics and baseline data
    demographics = {"age": 35, "sex": "F"}
    baseline = {
        "mean_health_score": 0.12,
        "mean_similarity_score": 0.15,
        "mean_shannon_diversity": 3.5,
        "mean_species_richness": 160
    }
    
    # Test different LLM clients
    clients_to_test = [
        ("openai", {"model": "gpt-4"}),
        ("openai", {"model": "gpt-3.5-turbo"}),
        ("llama3", {})
    ]
    
    for client_type, kwargs in clients_to_test:
        print(f"\n{'='*20} TESTING {client_type.upper()} {'='*20}")
        
        try:
            # Test client creation
            print(f"Creating {client_type} client...")
            client = LLMFactory.create_client(client_type, **kwargs)
            print(f"✓ {client_type} client created successfully")
            
            # Test connection
            print(f"Testing {client_type} connection...")
            if client.test_connection():
                print(f"✓ {client_type} connection successful")
            else:
                print(f"✗ {client_type} connection failed")
                continue
            
            # Test basic generation
            print(f"Testing {client_type} generation...")
            test_prompt = "Explain what a microbiome is in one sentence."
            response = client.generate(test_prompt, max_tokens=100, temperature=0.3)
            print(f"✓ {client_type} response: {response[:100]}...")
            
            # Test with orchestrator
            print(f"Testing {client_type} with orchestrator...")
            qa = AgentOrchestrator(client_type, **kwargs)
            print(f"✓ Orchestrator created with {client_type}")
            print(f"LLM Info: {qa.get_llm_info()}")
            
            # Test user query
            response = qa.handle_user_query("user_001", "What is health_score?",
                                          demographics=demographics, baseline=baseline)
            print(f"✓ User query response: {response[:150]}...")
            
        except Exception as e:
            print(f"✗ Error with {client_type}: {e}")
            continue
        
        print(f"✓ {client_type} testing completed successfully")
    
    print("\n" + "="*60)
    print("TESTING SUMMARY")
    print("="*60)
    
    # Show available clients
    available_clients = LLMFactory.get_available_clients()
    print(f"Available client types: {', '.join(available_clients)}")
    
    # Test each available client
    for client_type in available_clients:
        try:
            success = LLMFactory.test_client(client_type)
            status = "✓ Working" if success else "✗ Failed"
            print(f"{client_type}: {status}")
        except Exception as e:
            print(f"{client_type}: ✗ Error - {e}")

def test_openai_models():
    """Test different OpenAI models"""
    print("\n" + "="*60)
    print("OPENAI MODEL TESTING")
    print("="*60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("✗ OPENAI_API_KEY not set, skipping OpenAI model tests")
        return
    
    try:
        client = LLMFactory.create_client("openai")
        models = client.get_available_models()
        print(f"Available OpenAI models: {len(models)} found")
        
        # Test common models
        common_models = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]
        
        for model in common_models:
            if model in models:
                print(f"✓ {model} is available")
            else:
                print(f"✗ {model} is not available")
                
    except Exception as e:
        print(f"Error testing OpenAI models: {e}")

if __name__ == "__main__":
    test_llm_clients()
    test_openai_models() 