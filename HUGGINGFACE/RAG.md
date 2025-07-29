Join the Hugging Face community
and get access to the augmented documentation experience

Collaborate on models, datasets and Spaces
Faster examples with accelerated inference
Switch between documentation themes
Sign Up
to get started

RAG
PyTorchTensorFlowFlashAttention
Overview
Retrieval-augmented generation (“RAG”) models combine the powers of pretrained dense retrieval (DPR) and sequence-to-sequence models. RAG models retrieve documents, pass them to a seq2seq model, then marginalize to generate outputs. The retriever and seq2seq modules are initialized from pretrained models, and fine-tuned jointly, allowing both retrieval and generation to adapt to downstream tasks.

It is based on the paper Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks by Patrick Lewis, Ethan Perez, Aleksandara Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela.

The abstract from the paper is the following:

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit nonparametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

This model was contributed by ola13.

Usage tips
Retrieval-augmented generation (“RAG”) models combine the powers of pretrained dense retrieval (DPR) and Seq2Seq models. RAG models retrieve docs, pass them to a seq2seq model, then marginalize to generate outputs. The retriever and seq2seq modules are initialized from pretrained models, and fine-tuned jointly, allowing both retrieval and generation to adapt to downstream tasks.

RagConfig
class transformers.RagConfig
<
source
>
( vocab_size = Noneis_encoder_decoder = Trueprefix = Nonebos_token_id = Nonepad_token_id = Noneeos_token_id = Nonedecoder_start_token_id = Nonetitle_sep = ' / 'doc_sep = ' // 'n_docs = 5max_combined_length = 300retrieval_vector_size = 768retrieval_batch_size = 8dataset = 'wiki_dpr'dataset_split = 'train'index_name = 'compressed'index_path = Nonepassages_path = Noneuse_dummy_dataset = Falsereduce_loss = Falselabel_smoothing = 0.0do_deduplication = Trueexclude_bos_score = Falsedo_marginalize = Falseoutput_retrieved = Falseuse_cache = Trueforced_eos_token_id = Nonedataset_revision = None**kwargs )

Parameters

title_sep (, optional, defaults to ) — Separator inserted between the title and the text of the retrieved document when calling RagRetriever.str" / "
doc_sep (, optional, defaults to ) — Separator inserted between the text of the retrieved document and the original input when calling RagRetriever.str" // "
n_docs (, optional, defaults to 5) — Number of documents to retrieve.int
max_combined_length (, optional, defaults to 300) — Max length of contextualized input returned by .int__call__()
retrieval_vector_size (, optional, defaults to 768) — Dimensionality of the document embeddings indexed by RagRetriever.int
retrieval_batch_size (, optional, defaults to 8) — Retrieval batch size, defined as the number of queries issues concurrently to the faiss index encapsulated RagRetriever.int
dataset (, optional, defaults to ) — A dataset identifier of the indexed dataset in HuggingFace Datasets (list all available datasets and ids using ).str"wiki_dpr"datasets.list_datasets()
dataset_split (, optional, defaults to ) — Which split of the to load.str"train"dataset
index_name (, optional, defaults to ) — The index name of the index associated with the . One can choose between , and .str"compressed"dataset"legacy""exact""compressed"
index_path (, optional) — The path to the serialized faiss index on disk.str
passages_path (, optional) — A path to text passages compatible with the faiss index. Required if using strLegacyIndex
use_dummy_dataset (, optional, defaults to ) — Whether to load a “dummy” variant of the dataset specified by .boolFalsedataset
label_smoothing (, optional, defaults to 0.0) — Only relevant if is set to . Controls the parameter value for label smoothing in the loss calculation. If set to 0, no label smoothing is performed.floatreturn_lossTrueepsilon
do_marginalize (, optional, defaults to ) — If , the logits are marginalized over all documents by making use of .boolFalseTruetorch.nn.functional.log_softmax
reduce_loss (, optional, defaults to ) — Whether or not to reduce the NLL loss using the operation.boolFalsetorch.Tensor.sum
do_deduplication (, optional, defaults to ) — Whether or not to deduplicate the generations from different context documents for a given input. Has to be set to if used while training with distributed backend.boolTrueFalse
exclude_bos_score (, optional, defaults to ) — Whether or not to disregard the BOS token when computing the loss.boolFalse
output_retrieved(bool, optional, defaults to ) — If set to , , , and are returned. See returned tensors for more detail.FalseTrueretrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
use_cache (, optional, defaults to ) — Whether or not the model should return the last key/values attentions (not used by all models).boolTrue
forced_eos_token_id (, optional) — The id of the token to force as the last generated token when is reached. Usually set to .intmax_lengtheos_token_id
RagConfig stores the configuration of a RagModel. Configuration objects inherit from PretrainedConfig and can be used to control the model outputs. Read the documentation from PretrainedConfig for more information.

from_question_encoder_generator_configs
<
source
>
( question_encoder_config: PretrainedConfiggenerator_config: PretrainedConfig**kwargs ) → EncoderDecoderConfig

Returns

EncoderDecoderConfig

An instance of a configuration object


Instantiate a EncoderDecoderConfig (or a derived class) from a pre-trained encoder model configuration and decoder model configuration.

RagTokenizer
class transformers.RagTokenizer
<
source
>
( question_encodergenerator )

Rag specific outputs
class transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput
<
source
>
( loss: typing.Optional[torch.FloatTensor] = Nonelogits: typing.Optional[torch.FloatTensor] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Nonepast_key_values: typing.Optional[list[torch.FloatTensor]] = Noneretrieved_doc_embeds: typing.Optional[torch.FloatTensor] = Noneretrieved_doc_ids: typing.Optional[torch.LongTensor] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Nonequestion_encoder_last_hidden_state: typing.Optional[torch.FloatTensor] = Nonequestion_enc_hidden_states: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonequestion_enc_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_enc_last_hidden_state: typing.Optional[torch.FloatTensor] = Nonegenerator_enc_hidden_states: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_enc_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_dec_hidden_states: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_dec_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_cross_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = None )

Parameters

loss ( of shape , optional, returned when is provided) — Language modeling loss.torch.FloatTensor(1,)labels
logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.torch.FloatTensor(batch_size, sequence_length, config.vocab_size)
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state
past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[torch.FloatTensor]use_cache=Trueconfig.use_cache=Truetorch.FloatTensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)
Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .torch.FloatTensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores
retrieved_doc_ids ( of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.torch.LongTensor(batch_size, config.n_docs)
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)
context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids
question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)
question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)
Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)
generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)
Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)
Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_cross_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Cross-attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the cross-attention heads.

Base class for retriever augmented marginalized models outputs.

class transformers.models.rag.modeling_rag.RetrievAugLMOutput
<
source
>
( logits: typing.Optional[torch.FloatTensor] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Nonepast_key_values: typing.Optional[list[torch.FloatTensor]] = Noneretrieved_doc_embeds: typing.Optional[torch.FloatTensor] = Noneretrieved_doc_ids: typing.Optional[torch.LongTensor] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Nonequestion_encoder_last_hidden_state: typing.Optional[torch.FloatTensor] = Nonequestion_enc_hidden_states: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonequestion_enc_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_enc_last_hidden_state: typing.Optional[torch.FloatTensor] = Nonegenerator_enc_hidden_states: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_enc_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_dec_hidden_states: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_dec_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = Nonegenerator_cross_attentions: typing.Optional[tuple[torch.FloatTensor, ...]] = None )

Parameters

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.torch.FloatTensor(batch_size, sequence_length, config.vocab_size)
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state
past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[torch.FloatTensor]use_cache=Trueconfig.use_cache=Truetorch.FloatTensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)
Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .torch.FloatTensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores
retrieved_doc_ids ( of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.torch.LongTensor(batch_size, config.n_docs)
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)
context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids
question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)
question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)
Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)
generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)
Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)
Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_cross_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)
Cross-attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the cross-attention heads.

RagRetriever
class transformers.RagRetriever
<
source
>
( configquestion_encoder_tokenizergenerator_tokenizerindex = Noneinit_retrieval = True )

Parameters

config (RagConfig) — The configuration of the RAG model this Retriever is used with. Contains parameters indicating which to build. You can load your own custom dataset with or use a canonical one (default) from the datasets library with for example.Indexconfig.index_name="custom"config.index_name="wiki_dpr"
question_encoder_tokenizer (PreTrainedTokenizer) — The tokenizer that was used to tokenize the question. It is used to decode the question and then use the generator_tokenizer.
generator_tokenizer (PreTrainedTokenizer) — The tokenizer used for the generator part of the RagModel.
index (, optional, defaults to the one defined by the configuration) — If specified, use this index instead of the one built using the configurationIndex
Retriever used to get documents from vector queries. It retrieves the documents embeddings as well as the documents contents, and it formats them to be used with a RagModel.

Examples:

Copied
# To load the default "wiki_dpr" dataset with 21M passages from wikipedia (index name is 'compressed' or 'exact')
from transformers import RagRetriever

retriever = RagRetriever.from_pretrained(
    "facebook/dpr-ctx_encoder-single-nq-base", dataset="wiki_dpr", index_name="compressed"
)

