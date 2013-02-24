import subprocess
import random
import hashlib

class MergeError(Exception):
    def __init__(self, diff):
        self.diff = diff
    def __unicode__(self):
        return unicode(diff)

def merge(a, ancestor, b):

    apath = generate_path(a)
    bpath = generate_path(b)
    ancestorpath = generate_path(ancestor)

    afile = open(apath, 'w+')
    for line in a:
        afile.write(line)
    afile.close()

    bfile = open(bpath, 'w+')
    for line in b:
        bfile.write(line)
    bfile.close()

    ancestorfile = open(ancestorpath, 'w+')
    for line in ancestor:
        ancestorfile.write(line)
    ancestorfile.close()

    try:
        merged = subprocess.check_output(['diff3', '-m', apath, ancestorpath, bpath])
    except subprocess.CalledProcessError as e:
        raise  MergeError(e.output)

    subprocess.call(['rm',apath])
    subprocess.call(['rm',bpath])
    subprocess.call(['rm',ancestorpath])

    print "merging..."
    print "======="
    print a
    print "======="
    print b
    print "======="
    print merged
    print "======="

    return merged


def generate_path(string):
    path = 'tmp/diff/'
    path += str(hashlib.md5(string).hexdigest())
    path += str(random.random()*10000000)
    return path
