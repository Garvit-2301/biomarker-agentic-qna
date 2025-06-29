import json
import logging
import os
from typing import Dict, Any, List
from datetime import datetime
from utils.mock_llm_client import MockLLMClient
from utils.prompt_manager import PromptManager
from utils.user_data_loader import UserDataLoader

class OfflineSummaryBuilder:
    """
    Offline agent that builds detailed summaries of each user's data
    and stores them in files for future reference.
    """
    
    def __init__(self, output_dir: str = "user_summaries"):
        """
        Initialize the offline summary builder.
        
        Args:
            output_dir: Directory to store user summaries
        """
        self.output_dir = output_dir
        self.prompt_manager = PromptManager()
        self.user_loader = UserDataLoader()
        self.llm_client = MockLLMClient(client_type="offline_summary")
        self.logger = self._setup_logger()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the offline summary builder."""
        logger = logging.getLogger("OfflineSummaryBuilder")
        logger.setLevel(logging.INFO)
        
        # Create handlers
        os.makedirs("testing_logs", exist_ok=True)
        file_handler = logging.FileHandler("testing_logs/offline_summary_builder.log")
        console_handler = logging.StreamHandler()
        
        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def generate_user_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive summary for a specific user across all domains.
        
        Args:
            user_id: User ID to generate summary for
            
        Returns:
            Dictionary containing summary data and metadata
        """
        self.logger.info(f"Generating comprehensive summary for user: {user_id}")
        
        summary_data = {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "domains": {},
            "overall_health_assessment": {},
            "cross_domain_insights": {},
            "recommendations": {},
            "metadata": {}
        }
        
        # Get available domains for this user
        available_domains = self.user_loader.get_available_domains(user_id)
        self.logger.info(f"Available domains for {user_id}: {available_domains}")
        
        # Generate domain-specific summaries
        for domain in available_domains:
            try:
                domain_summary = self._generate_domain_summary(user_id, domain)
                summary_data["domains"][domain] = domain_summary
                self.logger.info(f"Generated {domain} summary for {user_id}")
            except Exception as e:
                self.logger.error(f"Error generating {domain} summary for {user_id}: {e}")
                summary_data["domains"][domain] = {"error": str(e)}
        
        # Generate cross-domain insights
        try:
            cross_domain_insights = self._generate_cross_domain_insights(user_id, summary_data["domains"])
            summary_data["cross_domain_insights"] = cross_domain_insights
        except Exception as e:
            self.logger.error(f"Error generating cross-domain insights for {user_id}: {e}")
            summary_data["cross_domain_insights"] = {"error": str(e)}
        
        # Generate overall health assessment
        try:
            overall_assessment = self._generate_overall_assessment(user_id, summary_data["domains"])
            summary_data["overall_health_assessment"] = overall_assessment
        except Exception as e:
            self.logger.error(f"Error generating overall assessment for {user_id}: {e}")
            summary_data["overall_health_assessment"] = {"error": str(e)}
        
        # Generate comprehensive recommendations
        try:
            recommendations = self._generate_comprehensive_recommendations(user_id, summary_data)
            summary_data["recommendations"] = recommendations
        except Exception as e:
            self.logger.error(f"Error generating recommendations for {user_id}: {e}")
            summary_data["recommendations"] = {"error": str(e)}
        
        # Add metadata
        summary_data["metadata"] = {
            "total_domains": len(available_domains),
            "domains_processed": list(summary_data["domains"].keys()),
            "processing_time": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        return summary_data
    
    def _generate_domain_summary(self, user_id: str, domain: str) -> Dict[str, Any]:
        """Generate summary for a specific domain."""
        # Load user data for the domain
        user_data = self.user_loader.load_user_report(user_id, domain)
        if not user_data:
            return {"error": f"No data available for {domain}"}
        
        # Get domain-specific prompt
        try:
            agent_prompt = self.prompt_manager.get_agent_prompt(domain, "summary")
            user_template = agent_prompt.get("user_template", "")
            
            # Map domain to expected variable name
            domain_variable_map = {
                "methylation": "methylation_data",
                "metagenomics": "metagenomics_data", 
                "proteomics": "proteomics_data",
                "transcriptomics": "transcriptomics_data",
                "whole_exome": "whole_exome_data",
                "whole_genome": "whole_genome_data"
            }
            
            data_variable = domain_variable_map.get(domain, f"{domain}_data")
            
            # Format the prompt
            formatted_prompt = user_template.format(
                user_id=user_id,
                user_context=f"Comprehensive {domain} analysis for {user_id}",
                **{data_variable: json.dumps(user_data, indent=2)}
            )
            
            # Generate response
            response = self.llm_client.generate_response(
                prompt=formatted_prompt,
                agent_type="summary",
                domain=domain,
                user_id=user_id
            )
            
            return {
                "summary": response["choices"][0]["message"]["content"],
                "data_snapshot": user_data,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error generating summary: {str(e)}"}
    
    def _generate_cross_domain_insights(self, user_id: str, domain_summaries: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights that span multiple domains."""
        prompt = f"""
You are a multi-domain biomarker specialist analyzing cross-domain insights for user {user_id}.

DOMAIN SUMMARIES:
{json.dumps(domain_summaries, indent=2)}

Generate comprehensive cross-domain insights including:

1. INTERCONNECTIONS:
   - How different biomarker domains relate to each other
   - Synergistic effects between domains
   - Potential conflicts or contradictions

2. HOLISTIC HEALTH PICTURE:
   - Overall health status across all domains
   - Strengths and weaknesses identified
   - Areas of concern that span multiple domains

3. INTEGRATED RISK ASSESSMENT:
   - Combined risk factors across domains
   - Protective factors that benefit multiple systems
   - Priority areas for intervention

4. CROSS-DOMAIN RECOMMENDATIONS:
   - Interventions that benefit multiple domains
   - Lifestyle changes with broad impact
   - Monitoring strategies for multiple biomarkers

5. CLINICAL RELEVANCE:
   - How findings from different domains support each other
   - Diagnostic implications of cross-domain patterns
   - Therapeutic opportunities

Provide actionable insights that integrate information from all available domains.
"""
        
        response = self.llm_client.generate_response(
            prompt=prompt,
            agent_type="analysis",
            domain="cross_domain",
            user_id=user_id
        )
        
        return {
            "insights": response["choices"][0]["message"]["content"],
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_overall_assessment(self, user_id: str, domain_summaries: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall health assessment."""
        prompt = f"""
You are a comprehensive health specialist providing an overall assessment for user {user_id}.

DOMAIN SUMMARIES:
{json.dumps(domain_summaries, indent=2)}

Generate an overall health assessment including:

1. EXECUTIVE SUMMARY:
   - Overall health status (excellent/good/fair/poor)
   - Key strengths and areas of concern
   - Priority health focus areas

2. HEALTH SCORE BREAKDOWN:
   - Cardiovascular health indicators
   - Metabolic health indicators
   - Immune system indicators
   - Genetic risk factors
   - Epigenetic health indicators

3. LIFESTYLE IMPACT ASSESSMENT:
   - How current lifestyle affects biomarkers
   - Positive lifestyle factors identified
   - Areas for lifestyle improvement

4. PREVENTIVE HEALTH PRIORITIES:
   - Primary prevention strategies
   - Secondary prevention needs
   - Monitoring recommendations

5. CLINICAL CONSIDERATIONS:
   - Specialist referrals if needed
   - Medical monitoring requirements
   - Integration with existing care

Provide a comprehensive, patient-friendly assessment that integrates all available biomarker data.
"""
        
        response = self.llm_client.generate_response(
            prompt=prompt,
            agent_type="analysis",
            domain="overall",
            user_id=user_id
        )
        
        return {
            "assessment": response["choices"][0]["message"]["content"],
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_comprehensive_recommendations(self, user_id: str, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive recommendations based on all domain data."""
        prompt = f"""
You are a comprehensive health specialist providing personalized recommendations for user {user_id}.

COMPREHENSIVE SUMMARY DATA:
{json.dumps(summary_data, indent=2)}

Generate comprehensive, personalized recommendations including:

1. NUTRITION RECOMMENDATIONS:
   - Dietary changes based on all biomarker data
   - Specific foods to include/avoid
   - Supplementation recommendations
   - Meal timing and frequency

2. LIFESTYLE INTERVENTIONS:
   - Exercise recommendations
   - Stress management strategies
   - Sleep optimization
   - Environmental factors

3. MONITORING STRATEGIES:
   - Follow-up testing recommendations
   - Timeline for reassessment
   - Key metrics to track
   - Progress indicators

4. CLINICAL ACTIONS:
   - Specialist referrals if needed
   - Medical monitoring requirements
   - Integration with existing treatments
   - Emergency considerations

5. IMPLEMENTATION PLAN:
   - Priority order for changes
   - Realistic timeline for implementation
   - Support resources needed
   - Success metrics

Provide actionable, evidence-based recommendations that integrate all available biomarker information.
"""
        
        response = self.llm_client.generate_response(
            prompt=prompt,
            agent_type="recommendation",
            domain="comprehensive",
            user_id=user_id
        )
        
        return {
            "recommendations": response["choices"][0]["message"]["content"],
            "generated_at": datetime.now().isoformat()
        }
    
    def save_user_summary(self, user_id: str, summary_data: Dict[str, Any]) -> str:
        """
        Save the user summary to a file.
        
        Args:
            user_id: User ID
            summary_data: Summary data to save
            
        Returns:
            Path to the saved file
        """
        filename = f"{user_id}_comprehensive_summary.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        self.logger.info(f"Saved comprehensive summary for {user_id} to {filepath}")
        return filepath
    
    def process_all_users(self) -> Dict[str, Any]:
        """
        Process all available users and generate comprehensive summaries.
        
        Returns:
            Dictionary with processing results
        """
        self.logger.info("Starting comprehensive summary generation for all users")
        
        available_users = self.user_loader.get_available_users()
        results = {
            "total_users": len(available_users),
            "processed_users": [],
            "failed_users": [],
            "summary_files": [],
            "processing_time": datetime.now().isoformat()
        }
        
        for user_id in available_users:
            try:
                self.logger.info(f"Processing user: {user_id}")
                
                # Generate summary
                summary_data = self.generate_user_summary(user_id)
                
                # Save summary
                filepath = self.save_user_summary(user_id, summary_data)
                
                results["processed_users"].append(user_id)
                results["summary_files"].append(filepath)
                
                self.logger.info(f"Successfully processed {user_id}")
                
            except Exception as e:
                self.logger.error(f"Failed to process {user_id}: {e}")
                results["failed_users"].append({"user_id": user_id, "error": str(e)})
        
        # Save processing report
        report_file = os.path.join(self.output_dir, "processing_report.json")
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Processing complete. Report saved to {report_file}")
        return results
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get statistics about generated summaries."""
        if not os.path.exists(self.output_dir):
            return {"error": "Output directory does not exist"}
        
        summary_files = [f for f in os.listdir(self.output_dir) if f.endswith('_comprehensive_summary.json')]
        
        stats = {
            "total_summaries": len(summary_files),
            "summary_files": summary_files,
            "output_directory": self.output_dir,
            "last_updated": datetime.now().isoformat()
        }
        
        return stats 