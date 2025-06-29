import json
from ..common.base import BaseAgent

class WholeGenomeInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract whole genome-specific data
        snp_variants = report.get("snp_variants", {})
        structural_variants = report.get("structural_variants", {})
        copy_number_variants = report.get("cnv", {})
        genome_wide_associations = report.get("gwas", {})
        ancestry_analysis = report.get("ancestry", {})
        complex_traits = report.get("complex_traits", {})
        
        prompt = (
f"""
You are a whole genome sequencing specialist analyzing complete genomic data for user {user_id}.

WHOLE GENOME REPORT DATA:
SNP Variants: {snp_variants}
Structural Variants: {structural_variants}
Copy Number Variants: {copy_number_variants}
Genome-Wide Associations: {genome_wide_associations}
Ancestry Analysis: {ancestry_analysis}
Complex Traits: {complex_traits}

Generate a comprehensive whole genome analysis including:

1. GENETIC VARIANT ANALYSIS:
   - SNP interpretation and significance
   - Structural variant implications
   - Copy number variant effects

2. GENOME-WIDE ASSOCIATION STUDIES:
   - Disease risk associations
   - Trait associations
   - Population-specific findings

3. ANCESTRY AND POPULATION GENETICS:
   - Genetic ancestry composition
   - Population-specific risks
   - Evolutionary implications

4. COMPLEX TRAIT ANALYSIS:
   - Polygenic risk scores
   - Complex disease predispositions
   - Trait predictions

5. STRUCTURAL GENOMIC VARIATIONS:
   - Large-scale genomic changes
   - Chromosomal abnormalities
   - Functional implications

6. CLINICAL INTERPRETATION:
   - Disease risk assessment
   - Pharmacogenomic implications
   - Personalized medicine opportunities

7. FAMILY AND REPRODUCTIVE IMPLICATIONS:
   - Inheritance patterns
   - Family planning considerations
   - Genetic counseling recommendations

8. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the whole genome data means for the user's health, ancestry, and personalized medicine opportunities.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 