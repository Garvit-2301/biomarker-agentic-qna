import json
from typing import Dict, Any
from ..common.base import BaseAgent

class TranscriptomicsExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        term = context.get("term", "")
        
        # Extract transcriptomics-specific data for context
        gene_expression_data = report.get("gene_expression_data", {})
        differentially_expressed_genes = report.get("differentially_expressed_genes", {})
        pathway_analysis = report.get("pathway_analysis", {})
        
        prompt = (
f"""
You are a transcriptomics specialist explaining concepts for user {user_id}.

GENE EXPRESSION CONTEXT:
{json.dumps(gene_expression_data, indent=2)}

DIFFERENTIALLY EXPRESSED GENES:
{json.dumps(differentially_expressed_genes, indent=2)}

PATHWAY ANALYSIS:
{json.dumps(pathway_analysis, indent=2)}

TERM TO EXPLAIN: {term}

USER QUESTION: {user_query}

Provide a comprehensive explanation that includes:

1. DEFINITION:
   - Clear, simple definition of the term
   - What it measures or represents
   - Why it's important for gene expression analysis

2. SCIENTIFIC CONTEXT:
   - How it relates to gene expression
   - Biological mechanisms involved
   - Role in cellular processes

3. HEALTH IMPLICATIONS:
   - What healthy vs unhealthy patterns look like
   - How it affects overall health
   - Disease associations

4. PERSONAL RELEVANCE:
   - How this term relates to the user's gene expression data
   - What their specific values mean
   - Implications for their health

5. PRACTICAL UNDERSTANDING:
   - Simple analogies or examples
   - What changes in this value indicate
   - How it can be influenced

6. End with a single-sentence summary in **bold**.

Use clear, non-technical language and provide specific examples. Make the explanation relevant to the user's gene expression profile.
"""
        )
        return self.generate(prompt, max_tokens=600) 