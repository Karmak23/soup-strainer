# -*- coding: utf-8 -*-
"""
Markup cleaning functions

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import logging
import urlparse

log = logging.getLogger()

import charade

import patterns

from bs4.element import Comment


def remove_whitespace(html):
    """Removes whitespace from an HTML buffer"""

    # NOTE: we still join on space, because in some not-so-rare cases,
    # stripping too much makes 2 words collapse (regularty seen on 1flow).
    return ' '.join([line.strip() for line in html.split('\n')])


def remove_unlikely(soup):
    """Remove tags that are unlikely to have anything of interest"""
    for el in soup.find_all():
        s = ''
        if 'class' in el.attrs:
            s += ''.join(el['class'])
        if 'id' in el.attrs:
            s += el['id']
        if patterns.unlikely.search(s) and (
                not patterns.low_potential.search(s)) and el.name != 'body':
            el.extract()
    return soup


def demote_divs(soup):
    """Demote divs that do not contain other block elements"""
    for el in soup.find_all():
        if el.name == "div":
            if not patterns.significant_children.search(
                    ''.join([e.name for e in el.find_all()])):
                el.name = "p"
    return soup


def remove_breaks(html):
    """Remove BR tags and replace them with Ps"""
    patterns.breaks.sub(u'</p><p>', html)
    return html


def cleanup(soup):
    """Remove unwanted tags and attributes"""
    # remove comments
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]

    # remove unwanted tags
    for t in patterns.strip_tags:
        for f in soup.find_all(t):
            f.extract()

    for t in patterns.sanitizable_tags:
        for f in soup.find_all(t):
            attrs = [a for a in f.attrs.keys()]
            for a in attrs:
                for s in patterns.strip_attrs:
                    if s.search(a):
                        del f[a]
            if 'class' in attrs:
                for s in patterns.strip_classes:
                    new_class = [c for c in f['class'] if not s.search(c)]
                    if len(new_class):
                        f['class'] = new_class
                    else:
                        del f['class']
    return soup


def make_links_absolute(soup, url):
    """Prepend base URL to all hrefs"""
    for el in soup.find_all('a', href=True):
        el['href'] = urlparse.urljoin(url, el['href'])


def set_encoding(soup):

    try:
        enc = charade.detect(soup.get_text())['encoding']

    except:
        log.warning('Could not detect encoding, good luck!')
        return soup

    return soup.encode(enc)
