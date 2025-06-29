import json
from .base import BaseAgent

class CompareAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        baseline = context.get("baseline", {})
        domain = context.get("domain", "general")
        user_id = context.get("user_id", "Unknown")
        
        domain_contexts = {
            "methylation": "methylation patterns, epigenetic age, CpG sites",
            "metagenomics": "microbiome composition, diversity scores, functional markers",
            "whole_exome": "genetic variants, disease risks, pharmacogenomics",
            "proteomics": "protein expression, biomarker levels, pathway analysis",
            "transcriptomics": "gene expression, differentially expressed genes, regulatory networks",
            "whole_genome": "genomic variants, ancestry, complex traits"
        }
        
        domain_context = domain_contexts.get(domain, "biomarker data")
        
        prompt = (
f"""
You are a {domain} specialist comparing user {user_id}'s data to population baselines.

USER DATA:
{json.dumps(report, indent=2)}

POPULATION BASELINE:
{json.dumps(baseline, indent=2)}

Domain context: {domain_context}

Provide a comprehensive comparison including:

1. OVERALL ASSESSMENT:
   - How user compares to population average
   - Percentile rankings where available
   - Health implications

2. KEY METRICS COMPARISON:
   - Specific measurements vs population norms
   - Statistical significance of differences
   - Clinical relevance

3. RISK ASSESSMENT:
   - Disease risk compared to population
   - Protective factors identified
   - Areas of concern

4. STRENGTHS AND WEAKNESSES:
   - Above-average areas
   - Below-average areas
   - Neutral findings

5. POPULATION CONTEXT:
   - Age/gender-specific comparisons
   - Ethnic/ancestry considerations
   - Lifestyle factor influences

6. CLINICAL IMPLICATIONS:
   - Monitoring recommendations
   - Intervention opportunities
   - Follow-up testing suggestions

Use specific numbers and explain what they mean for the user's health in the context of {domain}.
"""
        )
        return self.llm.generate(prompt, max_tokens=500) 