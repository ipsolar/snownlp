# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import normal
from . import seg
from . import tag
from . import sentiment
from .sim import bm25
from .summary import textrank


class SnowNLP(object):

    def __init__(self, doc):
        self.doc = doc
        self.bm25 = bm25.BM25(doc)

    @property
    def words(self):
        return seg.seg(self.doc)

    @property
    def sentences(self):
        return normal.get_sentences(self.doc)

    @property
    def han(self):
        return normal.zh2hans(self.doc)

    @property
    def pinyin(self):
        words = self.words
        ret = []
        for word in words:
            ret += normal.get_pinyin(word)
        return ret

    @property
    def sentiments(self):
        return sentiment.classify(self.doc)

    @property
    def tags(self):
        words = self.words
        tags = tag.tag(words)
        return zip(words, tags)

    @property
    def tf(self):
        return self.bm25.f

    @property
    def idf(self):
        return self.bm25.idf

    def summary(self, limit=5):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = seg.seg(sent)
            words = normal.filter_stop(words)
            doc.append(words)
        rank = textrank.TextRank(doc)
        rank.solve()
        ret = []
        for index in rank.top_index(limit):
            ret.append(sents[index])
        return ret

    def keywords(self, limit=5):
        doc = []
        sents = self.sentences
        for sent in sents:
            words = seg.seg(sent)
            words = normal.filter_stop(words)
            doc.append(words)
        rank = textrank.KeywordTextRank(doc)
        rank.solve()
        ret = []
        for w in rank.top_index(limit):
            ret.append(w)
        return ret
