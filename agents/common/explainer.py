from .base import BaseAgent

class ExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        term = context.get("term", user_query)
        domain = context.get("domain", "general")
        
        domain_contexts = {
            "methylation": "DNA methylation, epigenetic modifications, CpG sites, epigenetic age",
            "metagenomics": "gut microbiome, bacterial composition, microbial diversity, SCFA",
            "whole_exome": "genetic variants, exome sequencing, protein-coding genes, VUS",
            "proteomics": "protein expression, biomarkers, post-translational modifications",
            "transcriptomics": "gene expression, RNA levels, transcription factors, regulatory networks",
            "whole_genome": "genome sequencing, SNPs, structural variants, GWAS, ancestry"
        }
        
        domain_context = domain_contexts.get(domain, "biomarker analysis")
        
        prompt = (
f"""
You are a {domain} specialist explaining scientific terms in simple language.

Term to explain: '{term}'
Domain context: {domain_context}

Provide a clear, comprehensive explanation including:

1. DEFINITION:
   - What the term means in simple language
   - Scientific definition if helpful

2. BIOLOGICAL SIGNIFICANCE:
   - Why this term matters for health
   - How it relates to human biology

3. MEASUREMENT:
   - How it's typically measured or assessed
   - What the measurements mean

4. HEALTH IMPLICATIONS:
   - What healthy vs unhealthy ranges look like
   - Disease associations if relevant

5. PRACTICAL RELEVANCE:
   - How this affects daily health decisions
   - What people can do with this information

Use simple language and avoid jargon. Make it accessible to someone without a scientific background.
"""
        )
        return self.generate(prompt, max_tokens=400) 