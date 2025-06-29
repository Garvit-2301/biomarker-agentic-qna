import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class PromptManager:
    """
    Manages prompts for different domains and agents in the biomarker analysis system.
    Loads prompts from JSON files and provides easy access to prompt templates.
    """
    
    def __init__(self, prompts_dir: str = "agents"):
        """
        Initialize the prompt manager.
        
        Args:
            prompts_dir: Directory containing the prompts JSON files
        """
        self.prompts_dir = Path(prompts_dir)
        self._prompts_cache: Dict[str, Dict[str, Any]] = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self) -> None:
        """Load all prompt files from the prompts directory."""
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found: {self.prompts_dir}")
        
        # Load common prompts first
        common_prompts_file = self.prompts_dir / "common" / "prompts.json"
        if common_prompts_file.exists():
            with open(common_prompts_file, 'r') as f:
                self._prompts_cache["common"] = json.load(f)
        
        # Load domain-specific prompts
        for domain_dir in self.prompts_dir.iterdir():
            if domain_dir.is_dir() and domain_dir.name != "common":
                prompts_file = domain_dir / "prompts.json"
                if prompts_file.exists():
                    with open(prompts_file, 'r') as f:
                        self._prompts_cache[domain_dir.name] = json.load(f)
    
    def get_domain_prompts(self, domain: str) -> Dict[str, Any]:
        """
        Get all prompts for a specific domain.
        
        Args:
            domain: Domain name (e.g., 'methylation', 'metagenomics', etc.)
            
        Returns:
            Dictionary containing all prompts for the domain
        """
        if domain not in self._prompts_cache:
            raise ValueError(f"Domain '{domain}' not found. Available domains: {list(self._prompts_cache.keys())}")
        
        return self._prompts_cache[domain]
    
    def get_agent_prompt(self, domain: str, agent_type: str) -> Dict[str, Any]:
        """
        Get prompt for a specific agent in a domain.
        
        Args:
            domain: Domain name
            agent_type: Agent type ('analysis', 'summary', 'recommendation', etc.)
            
        Returns:
            Dictionary containing the agent's prompt configuration
        """
        domain_prompts = self.get_domain_prompts(domain)
        
        if "agents" not in domain_prompts:
            raise ValueError(f"No agents found in domain '{domain}'")
        
        if agent_type not in domain_prompts["agents"]:
            raise ValueError(f"Agent type '{agent_type}' not found in domain '{domain}'. Available agents: {list(domain_prompts['agents'].keys())}")
        
        return domain_prompts["agents"][agent_type]
    
    def get_common_prompt(self, prompt_type: str) -> str:
        """
        Get a common prompt template.
        
        Args:
            prompt_type: Type of common prompt ('explain_term', 'compare_population', etc.)
            
        Returns:
            Prompt template string
        """
        if "common" not in self._prompts_cache:
            raise ValueError("Common prompts not found")
        
        common_prompts = self._prompts_cache["common"]
        
        if "common_prompts" not in common_prompts:
            raise ValueError("No common prompts found")
        
        if prompt_type not in common_prompts["common_prompts"]:
            raise ValueError(f"Common prompt type '{prompt_type}' not found. Available types: {list(common_prompts['common_prompts'].keys())}")
        
        return common_prompts["common_prompts"][prompt_type]["prompt"]
    
    def get_common_agent_prompt(self, agent_type: str) -> Dict[str, Any]:
        """
        Get prompt for a common agent.
        
        Args:
            agent_type: Common agent type ('intent_classifier', 'domain_classifier', 'compare', 'explainer')
            
        Returns:
            Dictionary containing the agent's prompt configuration
        """
        return self.get_agent_prompt("common", agent_type)
    
    def format_prompt(self, prompt_template: str, **kwargs) -> str:
        """
        Format a prompt template with provided arguments.
        
        Args:
            prompt_template: The prompt template string
            **kwargs: Arguments to format into the template
            
        Returns:
            Formatted prompt string
        """
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required argument for prompt formatting: {e}")
    
    def get_available_domains(self) -> list:
        """Get list of available domains."""
        return list(self._prompts_cache.keys())
    
    def get_available_agents(self, domain: str) -> list:
        """Get list of available agents for a domain."""
        domain_prompts = self.get_domain_prompts(domain)
        if "agents" not in domain_prompts:
            return []
        return list(domain_prompts["agents"].keys())
    
    def get_prompt_parameters(self, domain: str, agent_type: str) -> Dict[str, Any]:
        """
        Get the LLM parameters for a specific agent.
        
        Args:
            domain: Domain name
            agent_type: Agent type
            
        Returns:
            Dictionary containing LLM parameters (max_tokens, temperature, etc.)
        """
        agent_prompt = self.get_agent_prompt(domain, agent_type)
        return agent_prompt.get("prompt", {}).get("parameters", {})
    
    def reload_prompts(self) -> None:
        """Reload all prompts from files (useful for development)."""
        self._prompts_cache.clear()
        self._load_all_prompts()

# Example usage and testing
if __name__ == "__main__":
    # Initialize prompt manager
    prompt_manager = PromptManager()
    
    # Print available domains
    print("Available domains:", prompt_manager.get_available_domains())
    
    # Test getting methylation analysis prompt
    try:
        methylation_analysis = prompt_manager.get_agent_prompt("methylation", "analysis")
        print(f"Methylation analysis agent: {methylation_analysis['name']}")
        print(f"Description: {methylation_analysis['description']}")
        
        # Test formatting a prompt
        formatted_prompt = prompt_manager.format_prompt(
            methylation_analysis["prompt"]["user_template"],
            user_id="user_001",
            methylation_data="Sample methylation data...",
            user_context="Sample context..."
        )
        print(f"Formatted prompt length: {len(formatted_prompt)} characters")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test common prompts
    try:
        explain_prompt = prompt_manager.get_common_prompt("explain_term")
        print(f"Explain term prompt: {explain_prompt[:100]}...")
        
    except Exception as e:
        print(f"Error: {e}") 