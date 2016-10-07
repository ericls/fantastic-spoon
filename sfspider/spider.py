# -*- coding utf-8 -*-
from pyquery import PyQuery as Pq
import requests


class SFQuestionSpider(object):
    def __init__(self, sf_id):
        self.id = sf_id
        self.url = 'https://segmentfault.com/q/%s' % sf_id
        self._dom = None

    @property
    def dom(self):
        if not self._dom:
            d = requests.get(self.url)
            d.encoding = 'utf-8'
            self._dom = Pq(d.text)
        return self._dom

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
