import json
from typing import Dict, Any
from ..common.base import BaseAgent

class WholeGenomeExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        term = context.get("term", "")
        
        # Extract whole genome-specific data for context
        genome_data = report.get("genome_data", {})
        snps = report.get("snps", {})
        structural_variants = report.get("structural_variants", {})
        ancestry = report.get("ancestry", {})
        
        prompt = (
f"""
You are a whole genome sequencing specialist explaining concepts for user {user_id}.

GENOME CONTEXT:
{json.dumps(genome_data, indent=2)}

SNPS:
{json.dumps(snps, indent=2)}

STRUCTURAL VARIANTS:
{json.dumps(structural_variants, indent=2)}

ANCESTRY:
{json.dumps(ancestry, indent=2)}

TERM TO EXPLAIN: {term}

USER QUESTION: {user_query}

Provide a comprehensive explanation that includes:

1. DEFINITION:
   - Clear, simple definition of the term
   - What it measures or represents
   - Why it's important for genome analysis

2. SCIENTIFIC CONTEXT:
   - How it relates to genome biology
   - Biological mechanisms involved
   - Role in health and disease

3. HEALTH IMPLICATIONS:
   - What healthy vs unhealthy patterns look like
   - How it affects overall health
   - Disease associations

4. PERSONAL RELEVANCE:
   - How this term relates to the user's genome data
   - What their specific values mean
   - Implications for their health

5. PRACTICAL UNDERSTANDING:
   - Simple analogies or examples
   - What changes in this value indicate
   - How it can be influenced

6. End with a single-sentence summary in **bold**.

Use clear, non-technical language and provide specific examples. Make the explanation relevant to the user's genome profile.
"""
        )
        return self.generate(prompt, max_tokens=600) 