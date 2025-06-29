import json
from ..common.base import BaseAgent

class MetagenomicsInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract metagenomics-specific data
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
You are a metagenomics specialist analyzing gut microbiome data for user {user_id}.

METAGENOMICS REPORT DATA:
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

Generate a comprehensive metagenomics analysis including:

1. MICROBIOME HEALTH ASSESSMENT:
   - Interpretation of health_score and diversity metrics
   - Balance of bacterial phyla
   - Overall microbiome health status

2. FUNCTIONAL ANALYSIS:
   - SCFA production capacity
   - Inflammation markers interpretation
   - Metabolic implications

3. SPECIES ANALYSIS:
   - Missing beneficial species
   - Overrepresented harmful species
   - Ecological relationships

4. DIET-MICROBIOME INTERACTIONS:
   - How current diet affects microbiome
   - Food-microbiome relationships
   - Dietary optimization opportunities

5. HEALTH IMPLICATIONS:
   - Disease risk assessment
   - Immune system implications
   - Metabolic health connections

6. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the metagenomics data means for the user's gut health and overall wellness.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 