# backend/agents/database_agent.py

from neo4j import GraphDatabase, basic_auth
import logging

logger = logging.getLogger(__name__)

class DatabaseAgent:
    def __init__(self, uri, user, password):
        """
        Initializes the DatabaseAgent with the given connection parameters.

        Args:
            uri (str): The Neo4j connection URI.
            user (str): The Neo4j username.
            password (str): The Neo4j password.
        """
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        """
        Closes the Neo4j driver connection.
        """
        self.driver.close()

    def add_papers(self, papers, topic):
        """
        Adds a list of papers to the Neo4j database under the specified topic.

        Args:
            papers (List[Dict]): A list of paper dictionaries.
            topic (str): The research topic.
        """
        with self.driver.session() as session:
            for paper in papers:
                session.write_transaction(self._create_paper_node, paper, topic)

    @staticmethod
    def _create_paper_node(tx, paper, topic):
        """
        Creates or updates a Paper node in the database.

        Args:
            tx: The transaction object.
            paper (Dict): A dictionary containing paper details.
            topic (str): The research topic.
        """
        tx.run(
            """
            MERGE (p:Paper {id: $id})
            SET p.title = $title,
                p.summary = $summary,
                p.authors = $authors,
                p.published = $published,
                p.pdf_url = $pdf_url,
                p.topic = $topic
            """,
            id=paper['id'],
            title=paper['title'],
            summary=paper['summary'],
            authors=paper['authors'],
            published=paper['published'],
            pdf_url=paper['pdf_url'],
            topic=topic
        )

    def get_papers(self, topic, year_from=None, year_to=None):
        """
        Retrieves papers from the database based on the topic and optional year range.

        Args:
            topic (str): The research topic.
            year_from (str, optional): The start year in "YYYY-MM-DD" format.
            year_to (str, optional): The end year in "YYYY-MM-DD" format.

        Returns:
            List[Dict]: A list of paper nodes.
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._query_papers, topic, year_from, year_to)
            return result

    @staticmethod
    def _query_papers(tx, topic, year_from, year_to):
        """
        Queries the database for papers matching the criteria.

        Args:
            tx: The transaction object.
            topic (str): The research topic.
            year_from (str, optional): The start year.
            year_to (str, optional): The end year.

        Returns:
            List[Dict]: A list of paper nodes.
        """
        query = """
        MATCH (p:Paper)
        WHERE p.topic = $topic
        """
        if year_from:
            query += " AND p.published >= $year_from"
        if year_to:
            query += " AND p.published <= $year_to"

        query += " RETURN p ORDER BY p.published DESC"

        result = tx.run(query, topic=topic, year_from=year_from, year_to=year_to)
        return [record['p'] for record in result]