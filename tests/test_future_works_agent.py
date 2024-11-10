import unittest
from backend.agents.future_works_agent import FutureWorksAgent
from backend.models import ResearchPaper
from datetime import datetime

class TestFutureWorksAgent(unittest.TestCase):
    def setUp(self):
        self.future_agent = FutureWorksAgent()
        self.test_paper = ResearchPaper(
            id="test_id",
            title="Test Paper",
            authors=["Author A"],
            abstract="This paper discusses the advancements in AI.",
            published=datetime.now(),
            url="http://testpaper.com"
        )

    def test_summarize_papers(self):
        summary = self.future_agent.summarize_papers([self.test_paper])
        self.assertTrue(len(summary) > 0)

    def test_generate_future_research_directions(self):
        summary = "Advancements in AI have been significant."
        future_directions = self.future_agent.generate_future_research_directions(summary)
        self.assertTrue(len(future_directions) > 0)

if __name__ == '__main__':
    unittest.main()