# -*- coding: utf-8 -*-

import json
import urllib2, urllib

import nltk
from nltk.tokenize import word_tokenize

from conll import ConllStruct

class BaseClient(object):

    lang_url_dict = {
        "en": "http://multisensor.taln.upf.edu/transition/en/refactor/parse"
    }

    def __init__(self, lang):
        self.base_url = type(self).lang_url_dict.get(lang)
        if self.base_url is None:
            raise Exception("Language %s is not supported!" % lang)
        
    def parse_tokens(self, tokens):
        return self.parse_data({"data": {"tokens": tokens}})

    def parse_data(self, data):

        req = urllib2.Request(self.base_url)
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))
        result = json.loads(response.read())

        if "error" in result:
            raise Exception(result["error"])

        return ConllStruct(result["output"])

class NLTKParserClient(BaseClient):

    max_sentences_per_request = 10
    ssplitter_dict = {
        "en": nltk.data.load('tokenizers/punkt/english.pickle'),
        "es": nltk.data.load('tokenizers/punkt/spanish.pickle')
    }

    def __init__(self, lang):
        super(NLTKParserClient, self).__init__(lang)

        self.ssplitter = type(self).ssplitter_dict.get(lang)
        if self.ssplitter is None:
            raise Exception("Language %s is not supported!" % lang)

    def parse_text(self, text):

        processed_text = self.preprocess(text)
        sentences = self.ssplit(processed_text)
        
        idx = 0
        output = ConllStruct()
        while idx < len(sentences):
            
            start = idx
            idx += type(self).max_sentences_per_request

            sentence_set = sentences[start:idx]
            tokenization = self.tokenize(sentence_set)
            output += self.parse_tokens(tokenization)

        return output

    def tokenize(self, sentences):
        tokenization = []
        for sentence in sentences:
            tokenization.append(word_tokenize(sentence))
        return tokenization

    def ssplit(self, text): 
        return self.ssplitter.tokenize(text)

    def preprocess(self, text):
        return text

