#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Translator module for Blogger App"""

import json
import uuid
import requests
from flask import current_app
from flask_babel import _


def translate(text, dest_language):
    """Return a translation text for a source text which will be mostly
    present in the body of a post."""

    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
       not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: The translation key is not configured.')

    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate'
    construct_url = base_url + path
    params = {
        'api-version': '3.0',
        'to': dest_language,
    }
    headers = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Content-Type': 'application/json; charset=UTF-8',
        'X-ClientTraceId': str(uuid.uuid4()),
    }
    body = [{
        'Text': text,
    }]
    response = requests.post(construct_url, params=params, headers=headers,
                             json=body)

    if response.status_code != 200:
        return _('Error: The translation service failed.')

    r = json.loads(response.content.decode('utf-8'))
    text = r[0]['translations'][0]['text']
    return text
