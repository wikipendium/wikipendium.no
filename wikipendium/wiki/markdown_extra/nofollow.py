# -*- coding: utf-8 -*-

"""
Adds rel=nofollow to all a elements
"""


from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class NofollowProcessor(Treeprocessor):

    def run(self, root):
        self.set_nofollow(root)
        return root

    def set_nofollow(self, element):
        for child in element:
            if child.tag == 'a':
                child.set('rel', 'nofollow')
            self.set_nofollow(child)  # run recursively on children


class NofollowExtension(Extension):
    """ Add nofollow to Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        md.treeprocessors.add('nofollow',
                              NofollowProcessor(md),
                              '_end')
