"""
Completely relies on the module https://github.com/jsvine/markovify.
"""

import markovify
import json
import os


def gen(name):
    """ Return a markovify object using the name of a model. """
    with open((os.curdir + '/bots/green/' + name + '.json'), 'r', encoding='UTF-8') as file:  # Open if exists
        data = json.load(file)
        model = markovify.Text.from_json(data)
        return model


def sentence(gene, start):
    if start:
        sentence = gene.make_sentence_with_start(start, strict=False, max_overlap_ratio=0.35)
    else:
        sentence = gene.make_sentence(max_overlap_ratio=0.35)

    return sentence
