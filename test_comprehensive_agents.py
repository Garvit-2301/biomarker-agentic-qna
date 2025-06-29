#!/usr/bin/env python3
"""
Comprehensive test script to test all agents (Insight, Q&A, Explainer, Recommendation) for each domain.
"""

import os
import sys
import json
from datetime import datetime

# Import all the new agents
from agents.methylation.qna_agent import MethylationQNAAgent
from agents.methylation.explainer_agent import MethylationExplainerAgent
from agents.metagenomics.qna_agent import MetagenomicsQNAAgent
from agents.metagenomics.explainer_agent import MetagenomicsExplainerAgent
from agents.proteomics.qna_agent import ProteomicsQNAAgent
from agents.proteomics.explainer_agent import ProteomicsExplainerAgent
from agents.transcriptomics.qna_agent import TranscriptomicsQNAAgent
from agents.transcriptomics.explainer_agent import TranscriptomicsExplainerAgent
from agents.whole_exome.qna_agent import WholeExomeQNAAgent
from agents.whole_exome.explainer_agent import WholeExomeExplainerAgent
from agents.whole_genome.qna_agent import WholeGenomeQNAAgent
from agents.whole_genome.explainer_agent import WholeGenomeExplainerAgent

# Import existing agents
from agents.methylation.insight_builder import MethylationInsightBuilderAgent
from agents.methylation.recommendation import MethylationRecommendationAgent
from agents.metagenomics.insight_builder import MetagenomicsInsightBuilderAgent
from agents.proteomics.insight_builder import ProteomicsInsightBuilderAgent
from agents.transcriptomics.insight_builder import TranscriptomicsInsightBuilderAgent
from agents.whole_exome.insight_builder import WholeExomeInsightBuilderAgent
from agents.whole_genome.insight_builder import WholeGenomeInsightBuilderAgent

from utils.mock_llm_client import MockLLMClient

def create_mock_llm():
    """Create a mock LLM client for testing."""
    return MockLLMClient(client_type="comprehensive_test")

def create_test_context(domain: str, user_id: str = "test_user_001") -> dict:
    """Create test context for a specific domain."""
    base_context = {
        "user_id": user_id,
        "report": {},
        "demographics": {"age": 35, "sex": "F"},
        "baseline": {"mean_health_score": 0.12}
    }
    
    # Add domain-specific mock data
    if domain == "methylation":
        base_context["report"] = {
            "methylation_score": 0.75,
            "cpg_sites": {"site1": 0.8, "site2": 0.6},
            "epigenetic_age": {"biological_age": 32, "chronological_age": 35},
            "methylation_patterns": {"pattern1": "normal", "pattern2": "elevated"},
            "health_implications": {"risk": "low", "status": "healthy"}
        }
    elif domain == "metagenomics":
        base_context["report"] = {
            "diversity_scores": {"shannon": 3.8, "simpson": 0.85},
            "microbiome_composition": {"bifidobacterium": 12.5, "lactobacillus": 8.3},
            "underrepresented_species": ["akkermansia", "faecalibacterium"],
            "functional_markers": {"scfa": "normal", "inflammation": "low"},
            "symptoms": {"digestive": "mild", "energy": "good"},
            "diet": {"fiber": "moderate", "diversity": "good"}
        }
    elif domain == "proteomics":
        base_context["report"] = {
            "protein_expression": {"protein1": 1.2, "protein2": 0.8},
            "biomarkers": {"crp": 2.1, "il6": 3.2},
            "pathways": {"metabolic": "normal", "inflammatory": "low"},
            "post_translational_modifications": {"phosphorylation": "normal"},
            "protein_interactions": {"complex1": "active", "complex2": "inactive"}
        }
    elif domain == "transcriptomics":
        base_context["report"] = {
            "gene_expression": {"gene1": 1.5, "gene2": 0.7},
            "pathways": {"immune": 23, "metabolic": 34},
            "regulatory_networks": {"tf1": "active", "tf2": "inactive"},
            "transcription_factors": {"tf1": "upregulated", "tf2": "downregulated"},
            "micrornas": {"mir1": "expressed", "mir2": "suppressed"}
        }
    elif domain == "whole_exome":
        base_context["report"] = {
            "variants": {"variant1": "heterozygous", "variant2": "homozygous"},
            "carrier_status": {"cystic_fibrosis": "carrier", "sickle_cell": "not_carrier"},
            "pharmacogenomics": {"cyp2d6": "normal", "cyp2c19": "normal"},
            "disease_risks": {"cancer": "low", "cardiovascular": "moderate"},
            "clinical_significance": {"pathogenic": 2, "benign": 150}
        }
    elif domain == "whole_genome":
        base_context["report"] = {
            "genomic_variants": {"variant1": "common", "variant2": "rare"},
            "structural_variations": {"sv1": "none", "sv2": "normal"},
            "copy_number_variations": {"cnv1": "normal", "cnv2": "normal"},
            "regulatory_elements": {"enhancer1": "active", "promoter1": "active"},
            "population_genetics": {"ancestry": "mixed", "diversity": "high"}
        }
    
    return base_context

