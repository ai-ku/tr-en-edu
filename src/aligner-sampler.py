#!/usr/bin/env python

import os, sys, re, random, math
from collections import namedtuple

aln_file = sys.argv[1]
separator_re = re.compile("^hunalign-.+\.aln$")

quality = {}
quality_tested = {}
en_dict = {}
tr_dict = {}

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

SPair = namedtuple('SPair', ['tr', 'en', 'tr_p_tr', 'tr_p_en', 'en_p_tr', 'en_p_en', 'quality', 'file', 'is_good'])
def str_spair(self):
    return """TR> %s
(p_tr: %f, p_en: %f)
EN> %s
(p_tr: %f, p_en: %f)
Quality: %f
File: %s
""" % (self.tr, self.tr_p_tr, self.tr_p_en,
       self.en, self.en_p_tr, self.en_p_en,
       self.quality, self.file)
SPair.str = str_spair

tr_id = lang_id()
en_id = lang_id()

file_name = ""
file_count = 0
file_lines = []
for line in open(aln_file):
    line = line.rstrip()
    if separator_re.search(line):
        file_name = line.split('-')[1]
        file_count += 1
        # if file_count == 10000:
        #     break
        continue
    line = line.split('\t')
    if line[0] == '' or line[1] == '':
        continue
    tr_id.add_words(line[0])
    en_id.add_words(line[1])
    file_lines.append((line[0], line[1], line[2], file_name))

print "Total files: %d" % file_count

tr_id.extend_dict(en_id.count)
en_id.extend_dict(tr_id.count)
tr_id.make_prob_dict()
en_id.make_prob_dict()

deleted = 0
trun_re = re.compile("(\.\d)\d+")
for line in file_lines:
    tr_p_tr = tr_id.sent_prob(line[0])
    tr_p_en = en_id.sent_prob(line[0])
    en_p_tr = tr_id.sent_prob(line[1])
    en_p_en = en_id.sent_prob(line[1])
    if tr_p_tr < tr_p_en or en_p_en < en_p_tr:
        print line[0]
        print line[1]
        deleted += 1
        continue
    bin = "%.1f" % float(trun_re.sub("\\1", line[2]))
    spair = SPair(tr=line[0], en=line[1],
                  tr_p_tr=tr_p_tr, tr_p_en=tr_p_en, en_p_tr=en_p_tr, en_p_en=en_p_en,
                  quality=float(line[2]), file=line[3], is_good=True)
    try:
        quality[bin].append(spair)
    except:
        quality[bin] = [spair]

print "%d pairs have same lang, deleted" % deleted

print "\n".join(["%s\t%d" % (k, len(v)) for k, v in sorted(quality.items(), key=lambda x: float(x[0]))])

read = raw_input
write = sys.stdout.write

def choice_and_remove(bin):
    last = len(quality[bin]) - 1
    r = random.randint(0, last)
    spair, quality[bin][r] = quality[bin][r], quality[bin][last]
    del quality[bin][last]
    return spair

pre = None
while 1:
    bin = read("bin: ").strip()
    if bin == "quit":
        break
    if bin == "" and pre:
        bin = pre
    if quality.get(bin):
        pre = bin
        for i in xrange(5):
            if len(quality[bin]):
                spair = choice_and_remove(bin)
                write(spair.str())
                good = None
                good_ans = set(["y", "n", ""])
                while good not in good_ans:
                    good = read("good (Y/n)? ").strip().lower()
                if good == "n":
                    spair = spair._replace(is_good=False)
                try:
                    quality_tested[bin].append(spair)
                except:
                    quality_tested[bin] = [spair]
            else:
                if i == 0:
                    print "Empty bin"
                else:
                    print "No more entries in bin"
                break
    for k, v in sorted([(float(k), v) for k, v in quality_tested.items()]):
        k = "%.1f" % k
        good = 0
        for spair in v:
            if spair.is_good:
                good += 1
        print "%s => %.2f%% (tested %d)" % (k, 100.0 * good / len(quality_tested[k]), len(quality_tested[k]))

from datetime import datetime
with open("tested.%s" % datetime.now().strftime("%H:%M-%d-%m-%Y"), 'w') as f:
    for k, vals in quality_tested.items():
        for v in vals:
            f.write("%s\t%s\t%f\t%s\t%s\n" % (v.tr, v.en, v.quality, v.file, v.is_good))

print "bye"