# To load your own indexed dataset built with the datasets library. More info on how to build the indexed dataset in examples/rag/use_own_knowledge_dataset.py
from transformers import RagRetriever

dataset = (
    ...
)  # dataset must be a datasets.Datasets object with columns "title", "text" and "embeddings", and it must have a supported index (e.g., Faiss or other index types depending on your setup)
retriever = RagRetriever.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base", indexed_dataset=dataset)

# To load your own indexed dataset built with the datasets library that was saved on disk. More info in examples/rag/use_own_knowledge_dataset.py
from transformers import RagRetriever

dataset_path = "path/to/my/dataset"  # dataset saved via *dataset.save_to_disk(...)*
index_path = "path/to/my/index"  # index saved via *dataset.get_index("embeddings").save(...)*
retriever = RagRetriever.from_pretrained(
    "facebook/dpr-ctx_encoder-single-nq-base",
    index_name="custom",
    passages_path=dataset_path,
    index_path=index_path,
)

# To load the legacy index built originally for Rag's paper
from transformers import RagRetriever

retriever = RagRetriever.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base", index_name="legacy")
init_retrieval
<
source
>
( )

Retriever initialization function. It loads the index into memory.

postprocess_docs
<
source
>
( docsinput_stringsprefixn_docsreturn_tensors = None ) → tuple(tensors)

Parameters

docs () — Retrieved documents.dict
input_strings () — Input strings decoded by .strpreprocess_query
prefix () — Prefix added at the beginning of each input, typically used with T5-based models.str
Returns

tuple(tensors)

a tuple consisting of two elements: contextualized and a compatible .input_idsattention_mask


Postprocessing retrieved and combining them with .docsinput_strings

retrieve
<
source
>
( question_hidden_states: ndarrayn_docs: int ) → tuple[np.ndarray, np.ndarray, list[dict]]

Parameters

question_hidden_states ( of shape ) — A batch of query vectors to retrieve with.np.ndarray(batch_size, vector_size)
n_docs () — The number of docs retrieved per query.int
Returns

tuple[np.ndarray, np.ndarray, list[dict]]

A tuple with the following objects:

retrieved_doc_embeds ( of shape ) — The retrieval embeddings of the retrieved docs per query.np.ndarray(batch_size, n_docs, dim)
doc_ids ( of shape ) — The ids of the documents in the indexnp.ndarray(batch_size, n_docs)
doc_dicts (): The examples per query.list[dict]retrieved_doc_embeds

Retrieves documents for specified .question_hidden_states

Pytorch
Hide Pytorch content
RagModel
class transformers.RagModel
<
source
>
( config: typing.Optional[transformers.configuration_utils.PretrainedConfig] = Nonequestion_encoder: typing.Optional[transformers.modeling_utils.PreTrainedModel] = Nonegenerator: typing.Optional[transformers.modeling_utils.PreTrainedModel] = Noneretriever: typing.Optional[transformers.models.rag.retrieval_rag.RagRetriever] = None**kwargs )

Parameters

config (PretrainedConfig, optional) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the from_pretrained() method to load the model weights.
question_encoder (, optional) — The model responsible for encoding the question into hidden states for retrieval.PreTrainedModel
generator (, optional) — The model responsible for generating text based on retrieved documents.PreTrainedModel
retriever (, optional) — The component responsible for retrieving documents from a knowledge base given the encoded question.RagRetriever
The bare Rag Model outputting raw hidden-states without any specific head on top.

This model inherits from PreTrainedModel. Check the superclass documentation for the generic methods the library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads etc.)

This model is also a PyTorch torch.nn.Module subclass. Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage and behavior.

forward
<
source
>
( input_ids: typing.Optional[torch.LongTensor] = Noneattention_mask: typing.Optional[torch.Tensor] = Noneencoder_outputs: typing.Optional[tuple[tuple[torch.FloatTensor]]] = Nonedecoder_input_ids: typing.Optional[torch.LongTensor] = Nonedecoder_attention_mask: typing.Optional[torch.BoolTensor] = Nonepast_key_values: typing.Optional[tuple[tuple[torch.FloatTensor]]] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Noneuse_cache: typing.Optional[bool] = Noneoutput_attentions: typing.Optional[bool] = Noneoutput_hidden_states: typing.Optional[bool] = Noneoutput_retrieved: typing.Optional[bool] = Nonen_docs: typing.Optional[int] = None ) → transformers.models.rag.modeling_rag.RetrievAugLMOutput or tuple(torch.FloatTensor)

Parameters

input_ids ( of shape ) — Indices of input sequence tokens in the vocabulary. RagConfig, used to initialize the model, specifies which generator to use, it also specifies a compatible generator tokenizer. Use that tokenizer class to obtain the indices.torch.LongTensor(batch_size, sequence_length)
What are input IDs?

attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :torch.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

encoder_outputs (, optional) — Tuple consists of (, optional: , optional: ). of shape is a sequence of hidden-states at the output of the last layer of the generator’s encoder.tuple(tuple(torch.FloatTensor)generator_enc_last_hidden_stategenerator_enc_hidden_statesgenerator_enc_attentionsgenerator_enc_last_hidden_state(batch_size, n_docs * sequence_length, hidden_size)
Used by the (RagModel) model during decoding.

decoder_input_ids ( of shape , optional) — Provide for generation tasks. by default, construct as per instructions for the generator model you’re using with your RAG instance.torch.LongTensor(batch_size, target_sequence_length)None
decoder_input_ids ( of shape , optional) — Indices of decoder input sequence tokens in the vocabulary.torch.LongTensor(batch_size, target_sequence_length)
Indices can be obtained using AutoTokenizer. See PreTrainedTokenizer.encode() and PreTrainedTokenizer.call() for details.

What are decoder input IDs?

decoder_attention_mask ( of shape , optional) — Default behavior: generate a tensor that ignores pad tokens in . Causal mask will also be used by default.torch.BoolTensor(batch_size, target_sequence_length)decoder_input_ids
past_key_values (, optional) — Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in the returned by the model at a previous stage of decoding, when or .tuple[tuple[torch.FloatTensor]]past_key_valuesuse_cache=Trueconfig.use_cache=True
Two formats are allowed:

a Cache instance, see our kv cache guide;
Tuple of of length , with each tuple having 2 tensors of shape ). This is also known as the legacy cache format.tuple(torch.FloatTensor)config.n_layers(batch_size, num_heads, sequence_length, embed_size_per_head)
The model will output the same cache format that is fed as input. If no are passed, the legacy cache format will be returned.past_key_values