def test_domain_agents(domain: str, llm_client) -> dict:
    """Test all agents for a specific domain."""
    print(f"\n🧪 Testing {domain.upper()} Domain Agents")
    print("=" * 50)
    
    results = {
        "domain": domain,
        "agents": {},
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    # Define agent classes for each domain
    agent_classes = {
        "methylation": {
            "insight": MethylationInsightBuilderAgent,
            "qna": MethylationQNAAgent,
            "explainer": MethylationExplainerAgent,
            "recommendation": MethylationRecommendationAgent
        },
        "metagenomics": {
            "insight": MetagenomicsInsightBuilderAgent,
            "qna": MetagenomicsQNAAgent,
            "explainer": MetagenomicsExplainerAgent
        },
        "proteomics": {
            "insight": ProteomicsInsightBuilderAgent,
            "qna": ProteomicsQNAAgent,
            "explainer": ProteomicsExplainerAgent
        },
        "transcriptomics": {
            "insight": TranscriptomicsInsightBuilderAgent,
            "qna": TranscriptomicsQNAAgent,
            "explainer": TranscriptomicsExplainerAgent
        },
        "whole_exome": {
            "insight": WholeExomeInsightBuilderAgent,
            "qna": WholeExomeQNAAgent,
            "explainer": WholeExomeExplainerAgent
        },
        "whole_genome": {
            "insight": WholeGenomeInsightBuilderAgent,
            "qna": WholeGenomeQNAAgent,
            "explainer": WholeGenomeExplainerAgent
        }
    }
    
    domain_agents = agent_classes.get(domain, {})
    test_context = create_test_context(domain)
    
    for agent_type, agent_class in domain_agents.items():
        try:
            print(f"  Testing {agent_type} agent...")
            
            # Create agent instance
            agent = agent_class(llm_client)
            
            # Test queries for different agent types
            if agent_type == "insight":
                test_query = f"Can you analyze my {domain} data?"
            elif agent_type == "qna":
                test_query = f"What does my {domain} data tell me about my health?"
            elif agent_type == "explainer":
                test_query = f"What is {domain}?"
                test_context["term"] = domain
            elif agent_type == "recommendation":
                test_query = f"What recommendations do you have based on my {domain} data?"
            
            # Run the agent
            response = agent.run(test_query, test_context)
            
            # Validate response
            if response and len(response) > 10:
                print(f"    ✅ {agent_type} agent - SUCCESS")
                print(f"       Response length: {len(response)} characters")
                results["agents"][agent_type] = {
                    "status": "success",
                    "response_length": len(response),
                    "response_preview": response[:100] + "..." if len(response) > 100 else response
                }
                results["passed"] += 1
            else:
                raise Exception("Empty or too short response")
                
        except Exception as e:
            print(f"    ❌ {agent_type} agent - FAILED")
            print(f"       Error: {e}")
            results["agents"][agent_type] = {
                "status": "failed",
                "error": str(e)
            }
            results["failed"] += 1
            results["errors"].append(f"{agent_type}: {e}")
    
    print(f"  📊 {domain} Results: {results['passed']} passed, {results['failed']} failed")
    return results

def test_offline_summary_builder():
    """Test the offline summary builder."""
    print("\n🧪 Testing Offline Summary Builder")
    print("=" * 50)
    
    try:
        from agents.offline_summary_builder import OfflineSummaryBuilder
        
        # Initialize the builder
        builder = OfflineSummaryBuilder(output_dir="test_user_summaries")
        
        # Test with a single user
        user_id = "user_001"
        print(f"  Generating summary for {user_id}...")
        
        summary_data = builder.generate_user_summary(user_id)
        
        if summary_data and "domains" in summary_data:
            print(f"    ✅ Summary generation - SUCCESS")
            print(f"       Domains processed: {list(summary_data['domains'].keys())}")
            print(f"       Cross-domain insights: {'cross_domain_insights' in summary_data}")
            print(f"       Overall assessment: {'overall_health_assessment' in summary_data}")
            print(f"       Recommendations: {'recommendations' in summary_data}")
            
            # Save the summary
            filepath = builder.save_user_summary(user_id, summary_data)
            print(f"       Summary saved to: {filepath}")
            
            return {
                "status": "success",
                "domains_processed": len(summary_data.get("domains", {})),
                "filepath": filepath
            }
        else:
            raise Exception("Invalid summary data structure")
            
    except Exception as e:
        print(f"    ❌ Summary builder - FAILED")
        print(f"       Error: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }

def main():
    """Main test function."""
    print("🚀 Starting Comprehensive Agent Testing")
    print("=" * 60)
    
    # Create mock LLM client
    llm_client = create_mock_llm()
    
    # Test all domains
    domains = ["methylation", "metagenomics", "proteomics", "transcriptomics", "whole_exome", "whole_genome"]
    
    all_results = {
        "test_timestamp": datetime.now().isoformat(),
        "domains": {},
        "offline_summary": {},
        "summary": {"total_passed": 0, "total_failed": 0, "success_rate": 0.0}
    }
    
    # Test domain agents
    for domain in domains:
        domain_results = test_domain_agents(domain, llm_client)
        all_results["domains"][domain] = domain_results
        all_results["summary"]["total_passed"] += domain_results["passed"]
        all_results["summary"]["total_failed"] += domain_results["failed"]
    
    # Test offline summary builder
    offline_results = test_offline_summary_builder()
    all_results["offline_summary"] = offline_results
    
    # Calculate success rate
    total_tests = all_results["summary"]["total_passed"] + all_results["summary"]["total_failed"]
    if total_tests > 0:
        all_results["summary"]["success_rate"] = (
            all_results["summary"]["total_passed"] / total_tests
        ) * 100
    
    # Save results
    os.makedirs("testing_logs", exist_ok=True)
    results_file = "testing_logs/comprehensive_agent_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Print final results
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    print(f"Overall Success Rate: {all_results['summary']['success_rate']:.1f}%")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {all_results['summary']['total_passed']}")
    print(f"Failed: {all_results['summary']['total_failed']}")
    
    print(f"\nDomain Results:")
    for domain, results in all_results["domains"].items():
        status = "✅" if results["failed"] == 0 else "⚠️" if results["passed"] > results["failed"] else "❌"
        print(f"  {status} {domain}: {results['passed']}/{results['passed'] + results['failed']} passed")
    
    print(f"\nOffline Summary Builder: {'✅ PASSED' if offline_results['status'] == 'success' else '❌ FAILED'}")
    
    if all_results['summary']['success_rate'] >= 90:
        print("\n🎉 EXCELLENT! All comprehensive agent tests passed successfully!")
    elif all_results['summary']['success_rate'] >= 80:
        print("\n✅ GOOD! Most comprehensive agent tests passed successfully!")
    elif all_results['summary']['success_rate'] >= 70:
        print("\n⚠️  FAIR! Some comprehensive agent tests need attention!")
    else:
        print("\n❌ POOR! Many comprehensive agent tests failed and need immediate attention!")
    
    print(f"\nDetailed results saved to: {results_file}")
    print("Check the testing_logs directory for detailed logs.")

if __name__ == "__main__":
    main() 