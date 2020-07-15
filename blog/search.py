#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Full Text search capability module for Blogger App"""

from flask import current_app


def add_to_index(index, model):
    """
    Adds certain text from a model with a __searchable__ attribute to
    a search engine index.
    Keyword Arguments:
    index -- The full text index for the text-search tool
    model -- The model that will be queried for any text string
    """
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Removes text stored within the index of a search engine tool.
    Keyword Arguments:
    index -- The full text index for the text-search tool
    model -- The model that will be queried for any text string
    """
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """Function to do a search within an index for a certain query string of
    text. The returning results depend on the provided page and the number of
    results per page within the search."""
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
