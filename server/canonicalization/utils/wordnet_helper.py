#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: Oliver Groth, Yutian Li
"""Contains various helper functions for working with WordNet."""

from __future__ import absolute_import
from __future__ import print_function
from nltk.corpus import wordnet
import collections


def lemma_counter(word, pos=wordnet.NOUN):
    """Gets frequency counts for a synset.

    Args:
        word: A word to lookup.
        pos: Part of speech.

    Returns:
        A collections.Counter for all synsets of the
        specified word with frequencies annotated.
    """
    syns = wordnet.synsets(word, pos)
    freq = []
    for s in syns:
        count = sum([l.count() for l in s.lemmas()])
        freq.extend([s] * count)
    return collections.Counter(freq)


def synset_to_wordnet_id(syn):
    """Converts synset to WordNet ID.

    Args:
        syn: A synset.

    Returns:
        A unique WordNet ID as used in ImageNet.
    """
    pos = str(syn.pos())
    offset = str(syn.offset())
    len_offset = len(offset)
    # Pad offset number with leading zeros.
    if len_offset < 8:
        pad = 8 - len_offset
        offset = '0' * pad + offset
    return pos + offset
