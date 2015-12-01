#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def clean_text(text):
    return re.sub(r'[^a-zA-Z]+', ' ', text).strip().lower()
