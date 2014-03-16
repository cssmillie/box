import sys, time
import pandas as pd

def message(text):
    # print message to stderr
    sys.stderr.write('  %s\n' %(text))


def read_list(fn, dtype=str):
    # read file as list
    x = [dtype(line.rstrip()) for line in open(fn)]
    return x


def read_dataframe(fn, index_dtype=str, columns_dtype=str):
    # read file as pandas dataframe
    x = pd.read_table(fn, sep='\t', header=0, index_col=0)
    x.index = x.index.astype(index_dtype)
    x.columns = x.columns.astype(columns_dtype)
    return x


def read_tseries(fn):
    # read file as pandas time series
    return read_dataframe(fn, index_dtype=float, columns_dtype=str)


def iter_fst(fn):
    # generator that returns [sid, seq] pairs in a fasta file
    seq = ''
    for line in open(fn):
        line = line.rstrip()
        if line.startswith('>'):
            if seq != '':
                yield [sid, seq]
            sid = line[1:]
            seq = ''
        else:
            seq += line
    yield [sid, seq]


def iter_fsq(fn):
    # generator that returns records in a fastq file
    record = []
    i = 0
    for line in open(fn):
        i += 1
        if i % 4 == 1:
            if len(record) > 0:
                yield record
            record = []
        record.append(line.rstrip())
    yield record


def read_fst(fn, reverse=False):
    # read fasta file as dictionary
    fst = {}
    for [sid, seq] in iterfst(fst):
        if reverse == False:
            fst[sid] = seq
        elif reverse == True:
            fst[seq] = sid
    return fst

def cycle(x):
    # an efficient way to cycle through a list (similar to itertools.cycle)
    while True:
        for xi in x:
            yield xi

def timer():
    # generator function that measures elapsed time
    t =[]
    while True:
        t.append(time.time())
        if len(t) > 1:
            yield t[-1] - t.pop(0)
        else:
            yield 0
