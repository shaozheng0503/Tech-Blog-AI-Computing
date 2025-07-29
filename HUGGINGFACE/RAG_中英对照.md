# RAG (检索增强生成) 中英对照文档

## 概述 / Overview

**中文：** 检索增强生成（"RAG"）模型结合了预训练密集检索（DPR）和序列到序列模型的能力。RAG 模型检索文档，将它们传递给 seq2seq 模型，然后进行边缘化以生成输出。检索器和 seq2seq 模块从预训练模型初始化，并联合微调，允许检索和生成都适应下游任务。

**English：** Retrieval-augmented generation ("RAG") models combine the powers of pretrained dense retrieval (DPR) and sequence-to-sequence models. RAG models retrieve documents, pass them to a seq2seq model, then marginalize to generate outputs. The retriever and seq2seq modules are initialized from pretrained models, and fine-tuned jointly, allowing both retrieval and generation to adapt to downstream tasks.

**中文：** 它基于 Patrick Lewis、Ethan Perez、Aleksandara Piktus、Fabio Petroni、Vladimir Karpukhin、Naman Goyal、Heinrich Küttler、Mike Lewis、Wen-tau Yih、Tim Rocktäschel、Sebastian Riedel、Douwe Kiela 撰写的论文《用于知识密集型 NLP 任务的检索增强生成》。

**English：** It is based on the paper Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks by Patrick Lewis, Ethan Perez, Aleksandara Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela.

## 论文摘要 / Paper Abstract

**中文：** 大型预训练语言模型已被证明在其参数中存储事实性知识，并在下游 NLP 任务上进行微调时达到最先进的结果。然而，它们访问和精确操作知识的能力仍然有限，因此在知识密集型任务上，它们的性能落后于特定任务的架构。此外，为其决策提供来源和更新其世界知识仍然是开放的研究问题。具有对显式非参数记忆的可微分访问机制的预训练模型可以克服这个问题，但迄今为止仅在抽取式下游任务中进行了研究。我们探索了检索增强生成（RAG）的通用微调配方——结合预训练参数和非参数记忆进行语言生成的模型。我们引入了 RAG 模型，其中参数记忆是预训练的 seq2seq 模型，非参数记忆是维基百科的密集向量索引，通过预训练的神经检索器访问。我们比较了两种 RAG 公式，一种在整个生成序列中对相同的检索段落进行条件化，另一种可以对每个标记使用不同的段落。我们在广泛的知识密集型 NLP 任务上微调和评估我们的模型，并在三个开放域问答任务上设置了最先进的技术，优于参数化 seq2seq 模型和特定任务的检索-抽取架构。对于语言生成任务，我们发现 RAG 模型比最先进的仅参数化 seq2seq 基线生成更具体、更多样化和更事实性的语言。

**English：** Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit nonparametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

**中文：** 该模型由 ola13 贡献。

**English：** This model was contributed by ola13.

## 使用技巧 / Usage Tips

**中文：** 检索增强生成（"RAG"）模型结合了预训练密集检索（DPR）和 Seq2Seq 模型的能力。RAG 模型检索文档，将它们传递给 seq2seq 模型，然后进行边缘化以生成输出。检索器和 seq2seq 模块从预训练模型初始化，并联合微调，允许检索和生成都适应下游任务。

**English：** Retrieval-augmented generation ("RAG") models combine the powers of pretrained dense retrieval (DPR) and Seq2Seq models. RAG models retrieve docs, pass them to a seq2seq model, then marginalize to generate outputs. The retriever and seq2seq modules are initialized from pretrained models, and fine-tuned jointly, allowing both retrieval and generation to adapt to downstream tasks.

## RagConfig 配置类 / RagConfig Class

**中文：** RagConfig 存储 RagModel 的配置。配置对象继承自 PretrainedConfig，可用于控制模型输出。有关更多信息，请阅读 PretrainedConfig 的文档。

