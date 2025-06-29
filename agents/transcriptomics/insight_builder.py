import json
from typing import Dict, Any
from ..common.base import BaseAgent

class TranscriptomicsInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract transcriptomics-specific data for context
        gene_expression_data = report.get("gene_expression_data", {})
        differentially_expressed_genes = report.get("differentially_expressed_genes", {})
        pathway_analysis = report.get("pathway_analysis", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a transcriptomics specialist analyzing data for user {user_id}.

GENE EXPRESSION DATA:
{json.dumps(gene_expression_data, indent=2)}

DIFFERENTIALLY EXPRESSED GENES:
{json.dumps(differentially_expressed_genes, indent=2)}

PATHWAY ANALYSIS:
{json.dumps(pathway_analysis, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive transcriptomics insights including:

1. GENE EXPRESSION ANALYSIS:
   - Overall gene expression patterns
   - Key differentially expressed genes
   - Expression level variations
   - Tissue-specific patterns

2. DIFFERENTIAL EXPRESSION ASSESSMENT:
   - Upregulated vs downregulated genes
   - Statistical significance of changes
   - Biological relevance of changes
   - Functional implications

3. PATHWAY ANALYSIS:
   - Affected biological pathways
   - Metabolic pathway activity
   - Signaling pathway status
   - Regulatory network changes

4. HEALTH IMPLICATIONS:
   - Disease risk assessment
   - Metabolic health indicators
   - Inflammation markers
   - Organ function status

5. LIFESTYLE FACTORS:
   - How diet affects gene expression
   - Exercise and gene patterns
   - Stress impact on transcription
   - Environmental influences

6. ACTIONABLE INSIGHTS:
   - Specific gene targets
   - Intervention opportunities
   - Monitoring recommendations
   - Prevention strategies

Provide evidence-based insights that explain gene expression patterns in the context of overall health and wellness.
"""
        )
        return self.generate(prompt, max_tokens=600) 