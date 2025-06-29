import json
from .base import BaseAgent

class CompareAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        baseline = context.get("baseline", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract comprehensive data for comparison
        health_score = report.get("health_score", 0)
        similarity_score = report.get("similarity_score", 0)
        diversity_scores = report.get("diversity_scores", {})
        functional_markers = report.get("functional_markers", {})
        microbiome_comp = report.get("microbiome_composition", {})
        
        prompt = (
f"""
Compare user {user_id}'s microbiome report to population baseline data.

USER DATA:
Health Score: {health_score}
Similarity Score: {similarity_score}
Diversity Metrics: {diversity_scores}
Functional Markers: {functional_markers}
Microbiome Composition: {microbiome_comp}

POPULATION BASELINE:
{json.dumps(baseline, indent=2)}

Provide a comprehensive comparison including:

1. HEALTH SCORE COMPARISON:
   - How user compares to population average
   - Percentile ranking if possible
   - Health implications

2. DIVERSITY COMPARISON:
   - Shannon diversity vs population norms
   - Species richness comparison
   - What this means for health

3. FUNCTIONAL MARKERS:
   - SCFA levels vs healthy ranges
   - Inflammation markers vs normal
   - Metabolic implications

4. MICROBIOME COMPOSITION:
   - Firmicutes/Bacteroidetes ratio analysis
   - Balance assessment
   - Health implications

5. OVERALL ASSESSMENT:
   - Above/below average summary
   - Key strengths and areas for improvement
   - Risk factors identified

Use specific numbers and explain what they mean for the user's health.
"""
        )
        return self.llm.generate(prompt, max_tokens=500)

