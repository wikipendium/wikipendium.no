# -*- coding: utf-8 -*-

"""
Wikitables extension for Python-Markdown
========================================

|| Row 1, col 1 || Row 1, col 2 ||
|| Row 2, col 1 || Row 2, col 2 ||

Based on wiki_tables extra in python-markdown2
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class WikiTableProcessor(BlockProcessor):

    def test(self, parent, block):
        """ Test if block is wikitable markup """

        if "||" not in block:
            return False

        wiki_table_re = re.compile(r'''
            (?:(?<=\n\n)|\A\n?)            # leading blank line
            ^([ ]{0,3})\|\|.+?\|\|[ ]*\n  # first line
            (^\1\|\|.+?\|\|\n)*        # any number of subsequent lines
            ''', re.M | re.X)
        return wiki_table_re.match(block) is not None

    def run(self, parent, blocks):
        """ Convert markdown to html """

        # Pop of the current block
        block = blocks.pop(0)

        rows = []
        for line in block.splitlines(0):
            line = line.strip()[2:-2].strip()
            row = [c.strip() for c in re.split(r'(?<!\\)\|\|', line)]
            rows.append(row)

        main = etree.SubElement(parent, 'table')
        tbody = etree.SubElement(main, 'tbody')
        for row in rows:
            hrow = etree.SubElement(tbody, 'tr')
            for cell in row:
                c = etree.SubElement(hrow, 'td')
                c.text = cell


class WikiTableExtension(Extension):
    """ Add wikitables to Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        md.parser.blockprocessors.add('wiki-table',
                                      WikiTableProcessor(md.parser),
                                      '<hashheader')