If are used, the user can optionally input only the last (those that don’t have their past key value states given to this model) of shape instead of all of shape .past_key_valuesinput_ids(batch_size, 1)input_ids(batch_size, sequence_length)

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a has to be provided to the forward pass. can be computed via and , see examples for more information.torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverdoc_scoresdoc_scoresquestion_encoder_last_hidden_stateretrieved_doc_embeds
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever. If the model was not initialized with a ` has to be provided to the forward pass. are returned by .torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrievercontext_input_idscontext_input_ids__call__()
context_attention_mask ( of shape ,optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever. If the model has is not initialized with a has to be provided to the forward pass. are returned by .torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrievercontext_attention_maskcontext_attention_mask__call__()
use_cache (, optional) — If set to , key value states are returned and can be used to speed up decoding (see ).boolTruepast_key_valuespast_key_values
output_attentions (, optional) — Whether or not to return the attentions tensors of all attention layers. See under returned tensors for more detail.boolattentions
output_hidden_states (, optional) — Whether or not to return the hidden states of all layers. See under returned tensors for more detail.boolhidden_states
output_retrieved (, optional) — Whether or not to return the , , and . See returned tensors for more detail.boolretrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
n_docs (, optional) — The number of documents to retrieve.int
Returns

transformers.models.rag.modeling_rag.RetrievAugLMOutput or tuple(torch.FloatTensor)

A transformers.models.rag.modeling_rag.RetrievAugLMOutput or a tuple of (if is passed or when ) comprising various elements depending on the configuration (RagConfig) and inputs.torch.FloatTensorreturn_dict=Falseconfig.return_dict=False

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.torch.FloatTensor(batch_size, sequence_length, config.vocab_size)

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state

past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[torch.FloatTensor]use_cache=Trueconfig.use_cache=Truetorch.FloatTensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)

Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .torch.FloatTensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores

retrieved_doc_ids ( of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.torch.LongTensor(batch_size, config.n_docs)

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)

context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids

question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)

question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)

generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_cross_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Cross-attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the cross-attention heads.


The RagModel forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

Example:

Copied
from transformers import AutoTokenizer, RagRetriever, RagModel
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-token-base")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-base", index_name="exact", use_dummy_dataset=True
)
# initialize with RagRetriever to do everything in one forward call
model = RagModel.from_pretrained("facebook/rag-token-base", retriever=retriever)

inputs = tokenizer("How many people live in Paris?", return_tensors="pt")
outputs = model(input_ids=inputs["input_ids"])
RagSequenceForGeneration
class transformers.RagSequenceForGeneration
<
source
>
( config: typing.Optional[transformers.configuration_utils.PretrainedConfig] = Nonequestion_encoder: typing.Optional[transformers.modeling_utils.PreTrainedModel] = Nonegenerator: typing.Optional[transformers.modeling_utils.PreTrainedModel] = Noneretriever: typing.Optional[transformers.models.rag.retrieval_rag.RagRetriever] = None**kwargs )

Parameters

config (PretrainedConfig, optional) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the from_pretrained() method to load the model weights.
question_encoder (, optional) — The model responsible for encoding the question into hidden states for retrieval.PreTrainedModel
generator (, optional) — The model responsible for generating text based on retrieved documents.PreTrainedModel
retriever (, optional) — The component responsible for retrieving documents from a knowledge base given the encoded question.RagRetriever
A RAG-sequence model implementation. It performs RAG-sequence specific marginalization in the forward pass.

This model inherits from PreTrainedModel. Check the superclass documentation for the generic methods the library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads etc.)

This model is also a PyTorch torch.nn.Module subclass. Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage and behavior.

forward
<
source
>
( input_ids: typing.Optional[torch.LongTensor] = Noneattention_mask: typing.Optional[torch.Tensor] = Noneencoder_outputs: typing.Optional[tuple[tuple[torch.Tensor]]] = Nonedecoder_input_ids: typing.Optional[torch.LongTensor] = Nonedecoder_attention_mask: typing.Optional[torch.BoolTensor] = Nonepast_key_values: typing.Optional[tuple[tuple[torch.Tensor]]] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Noneuse_cache: typing.Optional[bool] = Noneoutput_attentions: typing.Optional[bool] = Noneoutput_hidden_states: typing.Optional[bool] = Noneoutput_retrieved: typing.Optional[bool] = Noneexclude_bos_score: typing.Optional[bool] = Nonereduce_loss: typing.Optional[bool] = Nonelabels: typing.Optional[torch.LongTensor] = Nonen_docs: typing.Optional[int] = None**kwargs ) → transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput or tuple(torch.FloatTensor)

Parameters

input_ids ( of shape ) — Indices of input sequence tokens in the vocabulary. RagConfig, used to initialize the model, specifies which generator to use, it also specifies a compatible generator tokenizer. Use that tokenizer class to obtain the indices.torch.LongTensor(batch_size, sequence_length)
What are input IDs?

attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :torch.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

encoder_outputs (, optional) — Tuple consists of (, optional: , optional: ). of shape is a sequence of hidden-states at the output of the last layer of the generator’s encoder.tuple(tuple(torch.FloatTensor)generator_enc_last_hidden_stategenerator_enc_hidden_statesgenerator_enc_attentionsgenerator_enc_last_hidden_state(batch_size, n_docs * sequence_length, hidden_size)
Used by the (RagModel) model during decoding.

decoder_input_ids ( of shape , optional) — Provide for generation tasks. by default, construct as per instructions for the generator model you’re using with your RAG instance.torch.LongTensor(batch_size, target_sequence_length)None
decoder_input_ids ( of shape , optional) — Indices of decoder input sequence tokens in the vocabulary.torch.LongTensor(batch_size, target_sequence_length)
Indices can be obtained using AutoTokenizer. See PreTrainedTokenizer.encode() and PreTrainedTokenizer.call() for details.

What are decoder input IDs?

decoder_attention_mask ( of shape , optional) — Default behavior: generate a tensor that ignores pad tokens in . Causal mask will also be used by default.torch.BoolTensor(batch_size, target_sequence_length)decoder_input_ids
past_key_values (, optional) — Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in the returned by the model at a previous stage of decoding, when or .tuple[tuple[torch.Tensor]]past_key_valuesuse_cache=Trueconfig.use_cache=True
Two formats are allowed:

a Cache instance, see our kv cache guide;
Tuple of of length , with each tuple having 2 tensors of shape ). This is also known as the legacy cache format.tuple(torch.FloatTensor)config.n_layers(batch_size, num_heads, sequence_length, embed_size_per_head)
The model will output the same cache format that is fed as input. If no are passed, the legacy cache format will be returned.past_key_values

If are used, the user can optionally input only the last (those that don’t have their past key value states given to this model) of shape instead of all of shape .past_key_valuesinput_ids(batch_size, 1)input_ids(batch_size, sequence_length)

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever. If the model was not initialized with a ` has to be provided to the forward pass. are returned by .torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrievercontext_input_idscontext_input_ids__call__()
context_attention_mask ( of shape ,optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever. If the model has is not initialized with a has to be provided to the forward pass. are returned by .torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrievercontext_attention_maskcontext_attention_mask__call__()
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a has to be provided to the forward pass. can be computed via and , see examples for more information.torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverdoc_scoresdoc_scoresquestion_encoder_last_hidden_stateretrieved_doc_embeds
use_cache (, optional) — If set to , key value states are returned and can be used to speed up decoding (see ).boolTruepast_key_valuespast_key_values
output_attentions (, optional) — Whether or not to return the attentions tensors of all attention layers. See under returned tensors for more detail.boolattentions
output_hidden_states (, optional) — Whether or not to return the hidden states of all layers. See under returned tensors for more detail.boolhidden_states
output_retrieved (, optional) — Whether or not to return the , , and . See returned tensors for more detail.boolretrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
exclude_bos_score (, optional) — Only relevant if is passed. If , the score of the BOS token is disregarded when computing the loss.boollabelsTrue
reduce_loss (, optional) — Only relevant if is passed. If , the NLL loss is reduced using the operation.boollabelsTruetorch.Tensor.sum
labels ( of shape , optional) — Labels for computing the masked language modeling loss. Indices should either be in or -100 (see docstring). Tokens with indices set to are ignored (masked), the loss is only computed for the tokens with labels in .torch.LongTensor(batch_size, sequence_length)[0, ..., config.vocab_size]input_ids-100[0, ..., config.vocab_size]
n_docs (, optional) — The number of documents to retrieve.int
Returns

transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput or tuple(torch.FloatTensor)

A transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput or a tuple of (if is passed or when ) comprising various elements depending on the configuration (RagConfig) and inputs.torch.FloatTensorreturn_dict=Falseconfig.return_dict=False

loss ( of shape , optional, returned when is provided) — Language modeling loss.torch.FloatTensor(1,)labels

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.torch.FloatTensor(batch_size, sequence_length, config.vocab_size)

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state

past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[torch.FloatTensor]use_cache=Trueconfig.use_cache=Truetorch.FloatTensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)

Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .torch.FloatTensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores

retrieved_doc_ids ( of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.torch.LongTensor(batch_size, config.n_docs)

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)

context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids

question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)

question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)

generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_cross_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Cross-attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the cross-attention heads.


The RagSequenceForGeneration forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

Example:

Copied
from transformers import AutoTokenizer, RagRetriever, RagSequenceForGeneration
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-sequence-nq")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-sequence-nq", index_name="exact", use_dummy_dataset=True
)
# initialize with RagRetriever to do everything in one forward call
model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

inputs = tokenizer("How many people live in Paris?", return_tensors="pt")
targets = tokenizer(text_target="In Paris, there are 10 million people.", return_tensors="pt")
input_ids = inputs["input_ids"]
labels = targets["input_ids"]
outputs = model(input_ids=input_ids, labels=labels)

# or use retriever separately
model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq", use_dummy_dataset=True)
# 1. Encode
question_hidden_states = model.question_encoder(input_ids)[0]
# 2. Retrieve
docs_dict = retriever(input_ids.numpy(), question_hidden_states.detach().numpy(), return_tensors="pt")
doc_scores = torch.bmm(
    question_hidden_states.unsqueeze(1), docs_dict["retrieved_doc_embeds"].float().transpose(1, 2)
).squeeze(1)
# 3. Forward to generator
outputs = model(
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
    decoder_input_ids=labels,
)
generate
<
source
>
( input_ids: typing.Optional[torch.LongTensor] = Noneattention_mask: typing.Optional[torch.LongTensor] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Nonedo_deduplication: typing.Optional[bool] = Nonenum_return_sequences: typing.Optional[int] = Nonenum_beams: typing.Optional[int] = Nonen_docs: typing.Optional[int] = None**model_kwargs ) → torch.LongTensor of shape (batch_size * num_return_sequences, sequence_length)

Parameters

input_ids ( of shape , optional) — The sequence used as a prompt for the generation. If is not passed, then has to be provided.torch.LongTensor(batch_size, sequence_length)input_idscontext_input_ids
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :torch.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder input_ids by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)
context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model is not initialized with a or is not given, and have to be provided to the forward pass. They are returned by .retrieverinput_idscontext_input_idscontext_attention_mask__call__()

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state
If the model is not initialized with a or is not given, has to be provided to the forward pass. are returned by .retrieverinput_idsdoc_scoresdoc_scores__call__()

