from __future__ import annotations
import random
from typing import TYPE_CHECKING
from collections import defaultdict
import pandas as pd
import numpy as np
from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama
from llama_index.core.evaluation import DatasetGenerator, QueryResponseDataset
# Import evaluation classes and utilities
from llama_index.core.evaluation import (
    CorrectnessEvaluator,
    SemanticSimilarityEvaluator,
    RelevancyEvaluator,
    FaithfulnessEvaluator,
    PairwiseComparisonEvaluator,
)
from llama_index.core.evaluation.eval_utils import (
    get_responses,
    get_results_df,
)
from llama_index.core.evaluation import BatchEvalRunner
from IPython.display import Markdown, display
from app.common import (
        get_llama,
        get_base_nodes,
        load_stored_index,
        get_service_context
    )

from app.log import get_logger

import asyncio
import nest_asyncio
nest_asyncio.apply()


if TYPE_CHECKING:
    from llama_index.core.base.llms.types import CompletionResponse
    from llama_index.core.base.response.schema import RESPONSE_TYPE

__all__ = ["evaluate"]
logger = get_logger("evaluate")


async def dataset_generator():
    sentence_nodes , base_nodes = get_base_nodes()
    num_nodes_eval = 10
    # there are 216 nodes total. Take the first 25 to generate questions (the back half of the doc is all references)
    sample_eval_nodes = random.sample(sentence_nodes[:25], num_nodes_eval)
    # NOTE: run this if the dataset isn't already saved
    # generate questions from the largest chunks (1024)
    data_generator = DatasetGenerator(
        sample_eval_nodes,
        llm=get_llama(),
        show_progress=True,
        num_questions_per_chunk=2,
    )

    eval_dataset = await data_generator.agenerate_dataset_from_nodes()
    eval_dataset.save_json("book_dataset.json")
    eval_dataset = QueryResponseDataset.from_json("book_dataset.json")

    return eval_dataset

async def run_evaluvation(evaluator_dict, eval_qs, pred_responses, ref_response_strs):
    # Initialize a BatchEvalRunner to evaluate responses in parallel
    batch_runner = BatchEvalRunner(
        evaluator_dict,  # Dictionary of evaluators
        workers=2,       # Number of worker processes for parallel evaluation
        show_progress=True  # Show progress during evaluation
    )

    # Evaluate responses from the sentence window query engine
    eval_results = await batch_runner.aevaluate_responses(
        queries = eval_qs[:max_samples],                 # Subset of evaluation questions
        responses = pred_responses[:max_samples],        # Responses from the sentence window query engine
        reference = ref_response_strs[:max_samples],     # Reference response strings
    )

    # Evaluate responses from the base query engine
    base_eval_results = await batch_runner.aevaluate_responses(
        queries=eval_qs[:max_samples],                    # Subset of evaluation questions
        responses=base_pred_responses[:max_samples],      # Responses from the base query engine
        reference=ref_response_strs[:max_samples],        # Reference response strings
    )
    # Evaluate performance with num_nodes_eval = 10, base_nodes[:25] (25 nodes), max_samples = 6
    # Generate a DataFrame to display evaluation results
    results_df = get_results_df(
        [eval_results, base_eval_results],  # List of evaluation results
        ["Sentence Window Retriever", "Base Retriever"],  # Labels for different retrievers
        ["correctness", "relevancy", "faithfulness", "semantic_similarity"],  # Metrics to include in the DataFrame
    )
    # Display the DataFrame
    print("results_df", results_df)
    display(results_df)




def evaluate():
    llm = get_llama()
    # Initialize and configure evaluators for assessing language model performance
    # CorrectnessEvaluator evaluates the correctness of generated responses
    evaluator_c = CorrectnessEvaluator(llm=llm)
    # SemanticSimilarityEvaluator assesses semantic similarity between responses and references
    evaluator_s = SemanticSimilarityEvaluator(service_context=get_service_context())
    # RelevancyEvaluator evaluates relevancy of generated responses to input questions
    evaluator_r = RelevancyEvaluator(llm=llm)
    # FaithfulnessEvaluator assesses faithfulness of generated responses to input context
    evaluator_f = FaithfulnessEvaluator(llm=llm)
    # PairwiseComparisonEvaluator can be uncommented if needed

    # Set maximum number of samples for evaluation
    max_samples = 6

    eval_dataset = asyncio.run(dataset_generator())
    # Extract questions and reference response strings from the evaluation dataset
    eval_qs = eval_dataset.questions
    ref_response_strs = [r for (_, r) in eval_dataset.qr_pairs]

    sentence_index, base_index = load_stored_index()
    # Set up query engines for base index and sentence window index
    # Base query engine
    base_query_engine = base_index.as_query_engine(similarity_top_k=2)
    # Sentence window query engine
    query_engine = sentence_index.as_query_engine(
        similarity_top_k=2,
        # The target key defaults to `window` to match the node_parser's default
        node_postprocessors=[
            MetadataReplacementPostProcessor(target_metadata_key="window")
        ],
    )

    # Retrieve responses from the base query engine for evaluation
    base_pred_responses = get_responses(
        eval_qs[:max_samples],  # Subset of evaluation questions
        base_query_engine,      # Query engine for the base index
        show_progress=True     # Show progress while retrieving responses
    )

    # Retrieve responses from the sentence window query engine for evaluation
    pred_responses = get_responses(
        eval_qs[:max_samples],  # Subset of evaluation questions
        query_engine,           # Query engine for the sentence window index
        show_progress=True     # Show progress while retrieving responses
    )

    # Convert responses to strings for easier comparison
    pred_response_strs = [str(p) for p in pred_responses]
    base_pred_response_strs = [str(p) for p in base_pred_responses]

    # Define a dictionary of evaluators for different aspects of model performance
    evaluator_dict = {
        "correctness": evaluator_c,
        "faithfulness": evaluator_f,
        "relevancy": evaluator_r,
        "semantic_similarity": evaluator_s,
    }
    asyncio.run(run_evaluvation(evaluator_dict, eval_qs, pred_responses, ref_response_strs))

    
# def evaluate(response: RESPONSE_TYPE) -> CompletionResponse:
#     logger.info("Starting..")

#     llama = get_llama()

#     template = """"
#         <s>[INST] <<SYS>>

#         {{ System Prompt }}

#         <</SYS>>

#         {{ User Prompt }}
#          [/INST]

#         {{ Model Answer }}
#     """
#     prompt = PromptTemplate(template)




#     # TASK: Given the answer generated by the LLM in the previous step, write an evaluation prompt to have the LLM check if the answer
#     # appropriately answered the question.
#     # - If the answer sufficiently answers the question have the LLM respond with "Yes" and if not then "No".

#     return prompt
