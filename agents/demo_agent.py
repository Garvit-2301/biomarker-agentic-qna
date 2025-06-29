import json
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
from utils.mock_llm_client import MockLLMClient
from utils.prompt_manager import PromptManager

class DemoAgent:
    """
    Demo agent for testing the agentic workflow without making actual LLM calls.
    Uses mock LLM client and prompt manager to simulate the complete workflow.
    """
    
    def __init__(self, domain: str, agent_type: str, user_id: str = "user_001"):
        """
        Initialize the demo agent.
        
        Args:
            domain: Domain name (e.g., 'methylation', 'metagenomics', etc.)
            agent_type: Type of agent ('analysis', 'summary', 'recommendation')
            user_id: User ID for the analysis
        """
        self.domain = domain
        self.agent_type = agent_type
        self.user_id = user_id
        self.prompt_manager = PromptManager()
        self.llm_client = MockLLMClient(client_type="demo")
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the demo agent."""
        logger = logging.getLogger(f"demo_agent_{self.domain}_{self.agent_type}")
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Create testing_logs directory structure
        log_dir = f"testing_logs/{self.domain}"
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler
        file_handler = logging.FileHandler(f"{log_dir}/{self.agent_type}_agent.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def load_user_data(self) -> str:
        """
        Load user data for the specific domain.
        
        Returns:
            User data as string
        """
        try:
            data_file = f"user_data/{self.domain}/{self.user_id}_report.txt"
            with open(data_file, 'r') as f:
                data = f.read()
            self.logger.info(f"Successfully loaded user data from {data_file}")
            return data
        except FileNotFoundError:
            # Generate mock data if file doesn't exist
            mock_data = self._generate_mock_user_data()
            self.logger.warning(f"User data file not found, using mock data for {self.domain}")
            return mock_data
    
    def _generate_mock_user_data(self) -> str:
        """Generate mock user data for testing."""
        mock_data_templates = {
            "methylation": """
METHYLATION ANALYSIS REPORT - User: {user_id}
Date: {date}

Methylation Profile:
- MTHFR C677T: Heterozygous (CT)
- COMT V158M: Homozygous (GG)
- BDNF Val66Met: Heterozygous (AG)
- MAO-A: Normal methylation pattern
- DNMT1: Slightly elevated methylation

Key Findings:
- Moderate methylation efficiency
- Normal folate metabolism
- Slightly elevated stress response methylation
- Good detoxification methylation patterns

Recommendations:
- Consider B-vitamin supplementation
- Monitor stress levels
- Maintain healthy lifestyle habits
""",
            "metagenomics": """
GUT MICROBIOME ANALYSIS REPORT - User: {user_id}
Date: {date}

Microbiome Diversity:
- Shannon Diversity Index: 3.8 (Good)
- Simpson Diversity: 0.85 (Good)
- Chao1 Richness: 245 species

Key Species Abundance:
- Bifidobacterium: 12.5% (Normal)
- Lactobacillus: 8.3% (Normal)
- Akkermansia muciniphila: 2.1% (Low)
- Faecalibacterium prausnitzii: 15.2% (Good)
- Bacteroides: 18.7% (Normal)

Dysbiosis Indicators:
- Slight reduction in beneficial bacteria
- Normal pathogen levels
- Good short-chain fatty acid producers

Recommendations:
- Increase fiber intake
- Consider prebiotic supplementation
- Maintain regular exercise routine
""",
            "proteomics": """
PROTEOMIC PROFILE REPORT - User: {user_id}
Date: {date}

Protein Expression Analysis:
- Total proteins identified: 1,247
- Differentially expressed: 23 proteins
- Pathway enrichment: 5 significant pathways

Key Biomarkers:
- CRP: 2.1 mg/L (Normal)
- IL-6: 3.2 pg/mL (Normal)
- TNF-alpha: 2.8 pg/mL (Normal)
- Adiponectin: 8.5 μg/mL (Good)
- Leptin: 12.3 ng/mL (Normal)

Metabolic Pathways:
- Glucose metabolism: Normal
- Lipid metabolism: Normal
- Inflammatory response: Normal
- Stress response: Slightly elevated

Clinical Relevance:
- No significant inflammatory markers
- Good metabolic health indicators
- Normal stress response patterns
""",
            "transcriptomics": """
TRANSCRIPTOMIC ANALYSIS REPORT - User: {user_id}
Date: {date}

Gene Expression Profile:
- Total genes analyzed: 20,847
- Differentially expressed: 156 genes
- Upregulated: 89 genes
- Downregulated: 67 genes

Key Pathways:
- Immune response: 23 genes
- Stress response: 18 genes
- Metabolism: 34 genes
- Cell signaling: 27 genes

Regulatory Networks:
- Transcription factors: 12 active
- MicroRNAs: 8 differentially expressed
- Long non-coding RNAs: 15 identified

Summary:
- Normal transcriptional activity
- Stress response genes activated
- Good immune system function
- Stable metabolic gene expression
""",
            "whole_exome": """
WHOLE EXOME SEQUENCING REPORT - User: {user_id}
Date: {date}

