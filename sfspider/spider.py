# -*- coding utf-8 -*-
import os
import sys
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping.settings")
import django
django.setup()

from qa.models import Question, Tag, Answer
from pyquery import PyQuery as Pq
import requests


class SFBaseSpider(object):

    def __init__(self):
        self._dom = None

    @property
    def dom(self):
        if not self._dom:
            d = requests.get(self.url)
            d.encoding = 'utf-8'
            self._dom = Pq(d.text)
        return self._dom


class SFQuestionSpider(SFBaseSpider):
    def __init__(self, sf_id):
        super().__init__()
        self.id = sf_id
        self.url = 'https://segmentfault.com/q/%s' % sf_id

    @property
    def title(self):
        return self.dom('h1#questionTitle').text()

    @property
    def content(self):
        return self.dom(
            '.question.fmt'
        ).html().strip() # TODO: Process this

    @property
    def answers(self):
        answer_elements = self.dom('.answer.fmt').items()
        return list(map(lambda element: element.html(), answer_elements))

    @property
    def tags(self):
        tag_elements = self.dom('.tagPopup.mb5 > a').items()
        return list(
            map(lambda element: element.text(), tag_elements)
        )

    def save(self):
        question, created = Question.objects.get_or_create(
            sf_id=self.id,
            defaults={
                'title': self.title,
                'content_html': self.content
            }
        )
        if created:
            print("Created new question %s" % question.title)
        for tag_name in self.tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_name
            )
            question.tags.add(tag)
        for answer_content in self.answers:
            answer = Answer.objects.create(
                content_html=answer_content
            )
        return question

class SFTagSpider(SFBaseSpider):

    def __init__(self, tag, page=1):
        super().__init__()
        self.tag = tag
        self.url = 'https://segmentfault.com/t/%s?type=newest&page=%s' % (
            tag,
            page
        )
        self.page = page

    @property
    def has_next_page(self):
        return bool(
            self.dom('ul.pagination > li.next')
        )

    def next_page(self):
        if self.has_next_page:
            self.__init__(tag=self.tag, page=self.page + 1)
            return self
        else:
            return

    @property
    def question_urls(self):
        question_link_elements = self.dom(
            'section.stream-list__item > div.summary > h2 > a'
        ).items()
        return list(
            map(
                lambda element: 'https://segmentfault.com' + element.attr("href"), question_link_elements
            )
        )
