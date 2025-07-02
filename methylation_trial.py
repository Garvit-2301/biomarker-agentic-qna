import json
import dspy
import os
import sys
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

lm = dspy.LM('meta-llama/Llama-3-8b-chat-hf', api_key="tgp_v1_xaeOuQ7mmffFW8s-eyDp1RB3HbUSRyU-XWzhsf2nino", api_base="https://api.together.xyz/",
    custom_llm_provider="together_ai")
dspy.configure(lm=lm, temperature=0.7)

class Methylationqna(dspy.Signature):
    """Answers questions about methylation analysis data based on the reports """
    data = dspy.InputField(desc="Methylation Report Data")
    ques = dspy.InputField(desc="User Question about analysis")
    ans = dspy.OutputField(desc="Answer based on the report data")

class MethylationDataProcessor:
    """Process and format methylation data for the agent."""
    
    @staticmethod
    def format_methylation_data(json_data: Dict, report_text: str) -> str:
        
        context = f"""
METHYLATION ANALYSIS REPORT

Basic Information:
- User ID: {json_data.get('user_id', 'N/A')}
- Report Date: {json_data.get('report_date', 'N/A')}
- Domain: {json_data.get('domain', 'N/A')}
- Overall Methylation Score: {json_data.get('methylation_score', 'N/A')}

CpG Sites Analysis:
- Total Sites Analyzed: {json_data.get('cpg_sites', {}).get('total_analyzed', 'N/A'):,}
- Methylated Sites: {json_data.get('cpg_sites', {}).get('methylated_sites', 'N/A'):,}
- Unmethylated Sites: {json_data.get('cpg_sites', {}).get('unmethylated_sites', 'N/A'):,}

Key Regions Methylation:
- Promoter Regions: {json_data.get('cpg_sites', {}).get('key_regions', {}).get('promoter_regions', 'N/A')}
- Gene Bodies: {json_data.get('cpg_sites', {}).get('key_regions', {}).get('gene_bodies', 'N/A')}
- Enhancer Regions: {json_data.get('cpg_sites', {}).get('key_regions', {}).get('enhancer_regions', 'N/A')}
- CpG Islands: {json_data.get('cpg_sites', {}).get('key_regions', {}).get('cpg_islands', 'N/A')}

Epigenetic Age Analysis:
- Chronological Age: {json_data.get('epigenetic_age', {}).get('chronological_age', 'N/A')} years
- Biological Age: {json_data.get('epigenetic_age', {}).get('biological_age', 'N/A')} years
- Age Acceleration: {json_data.get('epigenetic_age', {}).get('age_acceleration', 'N/A')} years
- Age Percentile: {json_data.get('epigenetic_age', {}).get('age_percentile', 'N/A')}th percentile

Disease Risk Assessment:
- Cancer Risk: {json_data.get('methylation_patterns', {}).get('disease_associated', {}).get('cancer_risk', 'N/A')}
- Cardiovascular Risk: {json_data.get('methylation_patterns', {}).get('disease_associated', {}).get('cardiovascular_risk', 'N/A')}
- Diabetes Risk: {json_data.get('methylation_patterns', {}).get('disease_associated', {}).get('diabetes_risk', 'N/A')}

Health Markers:
Inflammation Markers:
- IL6 Methylation: {json_data.get('health_implications', {}).get('inflammation_markers', {}).get('il6_methylation', 'N/A')}
- TNF Alpha Methylation: {json_data.get('health_implications', {}).get('inflammation_markers', {}).get('tnf_alpha_methylation', 'N/A')}
- CRP Methylation: {json_data.get('health_implications', {}).get('inflammation_markers', {}).get('crp_methylation', 'N/A')}

Metabolic Markers:
- Insulin Methylation: {json_data.get('health_implications', {}).get('metabolic_markers', {}).get('insulin_methylation', 'N/A')}
- Leptin Methylation: {json_data.get('health_implications', {}).get('metabolic_markers', {}).get('leptin_methylation', 'N/A')}
- Adiponectin Methylation: {json_data.get('health_implications', {}).get('metabolic_markers', {}).get('adiponectin_methylation', 'N/A')}

Stress Response:
- Cortisol Methylation: {json_data.get('health_implications', {}).get('stress_response', {}).get('cortisol_methylation', 'N/A')}
- BDNF Methylation: {json_data.get('health_implications', {}).get('stress_response', {}).get('bdnf_methylation', 'N/A')}
- NR3C1 Methylation: {json_data.get('health_implications', {}).get('stress_response', {}).get('nr3c1_methylation', 'N/A')}

Genetic Profile Report:
{report_text}
"""
        return context

class MethylationAgent(dspy.Module):
    """Agent for Report Analysis """

    def __init__(self, json_file_path: str = None, report_file_path: str = None):
        self.qnagenerator = dspy.ChainOfThought(Methylationqna)
        self.data_processor = MethylationDataProcessor()
        self.current_context = None

        # Load data if paths are provided
        if json_file_path and report_file_path:
            self.load_data_from_files(json_file_path, report_file_path)

    def load_data_from_files(self, json_file_path: str, report_file_path: str):
        """Load data from JSON files"""
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Load report text - first read the content
        with open(report_file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # If file is empty or whitespace only, use default text
        if not content:
            report_text = "No report data available"
        else:
            # Try to parse as JSON, if it fails treat as plain text
            if content.startswith('{') or content.startswith('['):
                report_text = json.loads(content)
            else:
                report_text = content

        # Load the formatted data
        self.load_data(json_data, report_text)
        print("Data loaded successfully!")

    def load_data(self, json_data: Dict, report_text: str):
        """Load formatted data into the agent"""
        self.current_context = self.data_processor.format_methylation_data(json_data, report_text)

    def ask_ques(self, question: str) -> str:
        """Ask a question about the loaded data"""
        if not self.current_context:
            return "No data loaded. Please load methylation data first using load_data_from_files()."
        
        result = self.qnagenerator(
            data=self.current_context,
            ques=question
        )
        return result.ans
    
    def get_summary(self) -> str:
        """Get a summary of the methylation report"""
        summary_ques = "Please provide a detailed summary of the methylation report"
        return self.ask_ques(summary_ques)
    
    def get_recommendations(self) -> str:
        """Get health recommendations based on the report"""
        rec_ques = "Based on the report, what specific health recommendations would you suggest?"
        return self.ask_ques(rec_ques)

def main():
    # File paths - update these to match your actual file locations
    json_file = r"C:\Users\sahni\biomarker-agentic-qna\user_data\methylation\user_001_report.txt"
    report_file = r"C:\Users\sahni\biomarker-agentic-qna\user_data\methylation\test_user_001_report.txt"
    
    # Initialize agent
    agent = MethylationAgent()
    
    # Try to load data
    agent.load_data_from_files(json_file, report_file)
    
    print("Methylation Analysis Agent")
    print("Commands: 'summary', 'recommendations', or ask any question about the data")
    print("Type 'bye' to exit\n")

    while True:
        user_question = input("Enter your question: ").strip()

        if user_question.lower() == 'bye':
            print("Thank you, Bye!")
            break
        elif user_question.lower() == 'summary':
            print("\n" + agent.get_summary() + "\n")
        elif user_question.lower() == 'recommendations':
            print("\n" + agent.get_recommendations() + "\n")
        elif user_question:
            print("\n" + agent.ask_ques(user_question) + "\n")
        else:
            print("Please enter a question or command.")

if __name__ == "__main__":
    main()