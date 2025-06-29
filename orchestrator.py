from typing import Dict, Any
from utils.llm_factory import LLMFactory
from utils.user_data_loader import UserDataLoader
from agents.intent_classifier import IntentClassifierAgent
from agents.insight_builder import InsightBuilderAgent
from agents.recommendation import RecommendationAgent
from agents.compare import CompareAgent
from agents.explainer import ExplainerAgent

class AgentOrchestrator:
    def __init__(self, llm_client_type: str = "openai", **llm_kwargs) -> None:
        """
        Initialize the orchestrator with specified LLM client
        
        Args:
            llm_client_type: Type of LLM client ("openai" or "llama3")
            **llm_kwargs: Additional arguments for the LLM client
        """
        self.llm = LLMFactory.create_client(llm_client_type, **llm_kwargs)
        self.llm_client_type = llm_client_type
        self.user_loader = UserDataLoader()
        self.intent_classifier = IntentClassifierAgent(self.llm)
        self.agents: Dict[str, Any] = {
            "Insight": InsightBuilderAgent(self.llm),
            "Recommendation": RecommendationAgent(self.llm),
            "Compare": CompareAgent(self.llm),
            "Explain_Score": ExplainerAgent(self.llm),
        }

    def handle_user_query(self, user_id: str, user_query: str, *, 
                         demographics: Dict[str, Any] = None, 
                         baseline: Dict[str, Any] = None) -> str:
        """
        Handle query for a specific user by loading their data
        """
        # Load user's report data
        user_report = self.user_loader.load_user_report(user_id)
        if user_report is None:
            return f"Error: No data found for user {user_id}. Available users: {', '.join(self.user_loader.get_available_users())}"
        
        # Extract report data for context
        report_data = {
            "similarity_score": user_report.get("similarity_score"),
            "health_score": user_report.get("health_score"),
            "underrepresented_species": user_report.get("underrepresented_species", []),
            "microbiome_composition": user_report.get("microbiome_composition", {}),
            "diversity_scores": user_report.get("diversity_scores", {}),
            "functional_markers": user_report.get("functional_markers", {}),
            "symptoms": user_report.get("symptoms", {}),
            "diet": user_report.get("diet", {})
        }
        
        # Create context with user data
        ctx: Dict[str, Any] = {
            "report": report_data,
            "demographics": demographics or {},
            "baseline": baseline or {},
            "user_id": user_id,
            "full_user_data": user_report
        }
        
        # Handle "what is" queries
        if user_query.lower().startswith("what is"):
            ctx["term"] = user_query.split("what is", 1)[1].strip(" ?")
        
        # Classify intent and route to appropriate agent
        intent = self.intent_classifier.run(user_query, ctx)
        agent = self.agents.get(intent, self.agents['Insight'])
        return agent.run(user_query, ctx)

    def handle_query(self, user_query: str, *, report: Dict[str, Any] = None,
                     demographics: Dict[str, Any] = None, baseline: Dict[str, Any] = None) -> str:
        """
        Legacy method for backward compatibility
        """
        ctx: Dict[str, Any] = {"report": report or {}, "demographics": demographics or {}, "baseline": baseline or {}}
        if user_query.lower().startswith("what is"):
            ctx["term"] = user_query.split("what is", 1)[1].strip(" ?")
        intent = self.intent_classifier.run(user_query, ctx)
        agent = self.agents.get(intent, self.agents['Insight'])
        return agent.run(user_query, ctx)

    def get_available_users(self) -> list:
        """
        Get list of available users
        """
        return self.user_loader.get_available_users()
    
    def get_llm_info(self) -> Dict[str, Any]:
        """
        Get information about the current LLM client
        """
        return {
            "client_type": self.llm_client_type,
            "model": getattr(self.llm, 'model', 'unknown'),
            "connection_status": self.llm.test_connection() if hasattr(self.llm, 'test_connection') else "unknown"
        }

if __name__ == '__main__':
    # Sample demographics and baseline data
    demographics = {"age": 35, "sex": "F"}
    baseline = {"mean_health_score": 0.12}
    
    # Test with OpenAI client (default)
    print("Testing with OpenAI client:")
    qa_openai = AgentOrchestrator("openai", model="gpt-4")
    
    # Show available users
    print("Available users:", qa_openai.get_available_users())
    print("LLM Info:", qa_openai.get_llm_info())
    print("\n" + "="*50)
    
    # Test with user_001
    print("Testing with user_001:")
    response = qa_openai.handle_user_query("user_001", "Can you explain my gut health report?",
                                          demographics=demographics, baseline=baseline)
    print(response)
    
    print("\n" + "="*50)
    
    # Test with Llama3 client (if available)
    try:
        print("Testing with Llama3 client:")
        qa_llama = AgentOrchestrator("llama3")
        print("LLM Info:", qa_llama.get_llm_info())
        
        response = qa_llama.handle_user_query("user_005", "What recommendations do you have for me?",
                                             demographics=demographics, baseline=baseline)
        print(response)
    except Exception as e:
        print(f"Llama3 client not available: {e}")

