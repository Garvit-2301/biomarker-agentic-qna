#!/usr/bin/env python3
"""
Comprehensive testing script for the agentic workflow.
Tests all agents and prompts across all domains without making actual LLM calls.
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

from utils.prompt_manager import PromptManager
from agents.demo_agent import DemoAgent

class AgenticWorkflowTester:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.test_results = {}
        self.setup_logging()
        
    def setup_logging(self):
        os.makedirs("testing_logs", exist_ok=True)
        
        self.logger = logging.getLogger("agentic_workflow_tester")
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        file_handler = logging.FileHandler("testing_logs/test_execution.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        domains = self.prompt_manager.get_available_domains()
        for domain in domains:
            if domain != "common":
                os.makedirs(f"testing_logs/{domain}", exist_ok=True)
    
    def test_prompt_loading(self):
        self.logger.info("=" * 60)
        self.logger.info("TESTING PROMPT LOADING")
        self.logger.info("=" * 60)
        
        results = {"passed": 0, "failed": 0, "details": {}}
        domains = self.prompt_manager.get_available_domains()
        
        for domain in domains:
            self.logger.info(f"\nTesting prompt loading for domain: {domain}")
            domain_results = {"passed": 0, "failed": 0, "errors": []}
            
            try:
                domain_prompts = self.prompt_manager.get_domain_prompts(domain)
                self.logger.info(f"✓ Successfully loaded prompts for {domain}")
                domain_results["passed"] += 1
                
                if domain != "common":
                    agents = self.prompt_manager.get_available_agents(domain)
                    self.logger.info(f"✓ Found {len(agents)} agents in {domain}: {agents}")
                    domain_results["passed"] += 1
                    
                    for agent_type in agents:
                        try:
                            agent_prompt = self.prompt_manager.get_agent_prompt(domain, agent_type)
                            self.logger.info(f"  ✓ Successfully loaded {agent_type} agent prompt")
                            domain_results["passed"] += 1
                        except Exception as e:
                            self.logger.error(f"  ✗ Failed to load {agent_type} agent prompt: {e}")
                            domain_results["failed"] += 1
                            domain_results["errors"].append(f"{agent_type}: {e}")
                else:
                    common_prompts = ["explain_term", "compare_population"]
                    for prompt_type in common_prompts:
                        try:
                            prompt = self.prompt_manager.get_common_prompt(prompt_type)
                            self.logger.info(f"  ✓ Successfully loaded common prompt: {prompt_type}")
                            domain_results["passed"] += 1
                        except Exception as e:
                            self.logger.error(f"  ✗ Failed to load common prompt {prompt_type}: {e}")
                            domain_results["failed"] += 1
                            domain_results["errors"].append(f"{prompt_type}: {e}")
                
            except Exception as e:
                self.logger.error(f"✗ Failed to load prompts for {domain}: {e}")
                domain_results["failed"] += 1
                domain_results["errors"].append(str(e))
            
            results["details"][domain] = domain_results
            results["passed"] += domain_results["passed"]
            results["failed"] += domain_results["failed"]
        
        self.logger.info(f"\nPrompt loading test summary:")
        self.logger.info(f"Total passed: {results['passed']}")
        self.logger.info(f"Total failed: {results['failed']}")
        
        return results
    
    def test_demo_agents(self):
        self.logger.info("\n" + "=" * 60)
        self.logger.info("TESTING DEMO AGENTS")
        self.logger.info("=" * 60)
        
        results = {"passed": 0, "failed": 0, "details": {}}
        domains = self.prompt_manager.get_available_domains()
        
        for domain in domains:
            if domain == "common":
                continue
                
            self.logger.info(f"\nTesting demo agents for domain: {domain}")
            domain_results = {"passed": 0, "failed": 0, "errors": [], "agents": {}}
            
            agents = self.prompt_manager.get_available_agents(domain)
            
            for agent_type in agents:
                try:
                    self.logger.info(f"  Testing {agent_type} agent...")
                    
                    demo_agent = DemoAgent(domain=domain, agent_type=agent_type, user_id="test_user_001")
                    result = demo_agent.process()
                    
                    if result["success"]:
                        self.logger.info(f"    ✓ {agent_type} agent processed successfully")
                        self.logger.info(f"    Processing time: {result['processing_time']:.2f} seconds")
                        self.logger.info(f"    Response length: {result['response_length']} characters")
                        
                        domain_results["passed"] += 1
                        domain_results["agents"][agent_type] = {
                            "processing_time": result["processing_time"],
                            "response_length": result["response_length"],
                            "prompt_length": result["prompt_length"]
                        }
                    else:
                        raise Exception(result.get("error", "Unknown error"))
                        
                except Exception as e:
                    self.logger.error(f"    ✗ {agent_type} agent failed: {e}")
                    domain_results["failed"] += 1
                    domain_results["errors"].append(f"{agent_type}: {e}")
            
            results["details"][domain] = domain_results
            results["passed"] += domain_results["passed"]
            results["failed"] += domain_results["failed"]
        
        self.logger.info(f"\nDemo agents test summary:")
        self.logger.info(f"Total passed: {results['passed']}")
        self.logger.info(f"Total failed: {results['failed']}")
        
        return results
    
    def test_end_to_end_workflow(self):
        self.logger.info("\n" + "=" * 60)
        self.logger.info("TESTING END-TO-END WORKFLOW")
        self.logger.info("=" * 60)
        
        results = {"passed": 0, "failed": 0, "workflow_steps": []}
        test_domain = "methylation"
        test_user = "test_user_001"
        
        self.logger.info(f"Testing end-to-end workflow for {test_domain} domain")
        
        try:
            # Step 1: Analysis
            self.logger.info("Step 1: Analysis...")
            analysis_agent = DemoAgent(domain=test_domain, agent_type="analysis", user_id=test_user)
            analysis_result = analysis_agent.process()
            
            if analysis_result["success"]:
                self.logger.info("  ✓ Analysis successful")
                results["workflow_steps"].append({
                    "step": "analysis",
                    "success": True,
                    "processing_time": analysis_result["processing_time"]
                })
                results["passed"] += 1
            else:
                raise Exception("Analysis failed")
            
            # Step 2: Summary
            self.logger.info("Step 2: Summary generation...")
            summary_agent = DemoAgent(domain=test_domain, agent_type="summary", user_id=test_user)
            summary_result = summary_agent.process()
            
            if summary_result["success"]:
                self.logger.info("  ✓ Summary generation successful")
                results["workflow_steps"].append({
                    "step": "summary",
                    "success": True,
                    "processing_time": summary_result["processing_time"]
                })
                results["passed"] += 1
            else:
                raise Exception("Summary generation failed")
            
            # Step 3: Recommendations
            self.logger.info("Step 3: Recommendation generation...")
            rec_agent = DemoAgent(domain=test_domain, agent_type="recommendation", user_id=test_user)
            rec_result = rec_agent.process()
            
            if rec_result["success"]:
                self.logger.info("  ✓ Recommendation generation successful")
                results["workflow_steps"].append({
                    "step": "recommendation",
                    "success": True,
                    "processing_time": rec_result["processing_time"]
                })
                results["passed"] += 1
            else:
                raise Exception("Recommendation generation failed")
            
            self.logger.info("✓ End-to-end workflow completed successfully!")
            
        except Exception as e:
            self.logger.error(f"✗ End-to-end workflow failed: {e}")
            results["failed"] += 1
        
        total_time = sum(step["processing_time"] for step in results["workflow_steps"])
        self.logger.info(f"Total workflow time: {total_time:.2f} seconds")
        
        return results
    
    def generate_test_report(self, all_results):
        self.logger.info("\n" + "=" * 60)
        self.logger.info("GENERATING TEST REPORT")
        self.logger.info("=" * 60)
        
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "summary": {"total_tests": 0, "total_passed": 0, "total_failed": 0, "success_rate": 0.0},
            "detailed_results": all_results
        }
        
        for test_name, result in all_results.items():
            if isinstance(result, dict) and "passed" in result and "failed" in result:
                report["summary"]["total_tests"] += result["passed"] + result["failed"]
                report["summary"]["total_passed"] += result["passed"]
                report["summary"]["total_failed"] += result["failed"]
        
        if report["summary"]["total_tests"] > 0:
            report["summary"]["success_rate"] = (
                report["summary"]["total_passed"] / report["summary"]["total_tests"]
            ) * 100
        
        report_file = "testing_logs/test_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Test report saved to: {report_file}")
        self.logger.info(f"Overall success rate: {report['summary']['success_rate']:.1f}%")
        
        return report
    
    def run_all_tests(self):
        self.logger.info("Starting comprehensive agentic workflow testing...")
        start_time = time.time()
        
        all_results = {
            "prompt_loading": self.test_prompt_loading(),
            "demo_agents": self.test_demo_agents(),
            "end_to_end_workflow": self.test_end_to_end_workflow()
        }
        
        report = self.generate_test_report(all_results)
        
        total_time = time.time() - start_time
        self.logger.info(f"\nTotal testing time: {total_time:.2f} seconds")
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info("FINAL TEST SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"Overall Success Rate: {report['summary']['success_rate']:.1f}%")
        self.logger.info(f"Total Tests: {report['summary']['total_tests']}")
        self.logger.info(f"Passed: {report['summary']['total_passed']}")
        self.logger.info(f"Failed: {report['summary']['total_failed']}")
        
        if report['summary']['success_rate'] >= 90:
            self.logger.info("🎉 EXCELLENT! All tests passed successfully!")
        elif report['summary']['success_rate'] >= 80:
            self.logger.info("✅ GOOD! Most tests passed successfully!")
        elif report['summary']['success_rate'] >= 70:
            self.logger.info("⚠️  FAIR! Some tests need attention!")
        else:
            self.logger.info("❌ POOR! Many tests failed and need immediate attention!")
        
        return report

def main():
    print("🧪 Starting Agentic Workflow Testing Suite")
    print("=" * 60)
    
    tester = AgenticWorkflowTester()
    report = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("Testing completed! Check the testing_logs directory for detailed results.")
    print("=" * 60)

if __name__ == "__main__":
    main()
