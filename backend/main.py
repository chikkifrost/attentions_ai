# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from .agents.search_agent import search_arxiv
from .agents.database_agent import DatabaseAgent
from .agents.review_agent import generate_review_for_topic
from .agents.qa_agent import answer_question_about_topic
from .agents.future_works_agent import generate_future_works
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize DatabaseAgent with Neo4j Aura connection details
db_agent = DatabaseAgent(
    uri="neo4j+s://0aa0acad.databases.neo4j.io",
    user="neo4j",
    password="W78HGMmr9LY6OHNhvK4onOAxvfZar_pl5XurZP47qHM"  # Replace with your Neo4j Aura password
)

# Request models
class TopicRequest(BaseModel):
    topic: str

class QuestionRequest(BaseModel):
    topic: str
    question: str

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Academic Research Paper Assistant API"}

# Endpoint to collect and store papers
@app.post("/collect_papers/")
async def collect_papers(request: TopicRequest):
    logger.info(f"Collecting papers for topic: {request.topic}")
    try:
        papers = search_arxiv(request.topic)
        db_agent.add_papers(papers, request.topic)
        logger.info(f"Collected and stored {len(papers)} papers for topic '{request.topic}'.")
        return {"message": f"Collected and stored {len(papers)} papers for topic '{request.topic}'."}
    except Exception as e:
        logger.error(f"Error collecting papers: {e}")
        return {"error": "Failed to collect and store papers."}

# Endpoint to retrieve papers
@app.post("/get_papers/")
async def get_papers(request: TopicRequest):
    logger.info(f"Fetching papers for topic: {request.topic}")
    try:
        papers = db_agent.get_papers(request.topic)
        papers_data = []
        for paper in papers:
            papers_data.append({
                'title': paper['title'],
                'authors': paper['authors'],
                'published': paper['published'],
                'summary': paper['summary'],
                'pdf_url': paper['pdf_url'],
            })
        return {"papers": papers_data}
    except Exception as e:
        logger.error(f"Error fetching papers: {e}")
        return {"error": "Failed to fetch papers."}

# Endpoint to generate a review paper
@app.post("/generate_review/")
async def generate_review(request: TopicRequest):
    logger.info(f"Generating review for topic: {request.topic}")
    review = generate_review_for_topic(request.topic)
    if review.startswith("Error:"):
        return {"error": review}
    return {"review_paper": review}

# Endpoint to answer questions
@app.post("/answer_question/")
async def answer_question(request: QuestionRequest):
    logger.info(f"Answering question about topic: {request.topic}")
    answer, references = answer_question_about_topic(request.topic, request.question)
    if answer.startswith("Error:"):
        return {"error": answer}
    return {"answer": answer, "references": references}

# Endpoint to generate future works suggestions
@app.post("/generate_future_works/")
async def generate_future_works_endpoint(request: TopicRequest):
    logger.info(f"Generating future works for topic: {request.topic}")
    future_works = generate_future_works(request.topic)
    if future_works.startswith("Error:"):
        return {"error": future_works}
    return {"future_works": future_works}