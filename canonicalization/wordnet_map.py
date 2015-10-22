#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: Oliver Groth, Yutian Li

"""Contains functions to map terms to WordNet and ImageNet entities."""

from __future__ import absolute_import
from __future__ import print_function
import cPickle
import os.path
import nltk
from nltk.corpus import wordnet
from .utils import imagenet_helper
from .utils import wordnet_helper


exception_dict = {
    'crust': wordnet.synset('crust.n.02'),
    'helmet': wordnet.synset('helmet.n.02'),
    'microwave': wordnet.synset('microwave.n.02'),
    'number': wordnet.synset('numeral.n.01'),
    'plate': wordnet.synset('plate.n.04'),
    'sign': wordnet.synset('sign.n.02'),
    'spice': wordnet.synset('spice.n.02'),
    'time': wordnet.synset('clock_time.n.01'),
    'tissue': wordnet.synset('tissue.n.02'),
    'shoe': wordnet.synset('shoe.n.01'),
    'men': wordnet.synset('man.n.01'),
    'sunglasses': wordnet.synset('sunglasses.n.01'),
    'hood': wordnet.synset('hood.n.08'),
    'pants': wordnet.synset('trouser.n.01'),
    'front': None,
    'left': None,
    'right': None,
    'top': None,
    'planter': wordnet.synset('planter.n.02'),
    'shorts': wordnet.synset('short_pants.n.01'),
    'stickers': wordnet.synset('gummed_label.n.01'),
    'background': wordnet.synset('background.n.02'),
    'table': wordnet.synset('table.n.02'),
    'glasses': wordnet.synset('spectacles.n.01'),
    'lights': wordnet.synset('light.n.02'),
    'kite': wordnet.synset('kite.n.03'),
    'cake': wordnet.synset('cake.n.03'),
    'van': wordnet.synset('van.n.05'),
    'monitor': wordnet.synset('monitor.n.04'),
    'glove': wordnet.synset('glove.n.02'),
    'racket': wordnet.synset('racket.n.04'),
    'knob': wordnet.synset('knob.n.02'),
    'sticker': wordnet.synset('gummed_label.n.01'),
    'board': wordnet.synset('board.n.02'),
    'bat': wordnet.synset('bat.n.05')
}


class WordNetMapper(object):

    def __init__(self, res_path):
        """Initializer.

        Args:
            res_path: A string representing path to the resource files.
        """
        self.res_path = res_path
        self.lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
        self.in_helper = imagenet_helper.ImageNetHelper(res_path)
        self.wn_helper = wordnet_helper.WordNetHelper(res_path)
        with open(os.path.join(res_path, 'visualization',
                               'common_colors.txt')) as f:
            self.common_colors_set = set(cPickle.load(f))

    def map_word(self, word, pos=wordnet.NOUN):
        """Maps a word to the most frequent WordNet synset.

        The mapping is based on NLTK WordNet interface result, WordNet
        lemma counts, and ImageNet synset information.

        Args:
            word: A string representing the word.

        Returns:
            A synset or None if no match was found.
        """
        # Preprocess word.
        word = word.lower().strip().replace(' ', '_')

        # Check for exceptions.
        if word in self.common_colors_set:
            # TODO print '%s is common color, excluded from mapping!' % word
            return None
        elif word in exception_dict:
            # TODO print '%s is exception case, direct mapping!' % word
            return exception_dict[word]

        word = self.lmtzr.lemmatize(word, pos)
        # Check for exceptions.
        if word in self.common_colors_set:
            # TODO print '%s is common color, excluded from mapping!' % word
            return None
        elif word in exception_dict:
            # TODO print '%s is exception case, direct mapping!' % word
            return exception_dict[word]

        given = wordnet.synsets(word, pos)
        # print 'Given synsets:', given
        counted = [p[0] for p in self.wn_helper.lemma_counter(
            word, pos).most_common()]
        # print 'Counted synsets:', counted
        cap = [s for s in given if s in counted]
        if not cap:
            counted.extend(given)
            cap = counted
            # print 'Cap:', cap
            selection = [s for s in given if s in cap]

        # Cross check selection with ImageNet retrieval.
        visualized = [s for s in selection if self.in_helper.in_imagenet(s)]
        # print 'In ImageNet:', selection
        if not visualized:
            visualized = selection
            # print 'Visualized:', visualized

        # Merge textual and visual selection prioritizing visual clues.
        if selection:
            result = visualized.pop(0)
        else:
            result = None
        return result
