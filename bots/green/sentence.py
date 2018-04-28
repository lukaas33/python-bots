"""
Can create a markov model based on an txt file.
Will save the model and use it if available.

Completely relies on the module https://github.com/jsvine/markovify.
"""

import markovify
import json


def gen(name):
    """ Return a markovify object using the name of a model. """
    try:
        with open(name + '.json', 'r', encoding='UTF-8') as file:  # Open if exists
            data = json.load(file)
            model = markovify.Text.from_json(data)
            return model
    except:
        with open(name + '.txt', 'r', encoding='UTF-8') as file:  # Create
            bool = True  # Memory saving when false
            model = markovify.Text(file.read(), retain_original=bool, state_size=2)

        with open(name + '.json', 'w', encoding='UTF-8') as file:  # Save
            json.dump(model.to_json(), file)

        return model


def sentence(gene, start):
    """ Generator object for n sentences. """
    if start:
        sentence = gene.make_sentence_with_start(start, strict=False, max_overlap_ratio=0.35)
    else:
        sentence = gene.make_sentence(max_overlap_ratio=0.35) 

    return sentence
