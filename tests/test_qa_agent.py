import unittest
from backend.agents.qa_agent import QnAAgent
from backend.models import ResearchPaper
from datetime import datetime

class TestQnAAgent(unittest.TestCase):
    def setUp(self):
        self.qa_agent = QnAAgent()
        self.test_paper = ResearchPaper(
            id="test_id",
            title="Test Paper",
            authors=["Author A"],
            abstract="This paper discusses the advancements in AI.",
            published=datetime.now(),
            url="http://testpaper.com"
        )

    def test_answer_question(self):
        question = "What does the paper discuss?"
        answer, references = self.qa_agent.answer_question(question, [self.test_paper])
        self.assertTrue(len(answer) > 0)
        self.assertIn("advancements in AI", answer)

if __name__ == '__main__':
    unittest.main()