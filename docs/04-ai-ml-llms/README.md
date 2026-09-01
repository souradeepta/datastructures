# AI/ML/LLMs Interview Guide

Study reference for AI, machine learning, and large language model interview preparation.

---

## 📚 Guides in This Section

### 🤖 **Fundamentals**
- [ML Fundamentals](01-ml-fundamentals.md) — Core concepts, algorithms, workflows
- [Neural Networks Basics](02-neural-networks-basics.md) — Perceptrons, activation, backpropagation, optimization
- [Deep Learning Essentials](03-deep-learning-essentials.md) — CNNs, RNNs, attention mechanisms

### 🔄 **Language Models**
- [LLM Architecture & Transformers](04-llm-architecture.md) — Transformer architecture, attention, scaling laws
- [Prompt Engineering & Design](05-prompt-engineering.md) — Techniques, chain-of-thought, few-shot learning
- [RAG Systems & Knowledge Integration](06-rag-systems.md) — Retrieval-augmented generation, vector DBs, semantic search

### 🛠️ **Engineering & Optimization**
- [Fine-tuning & Training Strategies](07-fine-tuning-training.md) — LoRA, QLoRA, instruction tuning, RLHF
- [Model Serving & Inference](08-model-serving-inference.md) — Quantization, batching, latency optimization
- [Reinforcement Learning](09-reinforcement-learning.md) — Learning from rewards and policies

### 📊 **Production & Systems**
- [ML Systems Design](10-ml-systems-design.md) — Pipelines, data engineering, monitoring, feedback loops
- [Computer Vision](11-computer-vision.md) — Image recognition, detection, and segmentation
- [NLP Advanced](12-nlp-advanced.md) — Transformers, BERT, GPT, and modern architectures
- [Scaling LLMs](13-scaling-llms.md) — Parameters, parallelism, and systems constraints
- [Safety & Alignment](14-safety-alignment.md) — Evaluation, misuse resistance, and alignment
- [Model Evaluation](15-model-evaluation.md) — Metrics, benchmarks, and experimental design
- [Cost Optimization for ML](16-cost-optimization.md) — Capacity, caching, and cost trade-offs
- [Interpretability & Explainability](17-interpretability.md) — Explanations, limitations, and trust
- [Multimodal Models](18-multimodal-models.md) — Vision, language, audio, and fusion
- [LLMOps](19-llmops.md) — Model management, deployment, monitoring, and cost optimization

### 🧪 Runnable ML/AI systems labs

See [educational examples](EDUCATIONAL_EXAMPLES.md) and [content status](CONTENT_STATUS.md).
The labs cover feature point-in-time parity, lexical RAG retrieval/provenance, and
guarded model rollouts. They are standard-library-only in-memory exercises.

---

## 🎯 Quick Navigation

**"I have an AI interview next week"**
1. Read: [ML Fundamentals](01-ml-fundamentals.md) + [LLM Architecture](04-llm-architecture.md)
2. Study: [Prompt Engineering](05-prompt-engineering.md) (most practical)
3. Practice: Common interview Q&A patterns

**"I want to understand transformers"**
→ [LLM Architecture & Transformers](04-llm-architecture.md)

**"I want to build with LLMs"**
→ [RAG Systems](06-rag-systems.md) + [LLMOps](19-llmops.md)

**"I need to optimize model performance"**
→ [Fine-tuning Strategies](07-fine-tuning-training.md) + [Model Serving](08-model-serving-inference.md)

**"I'm designing an ML system"**
→ [ML Systems Design](10-ml-systems-design.md) + [LLMOps](19-llmops.md)

---

## 📖 Reading Path by Level

### Beginner (Week 1)
1. ML Fundamentals (concepts, algorithms)
2. Neural Networks Basics (perceptrons to optimization)
3. LLM Architecture (transformers simplified)
4. Prompt Engineering (practical techniques)

### Intermediate (Weeks 2-3)
5. RAG Systems (knowledge integration)
6. Fine-tuning Strategies (adapting models)
7. Model Serving (production deployment)
8. [Feature pipelines and parity](20-feature-pipelines-and-parity.md) (point-in-time practice)

### Advanced (Weeks 4+)
9. ML Systems Design (full pipeline)
10. [RAG grounding lab](21-rag-grounding-and-evaluation.md) and LLMOps
11. [Model rollout lab](22-model-rollouts-and-serving.md)

---

## 🔑 Key Interview Topics by Company

**Google/DeepMind:**
- Transformer architecture, attention mechanisms
- Scaling laws and model evaluation
- Distributed training and optimization

**OpenAI/Anthropic:**
- Prompt engineering and instruction tuning
- RLHF and alignment techniques
- Safety and interpretability

**Meta/Microsoft:**
- Large-scale LLM deployment
- Quantization and inference optimization
- Multimodal models and applications

**Amazon/AWS:**
- ML systems design and pipelines
- Real-time inference and serving
- A/B testing and monitoring in production

---

## 💡 Common Interview Questions

### ML Fundamentals
- "Explain overfitting and how to prevent it"
- "What's the difference between classification and regression?"
- "How do you handle imbalanced datasets?"
- "Explain regularization (L1, L2, dropout)"

### Neural Networks
- "How does backpropagation work?"
- "What are activation functions and why do we need them?"
- "Explain batch normalization"
- "What's the vanishing gradient problem?"

### Transformers/LLMs
- "Explain the attention mechanism"
- "How do position embeddings work?"
- "Why are transformers better than RNNs?"
- "Explain multi-head attention"

### Practical LLM Work
- "How do you improve LLM outputs without retraining?"
- "What's RAG and when would you use it?"
- "Explain prompt engineering techniques"
- "How do you fine-tune an LLM efficiently?"

### Systems
- "Design an LLM serving system for 1M daily users"
- "How would you reduce inference latency?"
- "Explain quantization and its trade-offs"
- "How do you monitor model performance in production?"

---

## 🧪 Practice Problems

### Coding Problems
- Implement attention mechanism from scratch
- Build a simple transformer encoder
- Implement tokenization and embeddings
- Create a basic RAG system

### System Design
- Design an LLM inference serving platform
- Build an ML training pipeline
- Design a recommendation system using embeddings
- Create a conversational AI with memory

### Conceptual
- Explain when to use fine-tuning vs. prompt engineering
- Discuss trade-offs in model size vs. latency
- Explain how to evaluate LLM outputs
- Describe safety considerations in LLM deployment

---

## 📚 External Resources

**Papers to Know:**
- "Attention is All You Need" (Vaswani et al., 2017)
- "BERT" (Devlin et al., 2018)
- "Language Models are Few-Shot Learners" (GPT-3)
- "LLaMA: Open and Efficient Foundation Language Models"

**Communities:**
- Hugging Face Hub (model zoo, papers, discussions)
- Papers with Code (benchmarks, implementations)
- ArXiv ML section (cutting-edge research)

---

## ✅ Self-Assessment Checklist

By the end of this guide, you should be able to:

- [ ] Explain how neural networks learn (forward & backprop)
- [ ] Describe attention mechanisms and why they matter
- [ ] Understand transformer architecture in detail
- [ ] Discuss prompt engineering techniques and trade-offs
- [ ] Explain RAG and when to use it
- [ ] Describe fine-tuning approaches (LoRA, etc.)
- [ ] Discuss inference optimization (quantization, batching)
- [ ] Design an end-to-end ML system
- [ ] Answer LLM-specific interview questions
- [ ] Build a simple LLM application (code or design)

---

**Last updated:** 2026-05-22
