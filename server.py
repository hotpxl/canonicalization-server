#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yutian Li

from __future__ import absolute_import
from __future__ import print_function
import os.path
import flask
import canonicalization
app = flask.Flask(__name__)

res_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res')
wordnet_mapper = canonicalization.WordNetMapper(res_path)

app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=False
)


@app.route('/canonicalize', methods=['POST'])
def canonicalize():
    app.logger.warning('request with params {}'.format(flask.request))
    if not flask.request.json or 'word' not in flask.request.json:
        return (flask.jsonify({'error': 'unrecognized format'}), 400)
    else:
        res = str(wordnet_mapper.map_word(flask.request.json['word']))
        return flask.jsonify({'result': res})

if __name__ == '__main__':
    app.run()
