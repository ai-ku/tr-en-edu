#!/usr/bin/env python

import os, sys, re, random, math
from collections import namedtuple

aln_file = sys.argv[1]
aln_q = float(sys.argv[2])
out = sys.argv[3]

class lang_id:
    def __init__(self):
        self.count = {}
        self.prob = {}

    def add_words(self, sent):
        for s in sent.split():
            try:
                self.count[s] += 1
            except:
                self.count[s] = 1

    def extend_dict(self, other_dict):
        for k in other_dict.iterkeys():
            self.count.setdefault(k, 0)

    def make_prob_dict(self):
        total = float(sum(self.count.itervalues()) + len(self.count))
        for k, v in self.count.iteritems():
            self.prob[k] = math.log((v + 1.0) / total)

    def sent_prob(self, sent):
        p = 0
        for s in sent.split():
            try:
                p += self.prob[s]
            except:
                p = -float('inf')
                break
        return p

tr_id = lang_id()
en_id = lang_id()

file_name = ""
file_count = 0
file_lines = []
for line in open(aln_file):
    line = line.rstrip().split('\t')
    if line[0] == '' or line[1] == '':
        continue
    tr_id.add_words(line[0])
    en_id.add_words(line[1])
    file_lines.append((line[0], line[1], line[2], file_name))

sys.stderr.write("Total files: %d\n" % file_count)

tr_id.extend_dict(en_id.count)
en_id.extend_dict(tr_id.count)
tr_id.make_prob_dict()
en_id.make_prob_dict()

f0 = open(out + ".tr", 'w')
f1 = open(out + ".en", 'w')
deleted = 0
passed_filter = 0
for line in file_lines:
    tr_p_tr = tr_id.sent_prob(line[0])
    tr_p_en = en_id.sent_prob(line[0])
    en_p_tr = tr_id.sent_prob(line[1])
    en_p_en = en_id.sent_prob(line[1])
    if tr_p_tr < tr_p_en or en_p_en < en_p_tr:
        deleted += 1
        continue
    if aln_q <= float(line[2]):
        f0.write(line[0])
        f0.write("\n")
        f1.write(line[1])
        f1.write("\n")
        passed_filter += 1

sys.stderr.write("%d pairs in same lang, deleted\n" % deleted)
sys.stderr.write("%d pairs passed filtering\n" % passed_filter)

f0.close()
f1.close()
