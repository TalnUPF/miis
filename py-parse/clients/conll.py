#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ConllStruct(object):

    def __init__(self, raw_conll=None):
        
        self.sentences = []
        
        if raw_conll is None:
            # Create an empty ConllStruct
            pass

        else:
            self.raw_conll = raw_conll.strip()

            if self.raw_conll:

                raw_sentence = u""
                for line in raw_conll.split(u'\n'):

                    if line.strip():
                        raw_sentence += line + u'\n'

                    elif raw_sentence:
                        sentence = ConllSentence(raw_sentence)
                        self.sentences.append(sentence)
                        raw_sentence = ""

            else:
                raise Exception('Empty conll!')

    def __add__(self, other):
        for sentence in other:
            self.sentences.append(sentence)
        return self

    def __iter__(self):
        return iter(self.sentences)

    def __repr__(self):
        return '\n\n'.join(map(str, self.sentences))

class ConllSentence(object):

    def __init__(self, raw_sentence):

        self.tokens = {}
        self.token_list = []
        self.plain_sentence = ""
        self.raw_sentence = raw_sentence.strip()
        
        if self.raw_sentence:
            try:
                self.raw_tokens = self.raw_sentence.split(u'\n')
                
                for raw_token in self.raw_tokens:
                    token = ConllToken2009(raw_token)

                    self.tokens[token.id] = token
                    self.token_list.append(token)
                    
                    self.plain_sentence += token.form + u" "
                
                for token in self.token_list:
                    # tries to use phead as parent-child relation
                    if token.phead != u'_':
                        if token.phead != u'0':
                            self.tokens[token.phead].add_child(token)
                    
                    # if phead is empty, tries head
                    elif token.head not in (u'0', u'_'):
                        self.tokens[token.head].add_child(token)

                self.plain_sentence = self.plain_sentence[:-1]
            except:
                print raw_sentence
                raise

        else:
            raise Exception('Empty conll sentence!')

    def __iter__(self):
        return iter(self.token_list)

    def __repr__(self):
        return '\n'.join(map(str, self.token_list))

    def get_token(self, token_id):
        return self.tokens[token_id]
        
    def get_form_sentence(self):
        return self.plain_sentence

class ConllToken2009(object):

    def __init__(self, raw_token):

        if raw_token.strip():
            self.columns = raw_token.split(u'\t')

            self.id         = self.columns[0]
            self.form       = self.columns[1]
            self.lemma      = self.columns[2]
            self.plemma     = self.columns[3]
            self.pos        = self.columns[4]
            self.ppos       = self.columns[5]
            self.feat       = self.columns[6]
            self.pfeat      = self.columns[7]
            self.head       = self.columns[8]
            self.phead      = self.columns[9]
            self.deprel     = self.columns[10]
            self.pdeprel    = self.columns[11]
            self.fillpred   = self.columns[12]
            self.pred       = self.columns[13]

            self.features = self._parse_features(self.feat)
            self.pfeatures = self._parse_features(self.pfeat)

            self.children = []
            
        else:
            raise Exception('Empty conll token!')

    def add_child(self, child_token):
        self.children.append(child_token)
        
    def _parse_features(self, feat_str):
        try:
            feat_dict = {}
            
            if feat_str != u"_":
                feat_list = feat_str.split(u"|")
                for feat in feat_list:
                    name, value = feat.split(u"=")
                    feat_dict[name] = value

            return feat_dict
            
        except:
            return None
    
    def get_feature_value(self, name):
        return self.features.get(name)

    def get_pfeature_value(self, name):
        return self.pfeatures.get(name)

    def __repr__(self):
        return u'\t'.join(self.columns).encode("utf8")
