# Multi-Domain Biomarker Agentic Q&A System

An intelligent conversational AI system that analyzes and explains biomarker data across multiple specialized domains, providing personalized insights and recommendations.

## 🧬 Supported Domains

### 1. **Methylation**
- DNA methylation patterns and epigenetic modifications
- CpG site analysis and epigenetic age assessment
- Disease risk based on methylation patterns
- Lifestyle and environmental influences

### 2. **Metagenomics**
- Gut microbiome composition and diversity
- Bacterial species analysis and functional markers
- SCFA levels and inflammation markers
- Diet-microbiome interactions

### 3. **Whole Exome**
- Protein-coding gene variants and mutations
- Pathogenic variants and VUS interpretation
- Disease risk assessment and pharmacogenomics
- Family inheritance patterns

### 4. **Proteomics**
- Protein expression levels and biomarkers
- Post-translational modifications (PTM)
- Protein pathway analysis and interactions
- Disease-associated protein changes

### 5. **Transcriptomics**
- Gene expression analysis and RNA levels
- Differentially expressed genes
- Transcription factor analysis
- Regulatory network perturbations

### 6. **Whole Genome**
- Complete genome analysis and structural variants
- SNP analysis and copy number variations
- Genome-wide association studies (GWAS)
- Ancestry analysis and complex traits

## 🏗️ System Architecture

### Core Components

1. **MultiDomainOrchestrator**: Main controller that routes queries to appropriate domain-specific agents
2. **DomainClassifier**: Determines which specialized domain a query belongs to
3. **IntentClassifier**: Determines the type of query (insights, recommendations, comparisons, explanations)
4. **Domain-Specific Agents**: Specialized agents for each biomarker domain
5. **Common Agents**: Shared agents for explanations and comparisons across domains

### Directory Structure

```
biomarker-agentic-qna/
├── agents/
│   ├── common/
│   │   ├── base.py
│   │   ├── domain_classifier.py
│   │   ├── intent_classifier.py
│   │   ├── explainer.py
│   │   └── compare.py
│   ├── methylation/
│   │   ├── insight_builder.py
│   │   └── recommendation.py
│   ├── metagenomics/
│   │   └── insight_builder.py
│   ├── whole_exome/
│   │   └── insight_builder.py
│   ├── proteomics/
│   │   └── insight_builder.py
│   ├── transcriptomics/
│   │   └── insight_builder.py
│   └── whole_genome/
│       └── insight_builder.py
├── utils/
│   ├── config.py
│   ├── llama3_client.py
│   ├── openai_client.py
│   ├── llm_factory.py
│   └── user_data_loader.py
├── user_data/
│   ├── methylation/
│   │   └── user_001_report.txt
│   ├── metagenomics/
│   │   └── user_001_report.txt
│   ├── whole_exome/
│   │   └── user_001_report.txt
│   ├── proteomics/
│   │   └── user_001_report.txt
│   ├── transcriptomics/
│   │   └── user_001_report.txt
│   └── whole_genome/
│       └── user_001_report.txt
├── multi_domain_orchestrator.py
├── test_multi_domain.py
└── README_MULTI_DOMAIN.md
```

## 🚀 Usage

### Basic Usage

```python
from multi_domain_orchestrator import MultiDomainOrchestrator

# Initialize the multi-domain system
qa = MultiDomainOrchestrator("openai", model="gpt-4")

# Handle queries - system automatically determines domain
response = qa.handle_user_query("user_001", "Can you explain my methylation report?")
response = qa.handle_user_query("user_001", "What do my microbiome results mean?")
response = qa.handle_user_query("user_001", "Explain my genetic variants")
```

### Domain-Specific Queries

The system automatically classifies queries into appropriate domains:

- **Methylation**: "DNA methylation", "epigenetic age", "CpG sites"
- **Metagenomics**: "microbiome", "gut bacteria", "SCFA levels"
- **Whole Exome**: "genetic variants", "exome sequencing", "VUS"
- **Proteomics**: "protein expression", "biomarkers", "phosphorylation"
- **Transcriptomics**: "gene expression", "RNA levels", "transcription factors"
- **Whole Genome**: "genome sequencing", "SNPs", "GWAS"

### Query Types

Each domain supports these query types:

