import json
from ..common.base import BaseAgent

class MethylationInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract methylation-specific data
        methylation_score = report.get("methylation_score", 0)
        cpg_sites = report.get("cpg_sites", {})
        epigenetic_age = report.get("epigenetic_age", {})
        methylation_patterns = report.get("methylation_patterns", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a DNA methylation specialist analyzing data for user {user_id}.

METHYLATION REPORT DATA:
Methylation Score: {methylation_score}
CpG Sites Analysis: {cpg_sites}
Epigenetic Age: {epigenetic_age}
Methylation Patterns: {methylation_patterns}
Health Implications: {health_implications}

Generate a comprehensive methylation analysis including:

1. METHYLATION SCORE INTERPRETATION:
   - What the methylation score means
   - Healthy vs unhealthy ranges
   - Age-related methylation changes

2. CPG SITES ANALYSIS:
   - Key CpG sites and their significance
   - Methylation patterns in different genomic regions
   - Regulatory implications

3. EPIGENETIC AGE ASSESSMENT:
   - Biological vs chronological age
   - Age acceleration/deceleration
   - Health implications of age-related methylation

4. METHYLATION PATTERNS:
   - Tissue-specific methylation
   - Disease-associated patterns
   - Environmental influences

5. HEALTH IMPLICATIONS:
   - Disease risk assessment
   - Lifestyle factors affecting methylation
   - Potential interventions

6. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the methylation data means for the user's health and aging.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 