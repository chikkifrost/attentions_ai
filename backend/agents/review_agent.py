# backend/agents/review_agent.py

import logging
import os
from .database_agent import DatabaseAgent
from huggingface_hub import InferenceApi

logger = logging.getLogger(__name__)

def generate_review_for_topic(topic: str) -> str:
    logger.info(f"Generating review for topic: {topic}")

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

    # Initialize the Inference API for summarization
    summarizer = InferenceApi(repo_id="facebook/bart-large-cnn", token=api_token)

    # Due to token limits, split the text if necessary
    max_chunk = 1024  # Adjust based on model's max input size
    chunks = [combined_summaries[i:i + max_chunk] for i in range(0, len(combined_summaries), max_chunk)]

    review = ""
    for chunk in chunks:
        response = summarizer(inputs=chunk)
        if 'error' in response:
            logger.error(f"Error from Hugging Face API: {response['error']}")
            continue
        review += response[0]['summary_text'] + " "

    logger.info("Review generated successfully.")

    return review.strip()