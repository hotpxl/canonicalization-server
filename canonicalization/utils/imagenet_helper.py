#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: Oliver Groth, Yutian Li

"""Contains helper functions for working with ImageNet."""

from __future__ import absolute_import
from __future__ import print_function
import cPickle
import os.path
from nltk.corpus import wordnet
from . import wordnet_helper


class ImageNetHelper(object):

    def __init__(self, res_path):
        self.res_path = res_path
        self.offset_synset_dict = None
        self.imagenet_index_dict = None

    def get_all_wordnet_ids(self):
        """Gets a list of synsets in ImageNet represented by IDs.

        Returns:
            A list of IDs.
        """
        with open(os.path.join(self.res_path, 'imagenet',
                               'imagenet_synsets.txt')) as f:
            return f.readlines()

    def get_offset_synset_dict(self):
        """Gets all synsets visualized in Imagenet.

        Creates a new dictionary on the fly if there is none.

        Returns:
            The dictionary in the format of `{offset: synset}`.
        """
        if self.offset_synset_dict is None:
            dict_path = os.path.join(self.res_path, 'imagenet',
                                     'offset_synset.dict')
            if os.path.isfile(dict_path):
                with open(dict_path, 'rb') as f:
                    self.offset_synset_dict = cPickle.load(f)
            else:
                with open(dict_path, 'wb') as f:
                    syns = list(wordnet.all_synsets())
                    offsets_list = [(s.offset(), str(s)) for s in syns]
                    self.offset_synset_dict = dict(offsets_list)
                    cPickle.dump(self.offset_synset_dict, f,
                                 protocol=cPickle.HIGHEST_PROTOCOL)
        return self.offset_synset_dict

    def wordnet_id_to_synset(self, wordnet_id):
        """Gets the synset associated with a WordNet ID.

        Args:
            wordnet_id: A WordNet ID.

        Returns:
            The synset.

        Raises:
            KeyError: Cannot find the corresponding WordNetID.
        """
        offset = int(wordnet_id[1:].lstrip('0'))
        return self.get_offset_synset_dict()[offset]

    def get_imagenet_index(self):
        """Gets a mapping of all synsets in ImageNet to their WordNet IDs.

        Returns:
            The dictionary in the format of `{synset: wordnet_id}`.
        """
        if self.imagenet_index_dict is None:
            dict_path = os.path.join(
                self.res_path, 'imagenet', 'imagenet_index.dict')
            if os.path.isfile(dict_path):
                with open(dict_path, 'rb') as f:
                    self.imagenet_index_dict = cPickle.load(f)
            else:
                with open(dict_path, 'wb') as f:
                    index_list = []
                    for i, wordnet_id in enumerate(self.get_all_wordnet_ids()):
                        entry = (
                            str(self.wordnet_id_to_synset(wordnet_id)),
                            wordnet_id)
                        index_list.append(entry)
                    self.imagenet_index_dict = dict(index_list)
                    cPickle.dump(self.imagenet_index_dict, f,
                                 protocol=cPickle.HIGHEST_PROTOCOL)
        return self.imagenet_index_dict

    def in_imagenet(self, synset):
        """Checks whether a synset is in ImageNet.

        Args:
            synset: The synset to check.

        Returns:
            Whether it is in ImageNet.
        """
        wordnet_id = wordnet_helper.synset_to_wordnet_id(synset)
        return wordnet_id in self.get_imagenet_index()
