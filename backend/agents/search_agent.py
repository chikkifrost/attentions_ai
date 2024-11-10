# backend/agents/search_agent.py

import arxiv
import logging

logger = logging.getLogger(__name__)

def search_arxiv(topic: str, max_results: int = 50):
    """
    Searches ArXiv for papers related to the given topic.

    Args:
        topic (str): The research topic to search for.
        max_results (int): Maximum number of results to return.

    Returns:
        List[Dict]: A list of dictionaries containing paper details.
    """
    logger.info(f"Searching ArXiv for topic: {topic}")

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    papers = []
    for result in search.results():
        paper = {
            'id': result.get_short_id(),
            'title': result.title,
            'summary': result.summary,
            'authors': [author.name for author in result.authors],
            'published': result.published.strftime("%Y-%m-%d"),
            'pdf_url': result.pdf_url,
        }
        papers.append(paper)

    logger.info(f"Found {len(papers)} papers on ArXiv for topic '{topic}'.")
    return papers