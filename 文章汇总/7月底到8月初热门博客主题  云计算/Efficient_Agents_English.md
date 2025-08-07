# Efficient Agents: Building Effective Agents While Reducing Cost

*OPPO AI Agent Team*  
*August 6, 2025*

## Abstract

The remarkable capabilities of Large Language Model (LLM)-driven agents have enabled sophisticated systems to tackle complex, multi-step tasks, but their escalating costs threaten scalability and accessibility. This work presents the first systematic study of the efficiency-effectiveness trade-off in modern agent systems, addressing the critical need for cost-effective designs without sacrificing performance.

We investigate three key questions:
1. How much complexity do agentic tasks inherently require?
2. When do additional modules yield diminishing returns?
3. How much efficiency can be gained through the design of efficient agent frameworks?

Through an empirical analysis on the GAIA benchmark, we evaluate the impact of LLM backbone selection, agent framework designs, and test-time scaling strategies. Using the cost-of-pass metric, we quantify the efficiency-performance trade-off across these dimensions. Our findings inform the development of **Efficient Agents**, a novel agent framework that has an optimal complexity to task requirements.

**Efficient Agents** retains 96.7% of the performance of OWL, one leading open-source agent framework, while reducing operational costs from $0.398 to $0.228, resulting in a 28.4% improvement in cost-of-pass. Our work provides actionable insights for designing efficient, high-performing agent systems, advancing the accessibility and sustainability of AI-driven solutions.

**Correspondence:** Wangchunshu Zhou at zhouwangchunshu@oppo.com; He Zhu at zhuhe@oppo.com  
**Code:** https://github.com/OPPO-PersonalAI/OAgents

## 1. Introduction

The ever-increasing reasoning and creation capabilities of Large Language Models (LLMs) have opened up a broad prospect for real-world applications. Researchers have developed numerous LLM-driven agent systems and created a large number of fascinating products capable of handling complex, multi-step tasks. However, this progress mirrors a familiar trajectory in NLP research: from BERT to ChatGPT, researchers consistently prioritize scaling up models to achieve breakthrough capabilities, only later turning to optimize efficiency, cost, and environmental impact.

We argue that agent research has now reached a similar inflection point. While increasingly sophisticated agent architectures can solve remarkably complex problems, their costs scale prohibitively. Industry deployments reveal this tension starkly: cutting-edge agent products (e.g., DeepResearch, Manus) demonstrate impressive capabilities but suffer from exorbitant operating costs due to explosive LLM call overhead. Some systems require hundreds of API calls per task, rendering them economically unsustainable despite their technical brilliance.

Our work presents the first systematic study of the efficiency-effectiveness trade-off in modern agent systems. Through rigorous empirical analysis, we investigate 3 research questions:

1. **How much complexity do agentic tasks truly require?**
2. **When do additional modules yield diminishing returns?**
3. **How much efficiency can be gained through the design of task-adaptive agent frameworks?**

By dissecting these relationships across the framework, we provide actionable insights for both researchers and practitioners.

## 2. Preliminaries

### 2.1 Setup

Many factors can influence the effectiveness and efficiency of an agent system. In this paper, we aim to conduct a comprehensive analysis from the perspective of agent systems. These factors encompass not only the backbone LLM itself but also the agent framework built around it, including:

- **Planning mechanisms**
- **Tool usage**
- **Memory module**
- **Test-time scaling strategies**

We evaluate these components on GAIA, a popular and challenging agent benchmark that typically requires agents to perform complex reasoning to solve problems.

### 2.2 Metrics

An ideal agent should achieve both high performance and computational efficiency. Therefore, in addition to accuracy, measured by pass@1 (solving the problem in one attempt) to evaluate effectiveness, we assess efficiency using the number of tokens taken by LLMs and associated costs.

We adopt the **cost-of-pass metric** to quantify model efficiency. The cost-of-pass metric, denoted as v(m,p), represents the expected monetary cost of using a model m to generate a correct solution for a problem p. It is computed as:

```
v(m,p) = C_m(p) / R_m(p)
```

Where:
- C_m(p) is the cost of a single inference attempt
- R_m(p) is the success rate

## 3. On the Efficiency-Performance Trade-off of Agent Systems

### 3.1 Backbones

Current Large Language Models acquire System-2 reasoning capabilities through reinforcement learning, leveraging extended chain-of-thought processes that often span thousands of tokens or more. While this approach significantly enhances reasoning performance, it also substantially increases computational costs and even leads to the phenomenon of overthinking.

**Key Findings:**

- **Claude 3.7 Sonnet** achieves the highest accuracy on the GAIA benchmark (61.82% overall) compared to GPT-4.1 (53.33%), but its cost-of-pass is significantly higher (3.54 vs. 0.98)
- **Sparse models** like Qwen3-30B-A3B exhibit superior efficiency, with a low cost-of-pass (0.13 overall) despite modest accuracy (17.58% overall)
- As task difficulty increases from Level 1 to Level 3, cost-of-pass rises dramatically across large reasoning models

