import subprocess
import random
import hashlib


class MergeError(Exception):
    def __init__(self, diff):
        self.diff = diff

    def __unicode__(self):
        return unicode(self.diff)


def merge(a, ancestor, b):

    apath = generate_path(a)
    bpath = generate_path(b)
    ancestorpath = generate_path(ancestor)

    afile = open(apath, 'w+')
    for line in a:
        afile.write(line.encode('utf-8'))
    afile.close()

    bfile = open(bpath, 'w+')
    for line in b:
        bfile.write(line.encode('utf-8'))
    bfile.close()

    ancestorfile = open(ancestorpath, 'w+')
    for line in ancestor:
        ancestorfile.write(line.encode('utf-8'))
    ancestorfile.close()

    try:
        merged = subprocess.check_output(
            ['diff3', '-m', apath, ancestorpath, bpath]
        )
    except subprocess.CalledProcessError as e:
        subprocess.check_call(['rm', apath])
        subprocess.check_call(['rm', bpath])
        subprocess.check_call(['rm', ancestorpath])
        raise MergeError(e.output)

    subprocess.check_call(['rm', apath])
    subprocess.check_call(['rm', bpath])
    subprocess.check_call(['rm', ancestorpath])

    return merged.decode('utf-8')


def generate_path(string):
    path = 'tmp/diff/'
    path += str(hashlib.md5(string.encode('utf-8')).hexdigest())
    path += str(random.random()*10000000)
    return path
