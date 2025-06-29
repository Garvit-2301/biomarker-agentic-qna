import json
from ..common.base import BaseAgent

class TranscriptomicsInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract transcriptomics-specific data
        gene_expression = report.get("gene_expression", {})
        differentially_expressed_genes = report.get("deg", {})
        pathway_enrichment = report.get("pathway_enrichment", {})
        transcription_factors = report.get("transcription_factors", {})
        rna_biomarkers = report.get("rna_biomarkers", {})
        regulatory_networks = report.get("regulatory_networks", {})
        
        prompt = (
f"""
You are a transcriptomics specialist analyzing gene expression data for user {user_id}.

TRANSCRIPTOMICS REPORT DATA:
Gene Expression Levels: {gene_expression}
Differentially Expressed Genes: {differentially_expressed_genes}
Pathway Enrichment: {pathway_enrichment}
Transcription Factors: {transcription_factors}
RNA Biomarkers: {rna_biomarkers}
Regulatory Networks: {regulatory_networks}

Generate a comprehensive transcriptomics analysis including:

1. GENE EXPRESSION ANALYSIS:
   - Key genes and their expression patterns
   - Upregulated vs downregulated genes
   - Biological significance of expression changes

2. DIFFERENTIALLY EXPRESSED GENES:
   - Most significant gene changes
   - Functional implications
   - Disease associations

3. PATHWAY ENRICHMENT:
   - Affected biological pathways
   - Metabolic pathway disruptions
   - Cellular process implications

4. TRANSCRIPTION FACTOR ANALYSIS:
   - Key transcription factors
   - Regulatory mechanisms
   - Gene regulation networks

5. RNA BIOMARKERS:
   - Diagnostic RNA markers
   - Prognostic indicators
   - Therapeutic targets

6. REGULATORY NETWORKS:
   - Gene regulatory networks
   - Network perturbations
   - Functional consequences

7. CLINICAL IMPLICATIONS:
   - Disease mechanisms
   - Therapeutic opportunities
   - Monitoring strategies

8. End with a single-sentence summary in **bold**.

Focus on actionable insights and explain what the transcriptomics data means for the user's health and potential interventions.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 