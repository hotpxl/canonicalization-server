#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains functions to canonicalize relationships."""
from __future__ import absolute_import
from __future__ import print_function

import repoze.lru
from nltk.corpus import wordnet
from .utils import wordnet_helper
from .utils import common


@repoze.lru.lru_cache(4096)
def canonicalize_relationship(text):
    words = common.clean_text(text).split()
    freq = []
    for word in words:
        for pos in [wordnet.VERB, wordnet.ADV]:
            freq.extend(wordnet_helper.lemma_counter(word,
                                                     pos=pos).most_common())
    if freq:
        return max(freq, key=lambda x: x[1])[0]
    else:
        return None
