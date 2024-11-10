import unittest
from backend.agents.search_agent import search_arxiv

class TestSearchAgent(unittest.TestCase):
    def test_search_arxiv(self):
        papers = search_arxiv("Text-to-SQL", max_results=5)
        self.assertTrue(len(papers) > 0)
        for paper in papers:
            self.assertIn("Text-to-SQL", paper.title)

if __name__ == '__main__':
    unittest.main()