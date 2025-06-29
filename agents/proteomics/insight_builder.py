import json
from ..common.base import BaseAgent

class ProteomicsInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract proteomics-specific data
        protein_expression = report.get("protein_expression", {})
        biomarker_levels = report.get("biomarker_levels", {})
        protein_pathways = report.get("protein_pathways", {})
        post_translational_modifications = report.get("ptm", {})
        protein_interactions = report.get("protein_interactions", {})
        disease_associations = report.get("disease_associations", {})
        
        prompt = (
f"""
You are a proteomics specialist analyzing protein expression data for user {user_id}.

PROTEOMICS REPORT DATA:
Protein Expression Levels: {protein_expression}
Biomarker Levels: {biomarker_levels}
Protein Pathways: {protein_pathways}
Post-Translational Modifications: {post_translational_modifications}
Protein Interactions: {protein_interactions}
Disease Associations: {disease_associations}

Generate a comprehensive proteomics analysis including:

1. PROTEIN EXPRESSION ANALYSIS:
   - Key proteins and their expression levels
   - Upregulated vs downregulated proteins
   - Biological significance of expression changes

2. BIOMARKER INTERPRETATION:
   - Clinical biomarker levels
   - Disease risk indicators
   - Health status markers

3. PATHWAY ANALYSIS:
   - Affected biological pathways
   - Metabolic implications
   - Cellular process disruptions

4. POST-TRANSLATIONAL MODIFICATIONS:
   - Protein modifications and their significance
   - Functional implications
   - Regulatory effects

5. PROTEIN INTERACTION NETWORKS:
   - Protein-protein interactions
   - Complex formation
   - Network perturbations

6. DISEASE ASSOCIATIONS:
   - Disease-related protein changes
   - Risk assessment
   - Prognostic implications

7. CLINICAL RELEVANCE:
   - Diagnostic potential
   - Therapeutic targets
   - Monitoring recommendations

8. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the proteomics data means for the user's health and potential interventions.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 