1. **Insights**: "Can you explain my [domain] report?"
2. **Recommendations**: "What recommendations do you have for my [domain]?"
3. **Comparisons**: "How do my [domain] results compare to others?"
4. **Explanations**: "What is [specific term]?"

## 📊 Data Structure

### Methylation Data
```json
{
  "methylation_score": 0.72,
  "cpg_sites": {
    "total_analyzed": 850000,
    "methylated_sites": 612000,
    "key_regions": {...}
  },
  "epigenetic_age": {
    "chronological_age": 35,
    "biological_age": 42,
    "age_acceleration": 7
  }
}
```

### Metagenomics Data
```json
{
  "health_score": 0.06829,
  "microbiome_composition": {
    "firmicutes": 0.45,
    "bacteroidetes": 0.35
  },
  "diversity_scores": {
    "shannon_diversity": 3.2,
    "species_richness": 150
  }
}
```

### Whole Exome Data
```json
{
  "variant_count": 12500,
  "pathogenic_variants": [...],
  "vus_variants": [...],
  "disease_risk": {
    "monogenic_diseases": {...},
    "complex_diseases": {...}
  }
}
```

## 🛠️ Setup

1. **Environment Variables**:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY="your_openai_api_key"
   export OPENAI_DEFAULT_MODEL="gpt-4"
   
   # For Llama3 (optional)
   export LLAMA3_API_KEY="your_llama3_api_key"
   export LLAMA3_API_URL="your_llama3_api_url"
   ```

2. **Install Dependencies**:
   ```bash
   pip install openai
   ```

3. **Run Tests**:
   ```bash
   python test_multi_domain.py
   ```

## 📝 Example Queries

### Methylation
- "Can you explain my methylation report?"
- "What is CpG methylation?"
- "How does my epigenetic age compare to others?"
- "What lifestyle factors affect my methylation?"

### Metagenomics
- "Can you explain my microbiome results?"
- "What is Shannon diversity?"
- "How do my gut bacteria compare to the population?"
- "What should I eat to improve my microbiome?"

### Whole Exome
- "Can you explain my whole exome sequencing results?"
- "What is a VUS variant?"
- "How do my genetic variants compare to others?"
- "What are my disease risks based on my genes?"

### Proteomics
- "Can you explain my proteomics results?"
- "What is protein phosphorylation?"
- "How do my protein levels compare to normal ranges?"
- "What do my biomarker levels mean?"

## 🔧 Adding New Domains

To add a new domain:

1. **Create Domain Directory**:
   ```bash
   mkdir -p agents/new_domain
   mkdir -p user_data/new_domain
   ```

2. **Create Domain Agents**:
   ```python
   # agents/new_domain/insight_builder.py
   from ..common.base import BaseAgent
   
   class NewDomainInsightBuilderAgent(BaseAgent):
       def run(self, user_query: str, context: Dict[str, Any]) -> str:
           # Domain-specific analysis logic
           pass
   ```

3. **Update Domain Classifier**:
   Add the new domain to `DomainClassifierAgent.DOMAINS`

4. **Update MultiDomainOrchestrator**:
   Import and register the new domain agents

## 🧪 Testing

The system includes comprehensive testing:

```python
# Test multi-domain functionality
python test_multi_domain.py

# Test specific domains
qa = MultiDomainOrchestrator("openai")
response = qa.handle_user_query("user_001", "Explain my methylation data")
```

## 🎯 Key Features

- **Automatic Domain Classification**: Queries are automatically routed to appropriate domain specialists
- **Domain-Specific Analysis**: Each domain has specialized agents with deep expertise
- **Common Functionality**: Shared agents for explanations and comparisons
- **Flexible Data Loading**: Support for domain-specific and general user data
- **Multiple LLM Support**: OpenAI and Llama3 clients
- **Comprehensive Testing**: Full test suite for all domains

## 🔮 Future Enhancements

- **Cross-Domain Analysis**: Integrate insights across multiple domains
- **Temporal Analysis**: Track changes over time
- **Predictive Modeling**: Disease risk predictions
- **Clinical Integration**: EHR integration and clinical decision support
- **Real-time Data**: Live data streaming and analysis

This multi-domain system provides a comprehensive platform for analyzing and interpreting diverse biomarker data, making complex health information accessible and actionable for users. 