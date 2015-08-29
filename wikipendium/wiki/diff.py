from difflib import SequenceMatcher
from collections import defaultdict


def render_diff_as_html(a, b):
    '''
    Renders the character-by-character diff between
    two strings a and b as HTML.

    Edit operations to get from a to b are rendered
    as combinations of inserts, deletions and equals,
    the latter of which is a noop. Equals-operations
    that span multiple newlines may be rendered as
    partially hidden.
    '''

    # Init a difflib sequence matcher, which is the
    # main engine behind the diff calculation.
    sequence_matcher = SequenceMatcher(a=a, b=b)

    # A dict of html-rendered operations needed
    # to transform string a to string b.
    operations = defaultdict(list)

    def insert(a_from, a_to, b_from, b_to):
        '''Renders an insert operation as HTML.'''
        operations[a_from].append('<ins>%s</ins>' % b[b_from:b_to])

    def delete(a_from, a_to, b_from, b_to):
        '''Renders a delete operation as HTML.'''
        operations[a_from].append('<del>%s</del>' % a[a_from:a_to])

    def equal(a_from, a_to, b_from, b_to,
              start_visible_lines=1, end_visible_lines=1):
        '''
        Renders an equal operation as HTML.
        start_visible_lines defines the number of lines
        in the start of the text that should not be hidden,
        and end_visible_lines defined the number of lines
        in the end of the text that should not be hidden.
        '''

        # The equal operation needs to know line boundaries
        # in the text for abbreviation purposes, so we work
        # with a list of text lines rather than just a single
        # large text string.
        text_lines = a[a_from:a_to].splitlines()

        # Normalise start_visible lines, end_visible_lines for
        # cases where no lines should be truncated/hidden.
        lines_should_be_truncated = (
            start_visible_lines + end_visible_lines < len(text_lines))
        if not lines_should_be_truncated:
            start_visible_lines = len(text_lines)
            end_visible_lines = 0

        # Render the start visible lines as HTML.
        operations[a_from].append('\n'.join(text_lines[:start_visible_lines]))

        # Render the hidden truncated lines as HTML, if any.
        if lines_should_be_truncated:
            operations[a_from].append(
                '<div class=equal-abridged>'
                '<div class=equal-abridged-content>%s</div>'
                '<div class=equal-abridged-placeholder>'
                '<div class=icon-wrapper>'
                '<span class="octicon octicon-unfold"></span>'
                '</div></div></div>' %
                '\n'.join(text_lines[
                    start_visible_lines:
                    len(text_lines)-end_visible_lines]))

        # Render the end visible lines as HTML.
        operations[a_from].append(
            '\n'.join(text_lines[len(text_lines) - end_visible_lines:]))

    # Get the operations needed to transform string a to string b.
    opcodes = sequence_matcher.get_opcodes()

    # Iterate through the opcodes and render them to HTML.
    for opcode in opcodes:
        tag, positions = opcode[0], opcode[1:]
        if tag == 'insert':
            insert(*positions)
        elif tag == 'delete':
            delete(*positions)
        elif tag == 'replace':
            # Replace is really just a delete and
            # an insert, so we render it as such.
            delete(*positions)
            insert(*positions)
        elif tag == 'equal':
            # Normally we want to show one line of visible
            # noop-transformed text at the beginning and the
            # end of the text, and fold away the rest. However,
            # In the case that the noop-transformed text is the
            # very first or the very last piece of text in the
            # rendered diff view, We only want to render visible
            # lines on one side of the fold.
            start_visible_lines = 0 if opcode == opcodes[0] else 1
            end_visible_lines = 0 if opcode == opcodes[-1] else 1
            equal(*positions,
                  start_visible_lines=start_visible_lines,
                  end_visible_lines=end_visible_lines)

    # Finally, the rendered operations are ordered and concatenated,
    # producing the final rendered HTML string.
    return ''.join([''.join(value) for _, value in sorted(operations.items())])
