#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from . import log

logger = log.get_logger(__name__)


def clean_text(text):
    return re.sub(r'[^a-zA-Z]+', ' ', text).strip().lower()


def pack_definition(res):
    if not res:
        logger.info('result is None')
        return None
    else:
        logger.info('result is {}'.format(res.name()))
        return {'name': res.name(), 'definition': res.definition()}
