import json
from ..common.base import BaseAgent

class WholeExomeInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract whole exome-specific data
        variant_count = report.get("variant_count", 0)
        pathogenic_variants = report.get("pathogenic_variants", [])
        vus_variants = report.get("vus_variants", [])  # Variants of Uncertain Significance
        gene_annotations = report.get("gene_annotations", {})
        disease_risk = report.get("disease_risk", {})
        pharmacogenomics = report.get("pharmacogenomics", {})
        
        prompt = (
f"""
You are a whole exome sequencing specialist analyzing genetic data for user {user_id}.

WHOLE EXOME REPORT DATA:
Total Variants: {variant_count}
Pathogenic Variants: {pathogenic_variants}
Variants of Uncertain Significance (VUS): {vus_variants}
Gene Annotations: {gene_annotations}
Disease Risk Assessment: {disease_risk}
Pharmacogenomics: {pharmacogenomics}

Generate a comprehensive whole exome analysis including:

1. VARIANT INTERPRETATION:
   - Pathogenic variant analysis and implications
   - VUS interpretation and monitoring recommendations
   - Clinical significance of findings

2. GENE FUNCTION ANALYSIS:
   - Key genes and their biological functions
   - Pathway implications
   - Protein function impact

3. DISEASE RISK ASSESSMENT:
   - Monogenic disease risks
   - Complex disease predispositions
   - Carrier status implications

4. PHARMACOGENOMICS:
   - Drug metabolism variants
   - Medication response predictions
   - Personalized medicine implications

5. FAMILY IMPLICATIONS:
   - Inheritance patterns
   - Family member testing recommendations
   - Reproductive planning considerations

6. CLINICAL RECOMMENDATIONS:
   - Follow-up testing suggestions
   - Specialist referrals
   - Monitoring protocols

7. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the genetic data means for the user's health and medical care.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 