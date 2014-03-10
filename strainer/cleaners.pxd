#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cython typing for markup cleaning functions

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

cpdef str remove_whitespace(str html)

cpdef object remove_unlikely(object soup)

cpdef object demote_divs(object soup)

cpdef str remove_breaks(str html)

cpdef object cleanup(object soup)

cpdef make_links_absolute(object soup, bytes url)

cpdef object set_encoding(object soup)
