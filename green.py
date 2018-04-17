"""
Can create a markov model based on an txt file.
Will save the model and use it if available.

Completely relies on the module https://github.com/jsvine/markovify.
"""

import markovify
import json
import sys


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
            model = markovify.Text(file.read(), retain_original=bool, state_size=3)

        with open(name + '.json', 'w', encoding='UTF-8') as file:  # Save
            json.dump(model.to_json(), file)
        return model

def sentences(name, n):
    """ Generator object for n sentences. """
    markov = gen(name)
    i = 0
    while i < n:
        sentence = markov.make_sentence(max_overlap_ratio=0.5)  # 50% like original
        if sentence:  # Not none
            i += 1
            yield sentence

if __name__ == "__main__":  # Command line
    if len(sys.argv) > 1:
        for w in sentences(sys.argv[1], int(sys.argv[2])):
            print(w)
    else:
        print("Please provide the model name + number of sentences.")
