#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yutian Li

from __future__ import absolute_import
from __future__ import print_function
import os.path
import flask
import canonicalization
from canonicalization.utils import common
app = flask.Flask(__name__)

res_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res')
wordnet_mapper = canonicalization.WordNetMapper(res_path)

app.config.update(JSONIFY_PRETTYPRINT_REGULAR=False)


@app.route('/canonicalize', methods=['POST'])
def canonicalize():
    handlers = {
        'object': lambda x: wordnet_mapper.map_word(x),
        'attribute': canonicalization.attribute_mapper.canonicalize_attribute,
        'relationship':
        canonicalization.relationship_mapper.canonicalize_relationship
    }
    if (not flask.request.json or 'text' not in flask.request.json or
            'type' not in flask.request.json or
            flask.request.json['type'] not in handlers):
        return (flask.jsonify({'error': 'unrecognized format'}), 400)
    else:
        res = common.pack_definition(handlers[flask.request.json['type']](
            flask.request.json['text']))
        return flask.jsonify({'result': res})


if __name__ == '__main__':
    app.run(debug=True)
