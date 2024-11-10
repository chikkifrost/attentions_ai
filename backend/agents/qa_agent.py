# backend/agents/qa_agent.py

import logging
import os
from .database_agent import DatabaseAgent
from huggingface_hub import InferenceApi
from transformers import AutoTokenizer, AutoModelForCausalLM

##tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
##model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
logger = logging.getLogger(__name__)

def answer_question_about_topic(topic: str, question: str):
    logger.info(f"Answering question '{question}' about topic '{topic}'.")

    # Initialize DatabaseAgent
    db_agent = DatabaseAgent(
        uri="neo4j+s://0aa0acad.databases.neo4j.io",
        user="neo4j",
        password="W78HGMmr9LY6OHNhvK4onOAxvfZar_pl5XurZP47qHM"  # Replace with your Neo4j Aura password
    )

    # Retrieve papers
    papers = db_agent.get_papers(topic)
    contexts = [paper['summary'] for paper in papers]

    # Access Hugging Face API token
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_token:
        logger.error("Hugging Face API token is not set.")
        return "Error: Hugging Face API token is not set."

    # Initialize the Inference API for question answering
    qa_pipeline = InferenceApi(repo_id="deepset/roberta-large-squad2", token=api_token)
    # qa_pipeline = InferenceApi(repo_id="meta-llama/Meta-Llama-3-70B", token=api_token)


    # Find the best answer
    best_answer = {'score': 0, 'answer': '', 'reference': ''}
    for paper, context in zip(papers, contexts):
        try:
            inputs = {
                'question': question,
                'context': context
            }
            response = qa_pipeline(inputs=inputs)
            if 'error' in response:
                logger.error(f"Error from Hugging Face API: {response['error']}")
                continue
            if response['score'] > best_answer['score']:
                best_answer = {
                    'score': response['score'],
                    'answer': response['answer'],
                    'reference': paper['title']
                }
        except Exception as e:
            logger.error(f"Error processing paper '{paper['title']}': {e}")

    if best_answer['answer']:
        logger.info("Question answered successfully.")
    else:
        logger.info("No suitable answer found.")

    return best_answer['answer'], [best_answer['reference']]