# -*- coding: utf-8 -*-


from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class AnchorNofollowProcessor(Treeprocessor):

    def run(self, node):
        if node.tag == 'a':
            node.set('rel', 'nofollow')
        for child in node:
            self.run(child)


class AnchorNofollowExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.treeprocessors.add('anchor-nofollow',
                              AnchorNofollowProcessor(md),
                              '_end')