do_deduplication (, optional) — Whether or not to deduplicate the generations from different context documents for a given input. Has to be set to if used while training with distributed backend.boolFalse
num_return_sequences(int, optional, defaults to 1) — The number of independently computed returned sequences for each element in the batch. Note that this is not the value we pass to the ’s function, where we set to .generator[generate()](/docs/transformers/v4.53.3/en/main_classes/text_generation#transformers.GenerationMixin.generate)num_return_sequencesnum_beams
num_beams (, optional, defaults to 1) — Number of beams for beam search. 1 means no beam search.int
n_docs (, optional, defaults to ) — Number of documents to retrieve and/or number of documents for which to generate an answer.intconfig.n_docs
kwargs (, optional) — Additional kwargs will be passed to generate().dict[str, Any]
Returns

torch.LongTensor of shape (batch_size * num_return_sequences, sequence_length)

The generated sequences. The second dimension (sequence length) is either equal to or shorter if all batches finished early due to the .max_lengtheos_token_id


Implements RAG sequence “thorough” decoding. Read the generate()` documentation for more information on how to set other generate input parameters.

RagTokenForGeneration
class transformers.RagTokenForGeneration
<
source
>
( config: typing.Optional[transformers.configuration_utils.PretrainedConfig] = Nonequestion_encoder: typing.Optional[transformers.modeling_utils.PreTrainedModel] = Nonegenerator: typing.Optional[transformers.modeling_utils.PreTrainedModel] = Noneretriever: typing.Optional[transformers.models.rag.retrieval_rag.RagRetriever] = None**kwargs )

Parameters

config (PretrainedConfig, optional) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the from_pretrained() method to load the model weights.
question_encoder (, optional) — The model responsible for encoding the question into hidden states for retrieval.PreTrainedModel
generator (, optional) — The model responsible for generating text based on retrieved documents.PreTrainedModel
retriever (, optional) — The component responsible for retrieving documents from a knowledge base given the encoded question.RagRetriever
A RAG-token model implementation. It performs RAG-token specific marginalization in the forward pass.

This model inherits from PreTrainedModel. Check the superclass documentation for the generic methods the library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads etc.)

This model is also a PyTorch torch.nn.Module subclass. Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage and behavior.

forward
<
source
>
( input_ids: typing.Optional[torch.LongTensor] = Noneattention_mask: typing.Optional[torch.FloatTensor] = Noneencoder_outputs: typing.Optional[tuple[tuple[torch.Tensor]]] = Nonedecoder_input_ids: typing.Optional[torch.LongTensor] = Nonedecoder_attention_mask: typing.Optional[torch.BoolTensor] = Nonepast_key_values: typing.Optional[tuple[tuple[torch.Tensor]]] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Noneuse_cache: typing.Optional[bool] = Noneoutput_attentions: typing.Optional[bool] = Noneoutput_hidden_states: typing.Optional[bool] = Noneoutput_retrieved: typing.Optional[bool] = Nonedo_marginalize: typing.Optional[bool] = Nonereduce_loss: typing.Optional[bool] = Nonelabels: typing.Optional[torch.LongTensor] = Nonen_docs: typing.Optional[int] = None**kwargs ) → transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput or tuple(torch.FloatTensor)

Parameters

input_ids ( of shape ) — Indices of input sequence tokens in the vocabulary. RagConfig, used to initialize the model, specifies which generator to use, it also specifies a compatible generator tokenizer. Use that tokenizer class to obtain the indices.torch.LongTensor(batch_size, sequence_length)
What are input IDs?

attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :torch.FloatTensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

encoder_outputs (, optional) — Tuple consists of (, optional: , optional: ). of shape is a sequence of hidden-states at the output of the last layer of the generator’s encoder.tuple(tuple(torch.FloatTensor)generator_enc_last_hidden_stategenerator_enc_hidden_statesgenerator_enc_attentionsgenerator_enc_last_hidden_state(batch_size, n_docs * sequence_length, hidden_size)
Used by the (RagModel) model during decoding.

decoder_input_ids ( of shape , optional) — Provide for generation tasks. by default, construct as per instructions for the generator model you’re using with your RAG instance.torch.LongTensor(batch_size, target_sequence_length)None
decoder_input_ids ( of shape , optional) — Indices of decoder input sequence tokens in the vocabulary.torch.LongTensor(batch_size, target_sequence_length)
Indices can be obtained using AutoTokenizer. See PreTrainedTokenizer.encode() and PreTrainedTokenizer.call() for details.

What are decoder input IDs?

decoder_attention_mask ( of shape , optional) — Default behavior: generate a tensor that ignores pad tokens in . Causal mask will also be used by default.torch.BoolTensor(batch_size, target_sequence_length)decoder_input_ids
past_key_values (, optional) — Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention blocks) that can be used to speed up sequential decoding. This typically consists in the returned by the model at a previous stage of decoding, when or .tuple[tuple[torch.Tensor]]past_key_valuesuse_cache=Trueconfig.use_cache=True
Two formats are allowed:

a Cache instance, see our kv cache guide;
Tuple of of length , with each tuple having 2 tensors of shape ). This is also known as the legacy cache format.tuple(torch.FloatTensor)config.n_layers(batch_size, num_heads, sequence_length, embed_size_per_head)
The model will output the same cache format that is fed as input. If no are passed, the legacy cache format will be returned.past_key_values

If are used, the user can optionally input only the last (those that don’t have their past key value states given to this model) of shape instead of all of shape .past_key_valuesinput_ids(batch_size, 1)input_ids(batch_size, sequence_length)

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever. If the model was not initialized with a ` has to be provided to the forward pass. are returned by .torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrievercontext_input_idscontext_input_ids__call__()
context_attention_mask ( of shape ,optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever. If the model has is not initialized with a has to be provided to the forward pass. are returned by .torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrievercontext_attention_maskcontext_attention_mask__call__()
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a has to be provided to the forward pass. can be computed via and , see examples for more information.torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverdoc_scoresdoc_scoresquestion_encoder_last_hidden_stateretrieved_doc_embeds
use_cache (, optional) — If set to , key value states are returned and can be used to speed up decoding (see ).boolTruepast_key_valuespast_key_values
output_attentions (, optional) — Whether or not to return the attentions tensors of all attention layers. See under returned tensors for more detail.boolattentions
output_hidden_states (, optional) — Whether or not to return the hidden states of all layers. See under returned tensors for more detail.boolhidden_states
output_retrieved (, optional) — Whether or not to return the , , and . See returned tensors for more detail.boolretrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
do_marginalize (, optional) — If , the logits are marginalized over all documents by making use of .boolTruetorch.nn.functional.log_softmax
reduce_loss (, optional) — Only relevant if is passed. If , the NLL loss is reduced using the operation.boollabelsTruetorch.Tensor.sum
labels ( of shape , optional) — Labels for computing the masked language modeling loss. Indices should either be in or -100 (see docstring). Tokens with indices set to are ignored (masked), the loss is only computed for the tokens with labels in .torch.LongTensor(batch_size, sequence_length)[0, ..., config.vocab_size]input_ids-100[0, ..., config.vocab_size]
n_docs (, optional) — The number of documents to retrieve.int
Returns

transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput or tuple(torch.FloatTensor)

A transformers.models.rag.modeling_rag.RetrievAugLMMarginOutput or a tuple of (if is passed or when ) comprising various elements depending on the configuration (RagConfig) and inputs.torch.FloatTensorreturn_dict=Falseconfig.return_dict=False

loss ( of shape , optional, returned when is provided) — Language modeling loss.torch.FloatTensor(1,)labels

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.torch.FloatTensor(batch_size, sequence_length, config.vocab_size)

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state

past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[torch.FloatTensor]use_cache=Trueconfig.use_cache=Truetorch.FloatTensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)

Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .torch.FloatTensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores

retrieved_doc_ids ( of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.torch.LongTensor(batch_size, config.n_docs)

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)

context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids

question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)

question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.torch.FloatTensor(batch_size, sequence_length, hidden_size)

generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(torch.FloatTensor)output_hidden_states=Trueconfig.output_hidden_states=Truetorch.FloatTensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_cross_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(torch.FloatTensor)output_attentions=Trueconfig.output_attentions=Truetorch.FloatTensor(batch_size, num_heads, sequence_length, sequence_length)

Cross-attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the cross-attention heads.


The RagTokenForGeneration forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

Example:

Copied
from transformers import AutoTokenizer, RagRetriever, RagTokenForGeneration
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True
)
# initialize with RagRetriever to do everything in one forward call
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

inputs = tokenizer("How many people live in Paris?", return_tensors="pt")
targets = tokenizer(text_target="In Paris, there are 10 million people.", return_tensors="pt")
input_ids = inputs["input_ids"]
labels = targets["input_ids"]
outputs = model(input_ids=input_ids, labels=labels)

# or use retriever separately
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", use_dummy_dataset=True)
# 1. Encode
question_hidden_states = model.question_encoder(input_ids)[0]
# 2. Retrieve
docs_dict = retriever(input_ids.numpy(), question_hidden_states.detach().numpy(), return_tensors="pt")
doc_scores = torch.bmm(
    question_hidden_states.unsqueeze(1), docs_dict["retrieved_doc_embeds"].float().transpose(1, 2)
).squeeze(1)
# 3. Forward to generator
outputs = model(
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
    decoder_input_ids=labels,
)

