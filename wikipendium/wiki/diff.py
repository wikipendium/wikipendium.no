"""HTML Diff: http://www.aaronsw.com/2002/diff
Rough code, badly documented. Send me comments and patches."""

"""Modified to parse markdown and ignore HTML"""

__author__ = 'Aaron Swartz <me@aaronsw.com>'
__copyright__ = '(C) 2003 Aaron Swartz. GNU GPL 2 or 3.'
__version__ = '0.22'

import difflib
import string


def textDiff(a, b):
    """Takes in strings a and b and returns a human-readable HTML diff."""

    out = []
    a, b = html2list(a), html2list(b)
    s = difflib.SequenceMatcher(None, a, b)
    for e in s.get_opcodes():
        if e[0] == "replace":
            # @@ need to do something more complicated here
            # call textDiff but not for html, but for some html... ugh
            # gonna cop-out for now
            out.append(
                '<del class="diff modified">' +
                ''.join(a[e[1]:e[2]]) +
                '</del><ins class="diff modified">' +
                ''.join(b[e[3]:e[4]]) +
                "</ins> "
                )
        elif e[0] == "delete":
            out.append('<del class="diff">' + ''.join(a[e[1]:e[2]]) + "</del>")
        elif e[0] == "insert":
            out.append('<ins class="diff">' + ''.join(b[e[3]:e[4]]) + "</ins>")
        elif e[0] == "equal":
            out.append(
                '<span class="diff equal hidden">' +
                ''.join(b[e[3]:e[4]]) +
                '</span>'
                )
        else:
            raise "Um, something's broken. I didn't expect a '" + \
                repr(e[0]) + "'."
    return ''.join(out)


def html2list(x, b=0):
    cur = ''
    out = []
    for c in x:
        if c in string.whitespace:
            out.append(cur+c)
            cur = ''
        else:
            cur += c
    out.append(cur)
    return filter(lambda x: x is not '', out)


if __name__ == '__main__':
    import sys
    try:
        a, b = sys.argv[1:3]
    except ValueError:
        print "htmldiff: highlight the differences between two html files"
        print "usage: " + sys.argv[0] + " a b"
        sys.exit(1)
    print textDiff(open(a).read(), open(b).read())
