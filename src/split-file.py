#!/usr/bin/env python

import sys

file = sys.argv[1]
parts = int(sys.argv[2])

with open(file, 'r') as f:
    lines = f.readlines()

chunk = (len(lines) + parts - 1) / parts
for i in xrange(parts):
    with open("%s.%03d" % (file, i), 'w') as f:
        for j in xrange(i * chunk, min((i + 1) * chunk, len(lines))):
            f.write(lines[j])