# or directly generate
generated = model.generate(
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
)
generated_string = tokenizer.batch_decode(generated, skip_special_tokens=True)
generate
<
source
>
( input_ids: typing.Optional[torch.LongTensor] = Noneattention_mask: typing.Optional[torch.LongTensor] = Nonecontext_input_ids: typing.Optional[torch.LongTensor] = Nonecontext_attention_mask: typing.Optional[torch.LongTensor] = Nonedoc_scores: typing.Optional[torch.FloatTensor] = Nonen_docs: typing.Optional[int] = Nonegeneration_config: typing.Optional[transformers.generation.configuration_utils.GenerationConfig] = Noneprefix_allowed_tokens_fn: typing.Optional[typing.Callable[[int, torch.Tensor], list[int]]] = Nonelogits_processor: typing.Optional[transformers.generation.logits_process.LogitsProcessorList] = []stopping_criteria: typing.Optional[transformers.generation.stopping_criteria.StoppingCriteriaList] = []**kwargs ) → torch.LongTensor of shape (batch_size * num_return_sequences, sequence_length)

Parameters

input_ids ( of shape , optional) — The sequence used as a prompt for the generation. If is not passed, then has to be provided.torch.LongTensor(batch_size, sequence_length)input_idscontext_input_ids
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :torch.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a , has to be provided to the forward pass. are returned by .retrievercontext_input_idscontext_input_ids__call__()

context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.torch.LongTensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a , has to be provided to the forward pass. are returned by .retrievercontext_input_idscontext_input_ids__call__()

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .torch.FloatTensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state
If the model has is not initialized with a , has to be provided to the forward pass. are returned by .retrievercontext_input_idscontext_input_ids__call__()

n_docs (, optional, defaults to ) — Number of documents to retrieve and/or number of documents for which to generate an answer.intconfig.n_docs
generation_config (, optional) — The generation configuration to be used as base parametrization for the generation call. passed to generate matching the attributes of will override them. If is not provided, the default will be used, which has the following loading priority: 1) from the model file, if it exists; 2) from the model configuration. Please note that unspecified parameters will inherit GenerationConfig’s default values, whose documentation should be checked to parameterize generation.~generation.GenerationConfig**kwargsgeneration_configgeneration_configgeneration_config.json
prefix_allowed_tokens_fn (, optional) — If provided, this function constraints the beam search to allowed tokens only at each step. If not provided no constraint is applied. This function takes 2 arguments and the batch ID . It has to return a list with the allowed tokens for the next generation step conditioned on the previously generated tokens and the batch ID . This argument is useful for constrained generation conditioned on the prefix, as described in Autoregressive Entity Retrieval.Callable[[int, torch.Tensor], list[int]]inputs_idsbatch_idinputs_idsbatch_id
logits_processor (, optional) — Custom logits processors that complement the default logits processors built from arguments and a model’s config. If a logit processor is passed that is already created with the arguments or a model’s config an error is thrown.LogitsProcessorList
stopping_criteria (, optional) — Custom stopping criteria that complement the default stopping criteria built from arguments and a model’s config. If a stopping criteria is passed that is already created with the arguments or a model’s config an error is thrown.StoppingCriteriaList
kwargs (, optional) — Ad hoc parametrization of and/or additional model-specific kwargs that will be forwarded to the function of the model.dict[str, Any]generate_configforward
Returns

torch.LongTensor of shape (batch_size * num_return_sequences, sequence_length)

The generated sequences. The second dimension (sequence_length) is either equal to or shorter if all batches finished early due to the .max_lengtheos_token_id


Implements RAG token decoding.

TensorFlow
Hide TensorFlow content
TFRagModel
class transformers.TFRagModel
<
source
>
( config: Optional[PretrainedConfig] = Nonequestion_encoder: Optional[TFPreTrainedModel] = Nonegenerator: Optional[TFPreTrainedModel] = Noneretriever: Optional[RagRetriever] = Noneload_weight_prefix: Optional[str] = None**kwargs )

Parameters

config (RagConfig) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the from_pretrained() method to load the model weights.
question_encoder (TFPreTrainedModel) — An encoder model compatible with the faiss index encapsulated by the .retriever
generator (TFPreTrainedModel) — A seq2seq model used as the generator in the RAG architecture.
retriever (RagRetriever) — A retriever class encapsulating a faiss index queried to obtain context documents for current inputs.
The TFRagModel forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

RAG is a sequence-to-sequence model which encapsulates two core components: a question encoder and a generator. During a forward pass, we encode the input with the question encoder and pass it to the retriever to extract relevant context documents. The documents are then prepended to the input. Such contextualized inputs is passed to the generator.

The question encoder can be any autoencoding model, preferably TFDPRQuestionEncoder, and the generator can be any seq2seq model, preferably TFBartForConditionalGeneration.

The model can be initialized with a RagRetriever for end-to-end generation or used in combination with the outputs of a retriever in multiple steps---see examples for more details. The model is compatible any autoencoding model as the and any seq2seq model with language model head as the . It has been tested with TFDPRQuestionEncoder as the and TFBartForConditionalGeneration as the .question_encodergeneratorquestion_encodergenerator

This model inherits from TFPreTrainedModel. Check the superclass documentation for the generic methods the library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads etc.)

This model is also a Tensorflow keras.Model subclass. Use it as a regular TF 2.0 Keras Model and refer to the TF 2.0 documentation for all matter related to general usage and behavior.

The model is in a developing state as it is now fully supports in eager-mode only, and may not be exported in SavedModel format.

call
<
source
>
( input_ids: TFModelInputType | None = Noneattention_mask: np.ndarray | tf.Tensor | None = Noneencoder_outputs: np.ndarray | tf.Tensor | None = Nonedecoder_input_ids: np.ndarray | tf.Tensor | None = Nonedecoder_attention_mask: np.ndarray | tf.Tensor | None = Nonepast_key_values: tuple[tuple[Union[np.ndarray, tf.Tensor]]] | None = Nonedoc_scores: np.ndarray | tf.Tensor | None = Nonecontext_input_ids: np.ndarray | tf.Tensor | None = Nonecontext_attention_mask: np.ndarray | tf.Tensor | None = Noneuse_cache: bool | None = Noneoutput_attentions: bool | None = Noneoutput_hidden_states: bool | None = Noneoutput_retrieved: bool | None = Nonen_docs: int | None = Nonereturn_dict: bool | None = Nonetraining: bool = False**kwargs ) → transformers.models.rag.modeling_tf_rag.TFRetrievAugLMOutput or tuple(tf.Tensor)

Parameters

input_ids ( of shape ) — Indices of input sequence tokens in the vocabulary. RagConfig, used to initialize the model, specifies which generator to use, it also specifies a compatible generator tokenizer. Use that tokenizer class to obtain the indices.tf.Tensor(batch_size, sequence_length)
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :tf.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

encoder_outputs (, optional) — Tuple consists of (, optional: , optional: ). of shape is a sequence of hidden-states at the output of the last layer of the generator’s encoder.tuple(tuple(tf.Tensor)generator_enc_last_hidden_stategenerator_enc_hidden_statesgenerator_enc_attentionsgenerator_enc_last_hidden_state(batch_size, n_docs * sequence_length, hidden_size)
Used by the (TFRagModel) model during decoding.

decoder_input_ids ( of shape , optional) — Provide for generation tasks. by default, construct as per instructions for the generator model you’re using with your RAG instance.tf.Tensor(batch_size, target_sequence_length)None
decoder_attention_mask ( of shape , optional) — Default behavior: generate a tensor that ignores pad tokens in . Causal mask will also be used by default.torch.BoolTensor(batch_size, target_sequence_length)decoder_input_ids
past_key_values () — Tuple consists of two elements: of the RAG model (see ) and of the underlying generator. Can be used to speed up decoding. are used in the (RagTokenForGeneration) model during decoding.tuple(tuple(tf.Tensor))encoder_outputsencoder_outputspast_key_valuespast_key_values
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a has to be provided to the forward pass. can be computed via and , see examples for more information.tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverdoc_scoresdoc_scoresquestion_encoder_last_hidden_stateretrieved_doc_embeds
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a ` has to be provided to the forward pass. are returned by . context_attention_mask ( of shape , optional, returned when output_retrieved=True): Attention mask post-processed from the retrieved documents and the question encoder by the retriever.retrievercontext_input_idscontext_input_ids__call__()tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids

If the model has is not initialized with a has to be provided to the forward pass. are returned by .retrievercontext_attention_maskcontext_attention_mask__call__()

use_cache (, optional, defaults to ) — If set to , key value states are returned and can be used to speed up decoding (see ).boolTrueTruepast_key_valuespast_key_values
output_attentions (, optional) — Whether or not to return the attentions tensors of all attention layers. See under returned tensors for more detail.boolattentions
output_hidden_states (, optional) — Whether or not to return the hidden states of all layers. See under returned tensors for more detail.boolhidden_states
output_retrieved(bool, optional) — Whether or not to return the , , and . See returned tensors for more detail.retrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
return_dict (, optional) — Whether or not to return a instead of a plain tuple.boolTFRetrievAugLMOutput
n_docs (, optional, defaults to `config.n_docs“) — Number of documents to retrieve and/or number of documents for which to generate an answer.int
Returns

