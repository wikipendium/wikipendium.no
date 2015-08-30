# -*- coding: utf-8 -*-

"""
Renders margin notes.

Markdown syntax:

[#] This is a margin note.

"""


from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


class MarginNotesProcessor(BlockProcessor):

    MARGIN_NOTES_MARKER = '[#]'

    def test(self, parent, block):
        """ Test if block is a margin note """
        return block.startswith(self.MARGIN_NOTES_MARKER)

    def run(self, parent, blocks):
        """ Convert markdown to margin notes """
        block = blocks.pop(0)
        if self.test(parent, block):
            note = etree.SubElement(parent, 'div')
            note.attrib['class'] = 'margin-note'
            note.text = block[len(self.MARGIN_NOTES_MARKER):]


class MarginNotesExtension(Extension):
    """ Add marginnotes to Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        md.parser.blockprocessors.add('marginnotes',
                                      MarginNotesProcessor(md.parser),
                                      '<hashheader')
