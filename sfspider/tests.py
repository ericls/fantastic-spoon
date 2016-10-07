import unittest
from spider import SFQuestionSpider, SFTagSpider


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



class TagSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = SFTagSpider('python')

    def test_can_get_list_of_question_urls(self):
        self.assertEqual(type(self.spider.question_urls), list)
        self.assertEqual(len(self.spider.question_urls), 20)

    def test_detect_next_page(self):
        self.assertEqual(self.spider.has_next_page, True)

    def test_go_next_page(self):
        self.spider.next_page()
        self.assertEqual(
            'https://segmentfault.com/t/python?type=newest&page=2',
            self.spider.url
        )


if __name__ == '__main__':
    unittest.main()
