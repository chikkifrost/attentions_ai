# backend/agents/future_works_agent.py

import logging
import os
from .database_agent import DatabaseAgent
from huggingface_hub import InferenceApi

logger = logging.getLogger(__name__)

def generate_future_works(topic: str) -> str:
    logger.info(f"Generating future works for topic: {topic}")

    # Initialize DatabaseAgent
    db_agent = DatabaseAgent(
        uri="neo4j+s://0aa0acad.databases.neo4j.io",
        user="neo4j",
        password="W78HGMmr9LY6OHNhvK4onOAxvfZar_pl5XurZP47qHM"  # Replace with your Neo4j Aura password
    )

    # Retrieve papers
    papers = db_agent.get_papers(topic)
    summaries = [paper['summary'] for paper in papers]

    # Concatenate summaries
    combined_summaries = ' '.join(summaries)

    # Access Hugging Face API token
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_token:
        logger.error("Hugging Face API token is not set.")
        return "Error: Hugging Face API token is not set."

    # Initialize the Inference API for text generation
    generator = InferenceApi(repo_id="EleutherAI/gpt-neo-2.7B", token=api_token)

    # Generate future work suggestions
    prompt = f"Based on recent advancements in {topic}, future research directions include:"
    inputs = prompt + "\n\n" + combined_summaries[:500]  # Limit input size if necessary

    response = generator(inputs=inputs, parameters={"max_length": 200, "temperature": 0.7})
    if 'error' in response:
        logger.error(f"Error from Hugging Face API: {response['error']}")
        return "Error generating future works."

    future_works = response

    logger.info("Future works generated successfully.")

    return future_works