import json
from .base import BaseAgent

class RecommendationAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        demographics = context.get("demographics", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract comprehensive data for personalized recommendations
        health_score = report.get("health_score", 0)
        underrepresented_species = report.get("underrepresented_species", [])
        microbiome_comp = report.get("microbiome_composition", {})
        diversity_scores = report.get("diversity_scores", {})
        functional_markers = report.get("functional_markers", {})
        symptoms = report.get("symptoms", {})
        diet = report.get("diet", {})
        
        prompt = (
f"""
You are a microbiome recommendation agent providing personalized advice for user {user_id}.

USER PROFILE:
Demographics: {demographics}
Health Score: {health_score}
Current Symptoms: {symptoms}
Current Diet: {diet}

MICROBIOME ANALYSIS:
Underrepresented Species: {underrepresented_species}
Microbiome Composition: {microbiome_comp}
Diversity Scores: {diversity_scores}
Functional Markers: {functional_markers}

Provide personalized, practical recommendations (3-4 specific suggestions each):

1. NUTRITION RECOMMENDATIONS:
   - Foods to increase based on missing species
   - Dietary changes to address symptoms
   - Specific foods for microbiome diversity

2. LIFESTYLE RECOMMENDATIONS:
   - Exercise suggestions based on energy levels
   - Stress management if inflammation is high
   - Sleep optimization if relevant

3. SUPPLEMENTS (if appropriate):
   - Probiotic strains to target missing species
   - Prebiotics for diversity
   - Anti-inflammatory supplements if needed

4. MONITORING SUGGESTIONS:
   - What to track for improvement
   - Timeline for reassessment

Make recommendations specific to this user's data and current health status.
"""
        )
        return self.llm.generate(prompt, max_tokens=600)