transformers.models.rag.modeling_tf_rag.TFRetrievAugLMOutput or tuple(tf.Tensor)

A or a tuple of (if is passed or when ) comprising various elements depending on the configuration (RagConfig) and inputs.transformers.models.rag.modeling_tf_rag.TFRetrievAugLMOutputtf.Tensorreturn_dict=Falseconfig.return_dict=False

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.tf.Tensor(batch_size, sequence_length, config.vocab_size)

past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[tf.Tensor]use_cache=Trueconfig.use_cache=Truetf.Tensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)

Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .tf.Tensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores

retrieved_doc_ids ( of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.tf.Tensor(batch_size, config.n_docs)

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)

context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids

question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.tf.Tensor(batch_size, sequence_length, hidden_size)

question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.tf.Tensor(batch_size, sequence_length, hidden_size)

generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.


The TFRagModel forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

Example:

Copied
from transformers import AutoTokenizer, RagRetriever, TFRagModel
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-token-base")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-base", index_name="exact", use_dummy_dataset=True
)
# initialize with RagRetriever to do everything in one forward call
model = TFRagModel.from_pretrained("facebook/rag-token-base", retriever=retriever, from_pt=True)

input_dict = tokenizer.prepare_seq2seq_batch(
    "How many people live in Paris?", "In Paris, there are 10 million people.", return_tensors="tf"
)
input_ids = input_dict["input_ids"]
outputs = model(input_ids)
TFRagSequenceForGeneration
class transformers.TFRagSequenceForGeneration
<
source
>
( config: Optional[PretrainedConfig] = Nonequestion_encoder: Optional[TFPreTrainedModel] = Nonegenerator: Optional[TFPreTrainedModel] = Noneretriever: Optional[RagRetriever] = None**kwargs )

Parameters

config (RagConfig) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the from_pretrained() method to load the model weights.
question_encoder (TFPreTrainedModel) — An encoder model compatible with the faiss index encapsulated by the .retriever
generator (TFPreTrainedModel) — A seq2seq model used as the generator in the RAG architecture.
retriever (RagRetriever) — A retriever class encapsulating a faiss index queried to obtain context documents for current inputs.
The TFRagSequenceForGeneration forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

A TF RAG-sequence model implementation. It performs RAG-sequence specific marginalization in the forward pass.

RAG is a sequence-to-sequence model which encapsulates two core components: a question encoder and a generator. During a forward pass, we encode the input with the question encoder and pass it to the retriever to extract relevant context documents. The documents are then prepended to the input. Such contextualized inputs is passed to the generator.

The question encoder can be any autoencoding model, preferably TFDPRQuestionEncoder, and the generator can be any seq2seq model, preferably TFBartForConditionalGeneration.

The model can be initialized with a RagRetriever for end-to-end generation or used in combination with the outputs of a retriever in multiple steps---see examples for more details. The model is compatible any autoencoding model as the and any seq2seq model with language model head as the . It has been tested with TFDPRQuestionEncoder as the and TFBartForConditionalGeneration as the .question_encodergeneratorquestion_encodergenerator

This model inherits from TFPreTrainedModel. Check the superclass documentation for the generic methods the library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads etc.)

This model is also a Tensorflow keras.Model subclass. Use it as a regular TF 2.0 Keras Model and refer to the TF 2.0 documentation for all matter related to general usage and behavior.

The model is in a developing state as it is now fully supports in eager-mode only, and may not be exported in SavedModel format.

call
<
source
>
( input_ids: TFModelInputType | None = Noneattention_mask: np.ndarray | tf.Tensor | None = Nonedecoder_input_ids: np.ndarray | tf.Tensor | None = Nonedecoder_attention_mask: np.ndarray | tf.Tensor | None = Noneencoder_outputs: np.ndarray | tf.Tensor | None = Nonepast_key_values: Optional[tuple[tuple[Union[np.ndarray, tf.Tensor]]]] = Nonedoc_scores: np.ndarray | tf.Tensor | None = Nonecontext_input_ids: np.ndarray | tf.Tensor | None = Nonecontext_attention_mask: np.ndarray | tf.Tensor | None = Noneuse_cache: Optional[bool] = Noneoutput_attentions: Optional[bool] = Noneoutput_hidden_states: Optional[bool] = Noneoutput_retrieved: Optional[bool] = Nonen_docs: Optional[int] = Noneexclude_bos_score: Optional[bool] = Nonelabels: np.ndarray | tf.Tensor | None = Nonereduce_loss: Optional[bool] = Nonereturn_dict: Optional[bool] = Nonetraining: bool = False**kwargs ) → transformers.models.rag.modeling_tf_rag.TFRetrievAugLMMarginOutput or tuple(tf.Tensor)

Parameters

input_ids ( of shape ) — Indices of input sequence tokens in the vocabulary. RagConfig, used to initialize the model, specifies which generator to use, it also specifies a compatible generator tokenizer. Use that tokenizer class to obtain the indices.tf.Tensor(batch_size, sequence_length)
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :tf.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

encoder_outputs (, optional) — Tuple consists of (, optional: , optional: ). of shape is a sequence of hidden-states at the output of the last layer of the generator’s encoder.tuple(tuple(tf.Tensor)generator_enc_last_hidden_stategenerator_enc_hidden_statesgenerator_enc_attentionsgenerator_enc_last_hidden_state(batch_size, n_docs * sequence_length, hidden_size)
Used by the (TFRagModel) model during decoding.

decoder_input_ids ( of shape , optional) — Provide for generation tasks. by default, construct as per instructions for the generator model you’re using with your RAG instance.tf.Tensor(batch_size, target_sequence_length)None
decoder_attention_mask ( of shape , optional) — Default behavior: generate a tensor that ignores pad tokens in . Causal mask will also be used by default.torch.BoolTensor(batch_size, target_sequence_length)decoder_input_ids
past_key_values () — Tuple consists of two elements: of the RAG model (see ) and of the underlying generator. Can be used to speed up decoding. are used in the (RagTokenForGeneration) model during decoding.tuple(tuple(tf.Tensor))encoder_outputsencoder_outputspast_key_valuespast_key_values
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a has to be provided to the forward pass. can be computed via and , see examples for more information.tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverdoc_scoresdoc_scoresquestion_encoder_last_hidden_stateretrieved_doc_embeds
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a ` has to be provided to the forward pass. are returned by . context_attention_mask ( of shape , optional, returned when output_retrieved=True): Attention mask post-processed from the retrieved documents and the question encoder by the retriever.retrievercontext_input_idscontext_input_ids__call__()tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids

If the model has is not initialized with a has to be provided to the forward pass. are returned by .retrievercontext_attention_maskcontext_attention_mask__call__()

use_cache (, optional, defaults to ) — If set to , key value states are returned and can be used to speed up decoding (see ).boolTrueTruepast_key_valuespast_key_values
output_attentions (, optional) — Whether or not to return the attentions tensors of all attention layers. See under returned tensors for more detail.boolattentions
output_hidden_states (, optional) — Whether or not to return the hidden states of all layers. See under returned tensors for more detail.boolhidden_states
output_retrieved(bool, optional) — Whether or not to return the , , and . See returned tensors for more detail.retrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
return_dict (, optional) — Whether or not to return a instead of a plain tuple.boolTFRetrievAugLMOutput
n_docs (, optional, defaults to `config.n_docs“) — Number of documents to retrieve and/or number of documents for which to generate an answer.int
exclude_bos_score (, optional) — Only relevant if is passed. If , the score of the BOS token is disregarded when computing the loss.boollabelsTrue
labels ( or of shape , optional) — Labels for computing the cross entropy classification loss according to Rag-Sequence model formulation See https://huggingface.co/papers/2005.11401 Section 2.1 for details about Rag-Sequence formulation. Indices should be in .tf.Tensornp.ndarray(batch_size, sequence_length)[0, ..., config.vocab_size - 1]
reduce_loss (, optional) — Only relevant if is passed. If , the NLL loss is reduced using the operation.boollabelsTruetf.Tensor.sum
kwargs (, optional, defaults to ) — Legacy dictionary, which is required so that model can use generate() function.dict[str, any]{}
Returns

transformers.models.rag.modeling_tf_rag.TFRetrievAugLMMarginOutput or tuple(tf.Tensor)

A or a tuple of (if is passed or when ) comprising various elements depending on the configuration (RagConfig) and inputs.transformers.models.rag.modeling_tf_rag.TFRetrievAugLMMarginOutputtf.Tensorreturn_dict=Falseconfig.return_dict=False

loss ( of shape , optional, returned when is provided) — Language modeling loss.tf.Tensor(1,)labels

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.tf.Tensor(batch_size, sequence_length, config.vocab_size)

past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[tf.Tensor]use_cache=Trueconfig.use_cache=Truetf.Tensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)

Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .tf.Tensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores

