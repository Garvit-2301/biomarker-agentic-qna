import json
from .base import BaseAgent

class InsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract comprehensive data
        health_score = report.get("health_score", 0)
        similarity_score = report.get("similarity_score", 0)
        underrepresented_species = report.get("underrepresented_species", [])
        microbiome_comp = report.get("microbiome_composition", {})
        diversity_scores = report.get("diversity_scores", {})
        functional_markers = report.get("functional_markers", {})
        symptoms = report.get("symptoms", {})
        diet = report.get("diet", {})
        
        prompt = (
f"""
You are a gut-microbiome insight builder analyzing data for user {user_id}.

COMPREHENSIVE REPORT DATA:
Health Score: {health_score}
Similarity Score (diabetes risk): {similarity_score}
Underrepresented Species: {underrepresented_species}

Microbiome Composition:
- Firmicutes: {microbiome_comp.get('firmicutes', 'N/A')}
- Bacteroidetes: {microbiome_comp.get('bacteroidetes', 'N/A')}
- Actinobacteria: {microbiome_comp.get('actinobacteria', 'N/A')}
- Proteobacteria: {microbiome_comp.get('proteobacteria', 'N/A')}

Diversity Metrics:
- Shannon Diversity: {diversity_scores.get('shannon_diversity', 'N/A')}
- Species Richness: {diversity_scores.get('species_richness', 'N/A')}

Functional Markers:
- SCFA Levels: {functional_markers.get('scfa_levels', {})}
- Inflammation Markers: {functional_markers.get('inflammation_markers', {})}

Current Symptoms: {symptoms}
Current Diet: {diet}

Generate a comprehensive analysis including:
1. Clear interpretation of health_score (healthy vs non-healthy range)
2. Meaning of similarity_score regarding diabetes risk
3. Analysis of microbiome composition balance
4. Diversity assessment and implications
5. Role of under-represented species & risk implications
6. Connection between symptoms, diet, and microbiome data
7. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the data means for the user's health.
"""
        )
        return self.llm.generate(prompt, max_tokens=500)

