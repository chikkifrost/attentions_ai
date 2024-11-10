import unittest
from backend.agents.database_agent import DatabaseAgent
from backend.models import ResearchPaper
from datetime import datetime

class TestDatabaseAgent(unittest.TestCase):
    def setUp(self):
        self.db_agent = DatabaseAgent()
        self.test_paper = ResearchPaper(
            id="test_id",
            title="Test Paper",
            authors=["Author A", "Author B"],
            abstract="This is a test abstract.",
            published=datetime.now(),
            url="http://testpaper.com"
        )
        self.topic = "Test Topic"

    def test_add_and_query_paper(self):
        self.db_agent.add_paper_with_relationships(self.test_paper, self.topic)
        papers = self.db_agent.query_papers_by_topic_and_year(self.topic, 2000, 2100)
        self.assertTrue(len(papers) > 0)
        self.assertEqual(papers[0].title, "Test Paper")

    def tearDown(self):
        # Clean up test data if necessary
        pass

if __name__ == '__main__':
    unittest.main()