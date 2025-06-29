# Biomarker Agentic Q&A System

A comprehensive offline testing framework for multi-domain biomarker analysis using agentic workflows. This system provides mock LLM clients and demo agents to test the complete workflow without making actual API calls.

## 🚀 Features

- **Multi-Domain Support**: Methylation, Metagenomics, Proteomics, Transcriptomics, Whole Exome, and Whole Genome analysis
- **Agentic Workflow**: Analysis, Summary, and Recommendation agents for each domain
- **Offline Testing**: Complete testing suite using mock LLM clients
- **Comprehensive Logging**: Detailed logs for each agent and domain
- **Test Data**: Realistic test data for all domains
- **Prompt Management**: Centralized prompt management system

## 📁 Project Structure

```
biomarker-agentic-qna/
├── agents/                          # Agent implementations
│   ├── common/                      # Common agent types
│   ├── methylation/                 # Methylation domain agents
│   ├── metagenomics/               # Metagenomics domain agents
│   ├── proteomics/                 # Proteomics domain agents
│   ├── transcriptomics/            # Transcriptomics domain agents
│   ├── whole_exome/                # Whole exome domain agents
│   ├── whole_genome/               # Whole genome domain agents
│   └── demo_agent.py               # Demo agent for testing
├── utils/                          # Utility modules
│   ├── prompt_manager.py           # Prompt management system
│   ├── mock_llm_client.py          # Mock LLM client for offline testing
│   └── ...
├── user_data/                      # Test data for each domain
│   ├── methylation/
│   ├── metagenomics/
│   ├── proteomics/
│   ├── transcriptomics/
│   ├── whole_exome/
│   └── whole_genome/
├── testing_logs/                   # Test execution logs and reports
├── test_agentic_workflow.py        # Comprehensive testing script
├── test_simple_demo.py             # Simple demo test script
└── README.md                       # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd biomarker-agentic-qna
   ```

2. **Install dependencies** (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the tests**:
   ```bash
   # Quick test
   python3 test_simple_demo.py
   
   # Full comprehensive test
   python3 test_agentic_workflow.py
   ```

## 🧪 Testing

### Quick Test
Run a simple test to verify the system works:
```bash
python3 test_simple_demo.py
```

### Comprehensive Test
Run the full test suite that tests all agents and domains:
```bash
python3 test_agentic_workflow.py
```

### Test Results
After running tests, check the results in:
- **Terminal output**: Real-time test results
- **`testing_logs/`**: Detailed logs and reports
  - `test_execution.log`: Main test execution log
  - `test_report.json`: Machine-readable test results
  - Domain-specific logs: `testing_logs/<domain>/<agent>_agent.log`

## 🔧 Components

### Mock LLM Client
- **File**: `utils/mock_llm_client.py`
- **Purpose**: Simulates LLM responses without making actual API calls
- **Features**: Domain-specific response templates, realistic response generation

### Demo Agent
- **File**: `agents/demo_agent.py`
- **Purpose**: Tests the complete agentic workflow
- **Features**: Prompt formatting, user data loading, comprehensive logging

### Prompt Manager
- **File**: `utils/prompt_manager.py`
- **Purpose**: Manages prompts for all domains and agents
- **Features**: Dynamic prompt loading, template formatting

## 📊 Supported Domains

| Domain | Description | Agents |
|--------|-------------|--------|
| **Methylation** | DNA methylation and epigenetic analysis | Analysis, Summary, Recommendation |
| **Metagenomics** | Gut microbiome analysis | Analysis, Summary, Recommendation |
| **Proteomics** | Protein expression analysis | Analysis, Summary, Recommendation |
| **Transcriptomics** | Gene expression analysis | Analysis, Summary, Recommendation |
| **Whole Exome** | Whole exome sequencing analysis | Analysis, Summary, Recommendation |
| **Whole Genome** | Whole genome analysis | Analysis, Summary, Recommendation |

## 🔍 Understanding the Logs

### Log Structure
Each domain has its own log directory with agent-specific logs:
```
testing_logs/
├── methylation/
│   ├── analysis_agent.log
│   ├── summary_agent.log
│   └── recommendation_agent.log
├── metagenomics/
│   └── ...
└── ...
```

### Log Levels
- **INFO**: Successful operations, processing times, response details
- **ERROR**: Failed operations, missing data, formatting errors
- **WARNING**: Non-critical issues, fallback to mock data

### Test Reports
- **Success Rate**: Overall test success percentage
- **Processing Times**: Time taken for each agent
- **Response Lengths**: Size of generated responses
- **Error Details**: Specific error messages and causes

## 🚀 Usage Examples

### Running a Single Agent Test
```python
from agents.demo_agent import DemoAgent

# Test methylation analysis
agent = DemoAgent(domain="methylation", agent_type="analysis", user_id="test_user_001")
result = agent.process()
print(f"Success: {result['success']}")
print(f"Response: {result['response'][:200]}...")
```

### Testing Multiple Domains
```python
domains = ["methylation", "metagenomics", "proteomics"]
for domain in domains:
    agent = DemoAgent(domain=domain, agent_type="analysis", user_id="test_user_001")
    result = agent.process()
    print(f"{domain}: {'✓' if result['success'] else '✗'}")
```

## 🔧 Customization

### Adding New Domains
1. Create domain directory in `agents/`
2. Add `prompts.json` with agent templates
3. Create test data in `user_data/<domain>/`
4. Update domain mapping in `demo_agent.py`

### Modifying Test Data
Edit files in `user_data/<domain>/<user_id>_report.txt` to customize test scenarios.

### Customizing Mock Responses
Modify `utils/mock_llm_client.py` to change response templates and behavior.

## 📈 Performance Metrics

The system tracks:
- **Processing Time**: Time taken for each agent
- **Success Rate**: Percentage of successful tests
- **Response Quality**: Length and content of responses
- **Error Analysis**: Detailed error tracking and categorization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the logs in `testing_logs/`
2. Review the test reports
3. Open an issue with detailed error information

---

**Note**: This is an offline testing system designed for development and validation. For production use, replace the mock LLM client with actual LLM API clients. 