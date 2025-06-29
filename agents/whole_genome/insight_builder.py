import json
from typing import Dict, Any
from ..common.base import BaseAgent

class WholeGenomeInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract whole genome-specific data for context
        genome_data = report.get("genome_data", {})
        snps = report.get("snps", {})
        structural_variants = report.get("structural_variants", {})
        ancestry = report.get("ancestry", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a whole genome sequencing specialist analyzing data for user {user_id}.

GENOME DATA:
{json.dumps(genome_data, indent=2)}

SNPS:
{json.dumps(snps, indent=2)}

STRUCTURAL VARIANTS:
{json.dumps(structural_variants, indent=2)}

ANCESTRY:
{json.dumps(ancestry, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive whole genome insights including:

1. GENOME-WIDE ANALYSIS:
   - Overall genome characteristics
   - Key genetic variations identified
   - Coverage and quality assessment
   - Novel variant discovery

2. SNP ANALYSIS:
   - Common variant associations
   - Complex trait predispositions
   - Population-specific variants
   - Polygenic risk scores

3. STRUCTURAL VARIANT ASSESSMENT:
   - Copy number variations
   - Insertions and deletions
   - Inversions and translocations
   - Clinical significance

4. ANCESTRY AND POPULATION GENETICS:
   - Genetic ancestry composition
   - Population-specific risks
   - Geographic origins
   - Genetic diversity assessment

5. HEALTH IMPLICATIONS:
   - Disease risk assessment
   - Complex trait associations
   - Pharmacogenomic insights
   - Preventive health opportunities

6. ACTIONABLE INSIGHTS:
   - Specific genetic targets
   - Intervention opportunities
   - Screening recommendations
   - Prevention strategies

Provide evidence-based insights that explain genome-wide patterns in the context of overall health and wellness.
"""
        )
        return self.generate(prompt, max_tokens=600) 