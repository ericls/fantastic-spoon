import unittest
from spider import SFQuestionSpider


class QuestionSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = SFQuestionSpider('1010000006988153')

    def test_title(self):
        self.assertEqual(
            self.spider.title,
            'Mysql用户消息系统设计的疑惑'
        )

    def test_content(self):
        self.assertIn(
            '现网站分为两种消息，第一种：全站消息，第二种',
            self.spider.content
        )

    def test_answers(self):
        self.assertTrue(self.spider.answers)

    def test_tags(self):
        self.assertEqual(
            self.spider.tags,
            ['mysql优化', 'mysql', 'php']
        )


if __name__ == '__main__':
    unittest.main()