### 3.2 Test-time Scaling Strategies

Test-time scaling enhances models performance by leveraging multiple inference runs, but these approaches typically require the model to be executed N times, significantly increasing token consumption.

**Best-of-N Results:**
- Increasing N from 1 to 4 leads to a substantial rise in token consumption (from 243k to 325k)
- Performance improvement is marginal, with accuracy only slightly increasing from 53.33% to 53.94%
- Cost-of-pass rises from 0.98 to 1.28

### 3.3 Planning

To enhance the agent's ability to handle long-horizon tasks, a planning module prior to execution is usually adopted. Planning can be regarded as a continuous task decomposition process.

**Key Insights:**
- Increasing the maximum number of steps within a certain range significantly improves performance
- When maximum steps increase from 4 to 8, accuracy rises from 58.49% to 69.81%
- Beyond a certain threshold, further increasing steps does not enhance performance but continues to increase costs

### 3.4 Tool Using

Incorporating external tools significantly enhances the agent's capabilities, especially in scenarios where neural networks alone fall short. We focus on web browser usage as it represents a widely adopted and general-purpose tool.

**Tool Configuration Impact:**
- Increasing the number of search sources significantly enhances both effectiveness and efficiency
- Simpler browser operations outperform advanced operations in both effectiveness and efficiency
- Expanding the number of reformulated queries consistently improves both effectiveness and efficiency

### 3.5 Memory

Memory is a critical component for LLM-driven agent systems, enabling effective interaction with and learning from dynamic environments. We design six memory configurations to evaluate their impact:

1. **Simple Memory**: Only historical observations and actions are kept
2. **Summarized Memory**: Information is summarized and embedded
3. **w/o Extra Memory**: Only step history is kept
4. **Extra Summarized Memory**: Summarized memory alongside step history
5. **Extra Fixed Memory**: Fixed-length text maintained as long-term memory
6. **Extra Hybrid Memory**: Both summarized and long memory approaches

**Results:** Simple Memory configuration yields the best performance, improving from 53.33% to 56.36%, while reducing cost-of-pass from 0.98 to 0.74.

## 4. Efficient Agents: Tricks of the Trade

Based on our empirical studies, we propose **Efficient Agents**, an agent system comprising carefully selected components to achieve a great trade-off between effectiveness and efficiency.

**Configuration Strategy:**
For each component in the agent system, we adopt the configuration with the lowest cost-of-pass among those that do not lead to substantial performance degradation.

**Performance Results:**
- Achieves 96.7% of the performance of OWL
- Reduces operational costs by 28.4%
- Cost-of-pass improvement from $0.398 to $0.228

## 5. Related Work

### 5.1 LLM-driven Agents

LLM-based agent technologies have demonstrated remarkable capabilities across a wide range of tasks, significantly spurring the rapid advancement of general agent systems. Recent research efforts have been dedicated to building general agent systems capable of tackling complex reasoning, planning, and search tasks.

**Notable Systems:**
- **OpenAI's Deep Research**: Achieved 67.36% on GAIA benchmark
- **OWL (Optimized Workforce Learning)**: Scored 69.7% on GAIA benchmark

### 5.2 Efficient NLP

Since the advent of BERT, the scale of language models has grown exponentially, leading to substantial increases in computational and energy costs during inference. Significant research has focused on enhancing NLP efficiency.

**Key Approaches:**
- **Knowledge Distillation**: DistilBERT creates compact models from BERT
- **Token Budget Awareness**: Controls model output length by estimating token requirements
- **Multi-agent Optimization**: AgentPrune optimizes communication by pruning superfluous messages

## 6. Conclusion

This paper makes several key contributions:

1. **Comprehensive Analysis**: We provide a thorough analysis of architectural choices and operational factors that contribute to economic overhead in contemporary agent systems.

2. **Efficient Agents Framework**: We introduce a novel agent framework engineered for optimal balance between task performance and computational cost.

3. **Empirical Validation**: Our extensive experiments on the GAIA benchmark demonstrate the efficacy of our approach, achieving 96.7% of state-of-the-art performance while reducing operational costs by 28.4%.

This work underscores the critical importance of efficiency considerations in the design of next-generation agent systems and offers a practical pathway towards more scalable and economically viable real-world deployments.

## Core Contributors

- Ningning Wang
- Xavier Hu

## Contributors

- Pai Liu
- Yue Hou
- Heyuan Huang
- Shengyu Zhang
- Jian Yang
- Jiaheng Liu
- Ge Zhang
- Changwang Zhang
- Jun Wang
- Yuchen Eleanor Jiang

## Corresponding Authors

- He Zhu
- Wangchunshu Zhou

---

*This document is based on the research paper "Efficient Agents: Building Effective Agents While Reducing Cost" by the OPPO AI Agent Team. For more information, visit: https://github.com/OPPO-PersonalAI/OAgents* 