**English：** RagConfig stores the configuration of a RagModel. Configuration objects inherit from PretrainedConfig and can be used to control the model outputs. Read the documentation from PretrainedConfig for more information.

### 主要参数 / Main Parameters

**中文：**
- `title_sep`：在调用 RagRetriever 时插入到检索文档标题和文本之间的分隔符
- `doc_sep`：在调用 RagRetriever 时插入到检索文档文本和原始输入之间的分隔符
- `n_docs`：要检索的文档数量
- `max_combined_length`：`__call__()` 返回的上下文化输入的最大长度
- `retrieval_vector_size`：RagRetriever 索引的文档嵌入的维度
- `retrieval_batch_size`：检索批次大小，定义为并发发送到 RagRetriever 封装的 faiss 索引的查询数量

**English：**
- `title_sep`: Separator inserted between the title and the text of the retrieved document when calling RagRetriever
- `doc_sep`: Separator inserted between the text of the retrieved document and the original input when calling RagRetriever
- `n_docs`: Number of documents to retrieve
- `max_combined_length`: Max length of contextualized input returned by `__call__()`
- `retrieval_vector_size`: Dimensionality of the document embeddings indexed by RagRetriever
- `retrieval_batch_size`: Retrieval batch size, defined as the number of queries issues concurrently to the faiss index encapsulated RagRetriever

## RagTokenizer 分词器 / RagTokenizer

**中文：** RAG 特定的分词器，用于处理问题和生成器的分词化。

**English：** RAG specific tokenizer for handling question and generator tokenization.

## RAG 特定输出 / RAG Specific Outputs

### RetrievAugLMMarginOutput

**中文：** 检索增强边缘化模型输出的基类。包含损失、逻辑值、文档分数、检索的文档嵌入、检索的文档 ID、上下文输入 ID、上下文注意力掩码等。

**English：** Base class for retriever augmented marginalized models outputs. Contains loss, logits, doc_scores, retrieved_doc_embeds, retrieved_doc_ids, context_input_ids, context_attention_mask, etc.

### RetrievAugLMOutput

**中文：** 检索增强语言模型输出，包含逻辑值、文档分数、过去的关键值、检索的文档嵌入等。

**English：** Retrieval augmented language model output containing logits, doc_scores, past_key_values, retrieved_doc_embeds, etc.

## RagRetriever 检索器 / RagRetriever

**中文：** 用于从向量查询获取文档的检索器。它检索文档嵌入以及文档内容，并将它们格式化为与 RagModel 一起使用。

**English：** Retriever used to get documents from vector queries. It retrieves the documents embeddings as well as the documents contents, and it formats them to be used with a RagModel.

### 主要方法 / Main Methods

**中文：**
- `init_retrieval()`：检索器初始化函数，将索引加载到内存中
- `postprocess_docs()`：后处理检索的文档并将其与输入字符串组合
- `retrieve()`：为指定的问题隐藏状态检索文档

**English：**
- `init_retrieval()`: Retriever initialization function. It loads the index into memory
- `postprocess_docs()`: Postprocessing retrieved and combining them with input_strings
- `retrieve()`: Retrieves documents for specified question_hidden_states

## PyTorch 模型 / PyTorch Models

### RagModel

**中文：** 输出原始隐藏状态而不在顶部有任何特定头的裸 RAG 模型。

**English：** The bare Rag Model outputting raw hidden-states without any specific head on top.

### RagSequenceForGeneration

**中文：** RAG 序列模型实现。它在前向传递中执行 RAG 序列特定的边缘化。

**English：** A RAG-sequence model implementation. It performs RAG-sequence specific marginalization in the forward pass.

### RagTokenForGeneration

**中文：** RAG 标记模型实现。它在前向传递中执行 RAG 标记特定的边缘化。

**English：** A RAG-token model implementation. It performs RAG-token specific marginalization in the forward pass.

## TensorFlow 模型 / TensorFlow Models

### TFRagModel