Variant Analysis:
- Total variants: 3,247
- Rare variants: 156
- Novel variants: 23
- Pathogenic variants: 2

Key Findings:
- MTHFR C677T: Heterozygous (CT)
- COMT V158M: Homozygous (GG)
- APOE: E3/E3 (Normal)
- BRCA1/2: No pathogenic variants

Carrier Status:
- Cystic fibrosis: Carrier (1 variant)
- Sickle cell anemia: Not carrier
- Tay-Sachs: Not carrier

Pharmacogenomics:
- CYP2D6: Normal metabolizer
- CYP2C19: Normal metabolizer
- CYP3A4: Normal metabolizer

Clinical Implications:
- Normal genetic risk profile
- No actionable genetic findings
- Standard medication metabolism
""",
            "whole_genome": """
WHOLE GENOME ANALYSIS REPORT - User: {user_id}
Date: {date}

Genomic Analysis:
- Total variants: 4.2 million
- Rare variants: 2,847
- Structural variations: 156
- Copy number variations: 23

Key Findings:
- No significant structural variations
- Normal copy number profile
- Good genomic stability
- Population-appropriate diversity

Regulatory Elements:
- Enhancers: 45,234 identified
- Promoters: 23,456 active
- Insulators: 12,345 mapped
- Non-coding RNAs: 8,234 expressed

Population Genetics:
- Ancestry: Mixed European/Asian
- Population-specific variants: 234
- Common variants: 3.8 million
- Rare variants: 2,847

Comprehensive Assessment:
- Overall genomic health: Good
- No significant genetic risks
- Normal population diversity
- Stable genomic structure
"""
        }
        
        template = mock_data_templates.get(self.domain, "Mock data for {domain} domain")
        return template.format(
            user_id=self.user_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            domain=self.domain
        )
    
    def get_prompt(self) -> str:
        """
        Get the formatted prompt for the agent.
        
        Returns:
            Formatted prompt string
        """
        try:
            agent_prompt = self.prompt_manager.get_agent_prompt(self.domain, self.agent_type)
            user_data = self.load_user_data()
            
            # Map domain to expected variable name in prompt templates
            domain_variable_map = {
                "methylation": "methylation_data",
                "metagenomics": "metagenomics_data", 
                "proteomics": "proteomics_data",
                "transcriptomics": "transcriptomics_data",
                "whole_exome": "whole_exome_data",
                "whole_genome": "whole_genome_data"
            }
            
            # Get the correct variable name for this domain
            data_variable = domain_variable_map.get(self.domain, "user_data")
            
            # Create the formatting arguments
            format_args = {
                "user_id": self.user_id,
                "user_context": f"User {self.user_id} from {self.domain} domain",
                "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                data_variable: user_data  # Use the domain-specific variable name
            }
            
            # Format the prompt with user data
            formatted_prompt = self.prompt_manager.format_prompt(
                agent_prompt["prompt"]["user_template"],
                **format_args
            )
            
            self.logger.info(f"Successfully formatted prompt for {self.agent_type} agent in {self.domain} domain")
            return formatted_prompt
            
        except Exception as e:
            self.logger.error(f"Error formatting prompt: {e}")
            return f"Error: Could not format prompt for {self.agent_type} agent in {self.domain} domain"
    
    def process(self) -> Dict[str, Any]:
        """
        Process the user query using the demo agent.
        
        Returns:
            Dictionary containing the agent's response and metadata
        """
        start_time = datetime.now()
        self.logger.info(f"Starting {self.agent_type} agent processing for {self.domain} domain")
        
        try:
            # Get formatted prompt
            prompt = self.get_prompt()
            
            # Generate response using mock LLM client
            response = self.llm_client.generate_response(
                prompt=prompt,
                agent_type=self.agent_type,
                domain=self.domain,
                user_id=self.user_id
            )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare result
            result = {
                "success": True,
                "agent_type": self.agent_type,
                "domain": self.domain,
                "user_id": self.user_id,
                "processing_time": processing_time,
                "prompt_length": len(prompt),
                "response_length": len(response["choices"][0]["message"]["content"]),
                "response": response["choices"][0]["message"]["content"],
                "metadata": {
                    "model": response["model"],
                    "usage": response["usage"],
                    "mock_data": response.get("mock_data", {})
                }
            }
            
            self.logger.info(f"Successfully processed {self.agent_type} agent for {self.domain} domain")
            self.logger.info(f"Processing time: {processing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error processing {self.agent_type} agent for {self.domain} domain: {e}")
            
            return {
                "success": False,
                "agent_type": self.agent_type,
                "domain": self.domain,
                "user_id": self.user_id,
                "processing_time": processing_time,
                "error": str(e),
                "response": f"Error occurred during processing: {e}"
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the agent's performance."""
        llm_stats = self.llm_client.get_usage_stats()
        return {
            "agent_type": self.agent_type,
            "domain": self.domain,
            "user_id": self.user_id,
            "llm_calls": llm_stats["total_calls"],
            "success_rate": llm_stats["success_rate"],
            "average_response_time": llm_stats["average_response_time"]
        } 