retrieved_doc_ids ( (int32) of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.tf.Tensor(batch_size, config.n_docs)

context_input_ids ((int32) of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)

context_attention_mask ( (int32) of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids

question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.tf.Tensor(batch_size, sequence_length, hidden_size)

question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.tf.Tensor(batch_size, sequence_length, hidden_size)

generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.


The TFRagSequenceForGeneration forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

Example:

Copied
from transformers import AutoTokenizer, RagRetriever, TFRagSequenceForGeneration

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-sequence-nq")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-sequence-nq", index_name="exact", use_dummy_dataset=True
)
# initialize with RagRetriever to do everything in one forward call
model = TFRagSequenceForGeneration.from_pretrained(
    "facebook/rag-sequence-nq", retriever=retriever, from_pt=True
)

input_dict = tokenizer.prepare_seq2seq_batch(
    "How many people live in Paris?", "In Paris, there are 10 million people.", return_tensors="tf"
)
outputs = model(input_dict, output_retrieved=True)

# or use retriever separately
# 1. Encode
input_ids = input_dict["input_ids"]
question_hidden_states = model.question_encoder(input_ids)[0]
# 2. Retrieve
docs_dict = retriever(input_ids.numpy(), question_hidden_states.numpy(), return_tensors="tf")
doc_scores = tf.squeeze(
    tf.matmul(
        tf.expand_dims(question_hidden_states, axis=1), docs_dict["retrieved_doc_embeds"], transpose_b=True
    ),
    axis=1,
)
# 3. Forward to generator
outputs = model(
    inputs=None,
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
    decoder_input_ids=input_dict["labels"],
)

# or directly generate
generated = model.generate(
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
)
generated_string = tokenizer.batch_decode(generated, skip_special_tokens=True)
generate
<
source
>
( input_ids: TFModelInputType | None = Noneattention_mask: tf.Tensor | None = Nonecontext_input_ids = Nonecontext_attention_mask = Nonedoc_scores = Nonedo_deduplication = Nonenum_return_sequences = Nonenum_beams = Nonen_docs = None**model_kwargs ) → tf.Tensor of shape (batch_size * num_return_sequences, sequence_length)

Parameters

input_ids ( of shape , optional) — The sequence used as a prompt for the generation. If is not passed, then has to be provided.tf.Tensor(batch_size, sequence_length)input_idscontext_input_ids
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in : - 1 for tokens that are not masked, - 0 for tokens that are masked. What are attention masks?tf.Tensor(batch_size, sequence_length)[0, 1]
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder input_ids by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)
context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever. If the model has is not initialized with a or is not given, and have to be provided to the forward pass. They are returned by .tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_idsretrieverinput_idscontext_input_idscontext_attention_mask__call__()
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a or is not given, has to be provided to the forward pass. are returned by .tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverinput_idsdoc_scoresdoc_scores__call__()
do_deduplication (, optional) — Whether or not to deduplicate the generations from different context documents for a given input. Has to be set to if used while training with distributed backend.boolFalse
num_return_sequences(int, optional, defaults to 1) — The number of independently computed returned sequences for each element in the batch. Note that this is not the value we pass to the ’s function, where we set to .generator[generate()](/docs/transformers/v4.53.3/en/main_classes/text_generation#transformers.GenerationMixin.generate)num_return_sequencesnum_beams
num_beams (, optional, defaults to 1) — Number of beams for beam search. 1 means no beam search.int
n_docs (, optional, defaults to ) — Number of documents to retrieve and/or number of documents for which to generate an answer.intconfig.n_docs
kwargs (, optional) — Additional kwargs will be passed to generate()dict[str, Any]
Returns

tf.Tensor of shape (batch_size * num_return_sequences, sequence_length)

The generated sequences. The second dimension (sequence length) is either equal to or shorter if all batches finished early due to the .max_lengtheos_token_id


Implements RAG sequence “thorough” decoding. Read the generate()` documentation for more information on how to set other generate input parameters

TFRagTokenForGeneration
class transformers.TFRagTokenForGeneration
<
source
>
( config: Optional[PretrainedConfig] = Nonequestion_encoder: Optional[TFPreTrainedModel] = Nonegenerator: Optional[TFPreTrainedModel] = Noneretriever: Optional[RagRetriever] = None**kwargs )

Parameters

config (RagConfig) — Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the from_pretrained() method to load the model weights.
question_encoder (TFPreTrainedModel) — An encoder model compatible with the faiss index encapsulated by the .retriever
generator (TFPreTrainedModel) — A seq2seq model used as the generator in the RAG architecture.
retriever (RagRetriever) — A retriever class encapsulating a faiss index queried to obtain context documents for current inputs.
The TFRagTokenForGeneration forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

A TF RAG-token model implementation. It performs RAG-token specific marginalization in the forward pass.

RAG is a sequence-to-sequence model which encapsulates two core components: a question encoder and a generator. During a forward pass, we encode the input with the question encoder and pass it to the retriever to extract relevant context documents. The documents are then prepended to the input. Such contextualized inputs is passed to the generator.

The question encoder can be any autoencoding model, preferably TFDPRQuestionEncoder, and the generator can be any seq2seq model, preferably TFBartForConditionalGeneration.

The model can be initialized with a RagRetriever for end-to-end generation or used in combination with the outputs of a retriever in multiple steps---see examples for more details. The model is compatible any autoencoding model as the and any seq2seq model with language model head as the . It has been tested with TFDPRQuestionEncoder as the and TFBartForConditionalGeneration as the .question_encodergeneratorquestion_encodergenerator

This model inherits from TFPreTrainedModel. Check the superclass documentation for the generic methods the library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads etc.)

This model is also a Tensorflow keras.Model subclass. Use it as a regular TF 2.0 Keras Model and refer to the TF 2.0 documentation for all matter related to general usage and behavior.

The model is in a developing state as it is now fully supports in eager-mode only, and may not be exported in SavedModel format.

call
<
source
>
( input_ids: TFModelInputType | None = Noneattention_mask: np.ndarray | tf.Tensor | None = Nonedecoder_input_ids: np.ndarray | tf.Tensor | None = Nonedecoder_attention_mask: np.ndarray | tf.Tensor | None = Noneencoder_outputs: np.ndarray | tf.Tensor | None = Nonepast_key_values: tuple[tuple[Union[np.ndarray, tf.Tensor]]] | None = Nonedoc_scores: np.ndarray | tf.Tensor | None = Nonecontext_input_ids: np.ndarray | tf.Tensor | None = Nonecontext_attention_mask: np.ndarray | tf.Tensor | None = Noneuse_cache: bool | None = Noneoutput_attentions: bool | None = Noneoutput_hidden_states: bool | None = Noneoutput_retrieved: bool | None = Nonen_docs: int | None = Nonedo_marginalize: bool | None = Nonelabels: np.ndarray | tf.Tensor | None = Nonereduce_loss: bool | None = Nonereturn_dict: bool | None = Nonetraining: bool = False**kwargs ) → transformers.models.rag.modeling_tf_rag.TFRetrievAugLMMarginOutput or tuple(tf.Tensor)

Parameters

input_ids ( of shape ) — Indices of input sequence tokens in the vocabulary. RagConfig, used to initialize the model, specifies which generator to use, it also specifies a compatible generator tokenizer. Use that tokenizer class to obtain the indices.tf.Tensor(batch_size, sequence_length)
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :tf.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

encoder_outputs (, optional) — Tuple consists of (, optional: , optional: ). of shape is a sequence of hidden-states at the output of the last layer of the generator’s encoder.tuple(tuple(tf.Tensor)generator_enc_last_hidden_stategenerator_enc_hidden_statesgenerator_enc_attentionsgenerator_enc_last_hidden_state(batch_size, n_docs * sequence_length, hidden_size)
Used by the (TFRagModel) model during decoding.

decoder_input_ids ( of shape , optional) — Provide for generation tasks. by default, construct as per instructions for the generator model you’re using with your RAG instance.tf.Tensor(batch_size, target_sequence_length)None
decoder_attention_mask ( of shape , optional) — Default behavior: generate a tensor that ignores pad tokens in . Causal mask will also be used by default.torch.BoolTensor(batch_size, target_sequence_length)decoder_input_ids
past_key_values () — Tuple consists of two elements: of the RAG model (see ) and of the underlying generator. Can be used to speed up decoding. are used in the (RagTokenForGeneration) model during decoding.tuple(tuple(tf.Tensor))encoder_outputsencoder_outputspast_key_valuespast_key_values
doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and . If the model has is not initialized with a has to be provided to the forward pass. can be computed via and , see examples for more information.tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_stateretrieverdoc_scoresdoc_scoresquestion_encoder_last_hidden_stateretrieved_doc_embeds
context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a ` has to be provided to the forward pass. are returned by . context_attention_mask ( of shape , optional, returned when output_retrieved=True): Attention mask post-processed from the retrieved documents and the question encoder by the retriever.retrievercontext_input_idscontext_input_ids__call__()tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids

If the model has is not initialized with a has to be provided to the forward pass. are returned by .retrievercontext_attention_maskcontext_attention_mask__call__()

use_cache (, optional, defaults to ) — If set to , key value states are returned and can be used to speed up decoding (see ).boolTrueTruepast_key_valuespast_key_values
output_attentions (, optional) — Whether or not to return the attentions tensors of all attention layers. See under returned tensors for more detail.boolattentions
output_hidden_states (, optional) — Whether or not to return the hidden states of all layers. See under returned tensors for more detail.boolhidden_states
output_retrieved(bool, optional) — Whether or not to return the , , and . See returned tensors for more detail.retrieved_doc_embedsretrieved_doc_idscontext_input_idscontext_attention_mask
return_dict (, optional) — Whether or not to return a instead of a plain tuple.boolTFRetrievAugLMOutput
n_docs (, optional, defaults to `config.n_docs“) — Number of documents to retrieve and/or number of documents for which to generate an answer.int
do_marginalize (, optional) — If , the logits are marginalized over all documents by making use of .boolTruetorch.nn.functional.log_softmax
labels ( or of shape , optional) — Labels for computing the cross entropy classification loss according to Rag-Token model formulation See https://huggingface.co/papers/2005.11401 Section 2.1 for details about Rag-Token formulation. Indices should be in .tf.Tensornp.ndarray(batch_size, sequence_length)[0, ..., config.vocab_size - 1]
reduce_loss (, optional) — Only relevant if is passed. If , the NLL loss is reduced using the operation.boollabelsTruetf.Tensor.sum
kwargs (, optional, defaults to ) — Legacy dictionary, which is required so that model can use generate() function.dict[str, any]{}
Returns

transformers.models.rag.modeling_tf_rag.TFRetrievAugLMMarginOutput or tuple(tf.Tensor)

A or a tuple of (if is passed or when ) comprising various elements depending on the configuration (RagConfig) and inputs.transformers.models.rag.modeling_tf_rag.TFRetrievAugLMMarginOutputtf.Tensorreturn_dict=Falseconfig.return_dict=False

loss ( of shape , optional, returned when is provided) — Language modeling loss.tf.Tensor(1,)labels

logits ( of shape ) — Prediction scores of the language modeling head. The score is possibly marginalized over all documents for each vocabulary token.tf.Tensor(batch_size, sequence_length, config.vocab_size)

past_key_values (, optional, returned when is passed or when ) — List of of length , with each tensor of shape ).list[tf.Tensor]use_cache=Trueconfig.use_cache=Truetf.Tensorconfig.n_layers(2, batch_size, num_heads, sequence_length, embed_size_per_head)

Contains precomputed hidden-states (key and values in the attention blocks) of the decoder that can be used (see input) to speed up sequential decoding.past_key_values

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state

retrieved_doc_embeds ( of shape , optional, returned when output_retrieved=True) — Embedded documents retrieved by the retriever. Is used with to compute the .tf.Tensor(batch_size, config.n_docs, hidden_size)question_encoder_last_hidden_statedoc_scores

retrieved_doc_ids ( (int32) of shape , optional, returned when output_retrieved=True) — The indexes of the embedded documents retrieved by the retriever.tf.Tensor(batch_size, config.n_docs)

context_input_ids ((int32) of shape , optional, returned when output_retrieved=True) — Input ids post-processed from the retrieved documents and the question encoder input_ids by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)

context_attention_mask ( (int32) of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids

question_encoder_last_hidden_state ( of shape , optional) — Sequence of hidden states at the output of the last layer of the question encoder pooled output of the model.tf.Tensor(batch_size, sequence_length, hidden_size)

question_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the question encoder at the output of each layer plus the initial embedding outputs.

question_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the question encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_enc_last_hidden_state ( of shape , optional) — Sequence of hidden-states at the output of the last layer of the generator encoder of the model.tf.Tensor(batch_size, sequence_length, hidden_size)

generator_enc_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator encoder at the output of each layer plus the initial embedding outputs.

generator_enc_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator encoder, after the attention softmax, used to compute the weighted average in the self-attention heads.

generator_dec_hidden_states (, optional, returned when is passed or when ) — Tuple of (one for the output of the embeddings and one for the output of each layer) of shape .tuple(tf.Tensor)output_hidden_states=Trueconfig.output_hidden_states=Truetf.Tensor(batch_size, sequence_length, hidden_size)

Hidden states of the generator decoder at the output of each layer plus the initial embedding outputs.

generator_dec_attentions (, optional, returned when is passed or when ) — Tuple of (one for each layer) of shape .tuple(tf.Tensor)output_attentions=Trueconfig.output_attentions=Truetf.Tensor(batch_size, num_heads, sequence_length, sequence_length)

Attentions weights of the generator decoder, after the attention softmax, used to compute the weighted average in the self-attention heads.


The TFRagTokenForGeneration forward method, overrides the special method.__call__

Although the recipe for forward pass needs to be defined within this function, one should call the instance afterwards instead of this since the former takes care of running the pre and post processing steps while the latter silently ignores them.Module

Example:

Copied
import tensorflow as tf
from transformers import AutoTokenizer, RagRetriever, TFRagTokenForGeneration

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True
)
# initialize with RagRetriever to do everything in one forward call
model = TFRagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever, from_pt=True)

input_dict = tokenizer.prepare_seq2seq_batch(
    "How many people live in Paris?", "In Paris, there are 10 million people.", return_tensors="tf"
)
outputs = model(input_dict, output_retrieved=True)

# or use retriever separately
# 1. Encode
input_ids = input_dict["input_ids"]
question_hidden_states = model.question_encoder(input_ids)[0]
# 2. Retrieve
docs_dict = retriever(input_ids.numpy(), question_hidden_states.numpy(), return_tensors="tf")
doc_scores = tf.squeeze(
    tf.matmul(
        tf.expand_dims(question_hidden_states, axis=1), docs_dict["retrieved_doc_embeds"], transpose_b=True
    ),
    axis=1,
)
# 3. Forward to generator
outputs = model(
    inputs=None,
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
    decoder_input_ids=input_dict["labels"],
)

# or directly generate
generated = model.generate(
    context_input_ids=docs_dict["context_input_ids"],
    context_attention_mask=docs_dict["context_attention_mask"],
    doc_scores=doc_scores,
)
generated_string = tokenizer.batch_decode(generated, skip_special_tokens=True)
generate
<
source
>
( input_ids: TFModelInputType | None = Noneattention_mask: tf.Tensor | None = Nonecontext_input_ids = Nonecontext_attention_mask = Nonedoc_scores = Nonen_docs = Nonegeneration_config = Nonelogits_processor = []**kwargs ) → tf.Tensor of shape (batch_size * num_return_sequences, sequence_length)

Parameters

input_ids ( of shape , optional) — The sequence used as a prompt for the generation. If is not passed, then has to be provided.tf.Tensor(batch_size, sequence_length)input_idscontext_input_ids
attention_mask ( of shape , optional) — Mask to avoid performing attention on padding token indices. Mask values selected in :tf.Tensor(batch_size, sequence_length)[0, 1]
1 for tokens that are not masked,
0 for tokens that are masked.
What are attention masks?

context_input_ids ( of shape , optional, returned when output_retrieved=True) — Input IDs post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a , has to be provided to the forward pass. are returned by .retrievercontext_input_idscontext_input_ids__call__()

context_attention_mask ( of shape , optional, returned when output_retrieved=True) — Attention mask post-processed from the retrieved documents and the question encoder by the retriever.tf.Tensor(batch_size * config.n_docs, config.max_combined_length)input_ids
If the model has is not initialized with a , has to be provided to the forward pass. are returned by .retrievercontext_input_idscontext_input_ids__call__()

doc_scores ( of shape ) — Score between each retrieved document embeddings (see ) and .tf.Tensor(batch_size, config.n_docs)retrieved_doc_embedsquestion_encoder_last_hidden_state
If the model has is not initialized with a , has to be provided to the forward pass. are returned by .retrievercontext_input_idscontext_input_ids__call__()

n_docs (, optional, defaults to ) — Number of documents to retrieve and/or number of documents for which to generate an answer.intconfig.n_docs
generation_config (, optional) — The generation configuration to be used as base parametrization for the generation call. passed to generate matching the attributes of will override them. If is not provided, the default will be used, which had the following loading priority: 1) from the model file, if it exists; 2) from the model configuration. Please note that unspecified parameters will inherit GenerationConfig’s default values, whose documentation should be checked to parameterize generation.~generation.GenerationConfig**kwargsgeneration_configgeneration_configgeneration_config.json
logits_processor (, optional) — Custom logits processors that complement the default logits processors built from arguments and a model’s config. If a logit processor is passed that is already created with the arguments or a model’s config an error is thrown.TFLogitsProcessorList
kwargs (, optional) — Ad hoc parametrization of and/or additional model-specific kwargs that will be forwarded to the function of the model.dict[str, Any]generate_configforward
Returns

tf.Tensor of shape (batch_size * num_return_sequences, sequence_length)

The generated sequences. The second dimension (sequence_length) is either equal to or shorter if all batches finished early due to the .max_lengtheos_token_id


Implements TFRAG token decoding.