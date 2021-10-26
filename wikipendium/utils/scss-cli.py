'''
A lightweight cli wrapper for libsass-python. This is used to integrate
libsass-python with django-compressor. Django-compressor can work with either
command line arguments or specially defined Filters. Implementing a lightweight
cli wrapper seemed to be the more lightweight of the two options. As a bonus,
this may be called externally as well, e.g. for testing or debugging.
'''

import codecs
import sass
import sys


def main():
    if len(sys.argv) != 2:
        print('Usage: python sass-cli.py filename.sass')
        sys.exit(1)
    filename = sys.argv[1]
    with codecs.open(filename, encoding='utf-8', mode='r') as f:
        print(sass.compile(string=f.read()))


if __name__ == '__main__':
    main()
