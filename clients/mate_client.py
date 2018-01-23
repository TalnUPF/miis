# -*- coding: utf-8 -*-

import json
import urllib2, urllib

from conll import ConllStruct

class MateClient(object):

    lang_url_dict = {
        "en": "http://multisensor.taln.upf.edu/mate/process/multisensor_en",
        "es": "http://multisensor.taln.upf.edu/mate/process/multisensor_es"
    }

    def __init__(self, lang):
        self.base_url = type(self).lang_url_dict.get(lang)
        if self.base_url is None:
            raise Exception("Language %s is not supported!" % lang)
     
    def process(self, conll):

        data = {}
        data['levels'] = 3
        data['conll'] = str(conll)

        params = urllib.urlencode(data)
        request = urllib2.urlopen(self.base_url, params)
        response = json.loads(request.read())

        if "error" in response:
            raise Exception(response["error"])

        return ConllStruct(response["output"][0])

