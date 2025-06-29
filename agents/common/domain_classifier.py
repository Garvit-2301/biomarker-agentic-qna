import json
from .base import BaseAgent

class DomainClassifierAgent(BaseAgent):
    DOMAINS = ["methylation", "metagenomics", "whole_exome", "proteomics", "transcriptomics", "whole_genome", "unknown"]

    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        prompt = (
            "Classify query into one of these domains: %s. " % self.DOMAINS +
            "Return JSON with keys 'domain' & 'confidence'.\n\n" +
            "Domain descriptions:\n" +
            "- methylation: DNA methylation patterns, epigenetic modifications, CpG sites\n" +
            "- metagenomics: Gut microbiome, bacterial composition, microbial diversity\n" +
            "- whole_exome: Protein-coding genes, exome sequencing, genetic variants\n" +
            "- proteomics: Protein expression, protein levels, protein biomarkers\n" +
            "- transcriptomics: Gene expression, RNA levels, transcriptome analysis\n" +
            "- whole_genome: Complete genome analysis, structural variants, genome-wide associations\n\n" +
            f"Query: '{user_query}'"
        )
        raw = self.llm.generate(prompt, max_tokens=120, temperature=0)
        try:
            data = json.loads(raw)
            domain = data.get("domain", "unknown")
        except Exception:
            domain = "unknown"
        return domain if domain in self.DOMAINS else "unknown" 