**中文：** TFRagModel 前向方法，重写 `__call__` 特殊方法。RAG 是一个序列到序列模型，它封装了两个核心组件：问题编码器和生成器。在前向传递期间，我们使用问题编码器对输入进行编码，并将其传递给检索器以提取相关的上下文文档。然后将文档前置到输入中。这种上下文化的输入被传递给生成器。

**English：** The TFRagModel forward method, overrides the special `__call__` method. RAG is a sequence-to-sequence model which encapsulates two core components: a question encoder and a generator. During a forward pass, we encode the input with the question encoder and pass it to the retriever to extract relevant context documents. The documents are then prepended to the input. Such contextualized inputs is passed to the generator.

### TFRagSequenceForGeneration

**中文：** TF RAG 序列模型实现。它在前向传递中执行 RAG 序列特定的边缘化。

**English：** A TF RAG-sequence model implementation. It performs RAG-sequence specific marginalization in the forward pass.

### TFRagTokenForGeneration

**中文：** TF RAG 标记模型实现。它在前向传递中执行 RAG 标记特定的边缘化。

**English：** A TF RAG-token model implementation. It performs RAG-token specific marginalization in the forward pass.

## 使用示例 / Usage Examples

### PyTorch 示例 / PyTorch Examples

**中文：** 以下是如何使用 RAG 模型的基本示例：

**English：** Here are basic examples of how to use RAG models:

```python
from transformers import AutoTokenizer, RagRetriever, RagModel
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-token-base")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-base", index_name="exact", use_dummy_dataset=True
)
# 使用 RagRetriever 初始化以在一次前向调用中完成所有操作
model = RagModel.from_pretrained("facebook/rag-token-base", retriever=retriever)

inputs = tokenizer("How many people live in Paris?", return_tensors="pt")
outputs = model(input_ids=inputs["input_ids"])
```

### TensorFlow 示例 / TensorFlow Examples

**中文：** 以下是 TensorFlow 版本的 RAG 模型使用示例：

**English：** Here are examples of using RAG models with TensorFlow:

```python
from transformers import AutoTokenizer, RagRetriever, TFRagModel
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-token-base")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-base", index_name="exact", use_dummy_dataset=True
)
# 使用 RagRetriever 初始化以在一次前向调用中完成所有操作
model = TFRagModel.from_pretrained("facebook/rag-token-base", retriever=retriever, from_pt=True)

input_dict = tokenizer.prepare_seq2seq_batch(
    "How many people live in Paris?", "In Paris, there are 10 million people.", return_tensors="tf"
)
input_ids = input_dict["input_ids"]
outputs = model(input_ids)
```

## 生成方法 / Generation Methods

### generate() 方法

**中文：** 实现 RAG 序列"彻底"解码。阅读 `generate()` 文档以了解如何设置其他生成输入参数的更多信息。

**English：** Implements RAG sequence "thorough" decoding. Read the `generate()` documentation for more information on how to set other generate input parameters.

**中文：** 实现 RAG 标记解码。

**English：** Implements RAG token decoding.

**中文：** 实现 TFRAG 标记解码。

**English：** Implements TFRAG token decoding.

## 关键特性 / Key Features

**中文：**
- 支持多种检索器配置
- 可自定义的文档检索数量
- 灵活的上下文长度设置
- 支持边缘化计算
- 完整的 PyTorch 和 TensorFlow 支持

**English：**
- Support for multiple retriever configurations
- Customizable number of documents to retrieve
- Flexible context length settings
- Support for marginalization computation
- Full PyTorch and TensorFlow support

## 总结 / Summary

**中文：** RAG 模型代表了检索增强生成领域的重要进展，通过结合参数化和非参数化记忆，为知识密集型 NLP 任务提供了强大的解决方案。该实现支持多种配置选项，并与 Hugging Face Transformers 库完全集成。

**English：** RAG models represent a significant advancement in the field of retrieval-augmented generation, providing powerful solutions for knowledge-intensive NLP tasks by combining parametric and non-parametric memory. This implementation supports multiple configuration options and is fully integrated with the Hugging Face Transformers library. 