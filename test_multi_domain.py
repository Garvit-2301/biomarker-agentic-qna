#!/usr/bin/env python3
"""
Test script to demonstrate multi-domain biomarker Q&A system
"""

import os
from multi_domain_orchestrator import MultiDomainOrchestrator

def test_multi_domain_system():
    print("=" * 60)
    print("MULTI-DOMAIN BIOMARKER Q&A SYSTEM TESTING")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize the multi-domain orchestrator
    print("Initializing multi-domain orchestrator...")
    qa = MultiDomainOrchestrator("openai", model="gpt-4")
    
    # Show system info
    print(f"LLM Info: {qa.get_llm_info()}")
    print(f"Available users: {qa.get_available_users()}")
    
    # Sample demographics and baseline data
    demographics = {"age": 35, "sex": "F"}
    baseline = {
        "methylation": {
            "mean_methylation_score": 0.65,
            "mean_epigenetic_age": 38,
            "age_acceleration_percentile": 50
        },
        "metagenomics": {
            "mean_health_score": 0.12,
            "mean_similarity_score": 0.15,
            "mean_shannon_diversity": 3.5
        },
        "whole_exome": {
            "mean_variant_count": 12000,
            "mean_pathogenic_variants": 2,
            "mean_vus_variants": 15
        },
        "proteomics": {
            "mean_protein_expression": 1.0,
            "mean_inflammation_score": 2.0,
            "mean_metabolic_score": 1.2
        }
    }
    
    # Test queries for different domains
    test_queries = [
        # Methylation queries
        ("user_001", "Can you explain my methylation report?"),
        ("user_001", "What is CpG methylation?"),
        ("user_001", "How does my epigenetic age compare to others?"),
        
        # Metagenomics queries
        ("user_001", "Can you explain my microbiome results?"),
        ("user_001", "What is Shannon diversity?"),
        ("user_001", "How do my gut bacteria compare to the population?"),
        
        # Whole exome queries
        ("user_001", "Can you explain my whole exome sequencing results?"),
        ("user_001", "What is a VUS variant?"),
        ("user_001", "How do my genetic variants compare to others?"),
        
        # Proteomics queries
        ("user_001", "Can you explain my proteomics results?"),
        ("user_001", "What is protein phosphorylation?"),
        ("user_001", "How do my protein levels compare to normal ranges?"),
    ]
    
    for user_id, query in test_queries:
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

def test_domain_classification():
    """Test domain classification functionality"""
    print("\n" + "="*60)
    print("DOMAIN CLASSIFICATION TESTING")
    print("="*60)
    
    if not os.getenv("OPENAI_API_KEY"):
        return
    
    qa = MultiDomainOrchestrator("openai", model="gpt-4")
    
    # Test queries for domain classification
    test_queries = [
        "What is DNA methylation?",
        "How is my gut microbiome?",
        "Explain my genetic variants",
        "What do my protein levels mean?",
        "Tell me about my gene expression",
        "What is my genome sequence?",
        "How is my blood pressure?"
    ]
    
    for query in test_queries:
        try:
            # This would normally be done internally, but we can test the domain classifier
            from agents.common.domain_classifier import DomainClassifierAgent
            domain_classifier = DomainClassifierAgent(qa.llm)
            domain = domain_classifier.run(query, {})
            print(f"Query: '{query}' -> Domain: {domain}")
        except Exception as e:
            print(f"Error classifying '{query}': {e}")

def test_user_data_loading():
    """Test user data loading functionality"""
    print("\n" + "="*60)
    print("USER DATA LOADING TESTING")
    print("="*60)
    
    from utils.user_data_loader import UserDataLoader
    
    loader = UserDataLoader()
    
    # Test available users
    users = loader.get_available_users()
    print(f"Available users: {users}")
    
    # Test available domains for user_001
    if "user_001" in users:
        domains = loader.get_available_domains("user_001")
        print(f"Available domains for user_001: {domains}")
        
        # Test loading data for each domain
        for domain in domains:
            data = loader.load_user_report("user_001", domain)
            if data:
                print(f"✓ Loaded {domain} data for user_001")
            else:
                print(f"✗ Failed to load {domain} data for user_001")

if __name__ == "__main__":
    test_multi_domain_system()
    test_domain_classification()
    test_user_data_loading() 