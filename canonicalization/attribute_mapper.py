#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains functions to canonicalize attributes."""
from __future__ import absolute_import
from __future__ import print_function
import re
import collections

import nltk
from nltk.corpus import wordnet
from .utils import log
from .utils import wordnet_helper

logger = log.get_logger(__name__)

exception_dict = {
    'square': wordnet.synset('square.a.01'),
    'light': wordnet.synset('light.a.02'),
    'dark': wordnet.synset('dark.a.02'),
    'right': wordnet.synset('right.a.01'),
    'overcast': wordnet.synset('overcast.a.01'),
    'little': wordnet.synset('little.a.01'),
    'ready': wordnet.synset('ready.a.01'),
    'straight': wordnet.synset('straight.a.02'),
    'long': wordnet.synset('long.a.02'),
    'short': wordnet.synset('short.a.02'),
    'clear': wordnet.synset('clear.a.07'),
    'foggy': wordnet.synset('foggy.a.03'),
    'inside': wordnet.synset('inside.a.02'),
    'cloudy': wordnet.synset('cloudy.a.02')
}

def clean_text(text):
    return re.sub(r'[^a-zA-Z]+', ' ', text).strip().lower()

def wn_tag(words, pos_tagged):
    tagged = []
    pos_collection = [wordnet.NOUN, wordnet.ADJ, wordnet.VERB, wordnet.ADV]
    for index, word in enumerate(words):
        if 1 < len(words) and pos_tagged[index] == 'IN' and word != 'white':
            tagged.append('prep')
            continue
        counts = [wordnet_helper.WordNetHelper().lemma_counter(word, pos=i).most_common() for i in pos_collection]
        counts = [i[0][1] if i else 0 for i in counts]
        highest = max(counts)
        if highest == 0:
            return []
        else:
            tagged.append(pos_collection[counts.index(highest)])
    return tagged

def canonicalize_attribute(text):
    def pack_definition(res):
        if res is None:
            logger.info('result is None')
            return None
        else:
            logger.info('result is {}'.format(res.name()))
            return {
                'name': res.name(),
                'definition': res.definition()
            }
    words = clean_text(text).split()
    pos_tagged = [i[1] for i in nltk.pos_tag(words)]
    # Remove adverbs.
    if 1 < len(words) and words[0] not in exception_dict and pos_tagged[0] == 'RB':
        words.pop(0)
    # Remove common modifiers.
    if 1 < len(words) and (words[0] == 'light' or words[0] == 'dark' or words[0] == 'not'):
        words.pop(0)

    pos = None
    if len(words) == 0:
        return None
    if words[0] in exception_dict:
        logger.info('{} is in exceptions'.format(words[0]))
        return pack_definition(exception_dict[words[0]])
    if words[0][-3:] == 'ing':
        words[0] = nltk.stem.WordNetLemmatizer().lemmatize(words[0], wordnet.VERB)
        pos = wordnet.VERB
    elif pos_tagged[0] == 'IN' and 1 < len(words) and words[0] != 'white':
        # Do not handle prepositions.
        return None
    else:
        wn_tagged = wn_tag(words, pos_tagged)
        if 1 < len(words) and set(wn_tagged) == set([wordnet.NOUN]):
            # Most likely random nouns.
            return None
        elif wordnet.synsets(words[0], pos=wordnet.ADJ):
            pos = wordnet.ADJ
        elif wn_tagged and wn_tagged[0] == wordnet.VERB:
            pos = wordnet.VERB
        elif wn_tagged and wn_tagged[0] == wordnet.ADV:
            pos = wordnet.ADV
        elif wordnet.synsets(words[0], pos=wordnet.NOUN):
            pos = wordnet.NOUN
        else:
            # Otherwise most likely not in WordNet or misspelled
            return None
    given = wordnet.synsets(words[0], pos)
    counted = [p[0] for p in wordnet_helper.WordNetHelper().lemma_counter(words[0], pos).most_common()]
    cap = [s for s in given if s in counted]
    if not cap:
        counted.expend(given)
        cap = counted
    selection = [s for s in given if s in cap]
    if selection:
        return pack_definition(selection[0])
    else:
        return None
