#!/usr/bin/env python3

# Note: The work of processing the indefinite sequence of words (via a Python
# generator) is done in wc_on_geneator(). The rest of the code is about making
# this a nice-to-use program!

import argparse
import re
import os
import sys
import time

from collections import deque
from itertools import count
from urllib import request

# Looking for a dataset?
# Try -u http://www.gutenberg.org/files/1524/1524-0.txt


def get_words(text):
    word_pattern = re.compile("\w+")
    return re.findall(word_pattern, text)


def get_words_from_url(url):
    resource = request.urlopen(url)
    text = resource.read().decode("utf-8")
    return get_words(text)

def get_words_from_file(filename):
    with open(filename) as infile:
        text = infile.read()
    return get_words(text)

def get_words_from_stdin():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        for word in get_words(line):
            yield word


def wc_on_generator(word_generator, window_size, exclude_words):
    lru_word_cache = deque()
    wc = {}
    lru_item = None
    counter = count()
    for word in word_generator:
        # don't count any word being excluded; however, we still must cache, because it is part of the window of words
        if word.lower() not in exclude_words:
            wc[word] = wc.get(word, 0) + 1
        lru_word_cache.append(word)
        if len(lru_word_cache) > window_size:
            lru_item = lru_word_cache.popleft()
            wc[lru_item] = lru_item_count = wc.get(lru_item, 1) - 1
            if lru_item_count > 0:
                del(wc[lru_item])

        # Make this more like a "view" of the generator state

        yield {'seq': next(counter),
               'word': word,
               'is_stop_word': word.lower() in exclude_words,
               'word_counts': wc,
               'lru_word': "*" if not lru_item else lru_item}


def get_top_counts(wc, top):
    items = [(wc[word], word) for word in wc]
    items.sort(reverse=True)

    if len(items) > top:
        items = items[0:top]

    return ", ".join(["%(word)s (%(count)d)" % vars() for (count, word) in items])


def get_argparser():
    parser = argparse.ArgumentParser(
        description="Word Count with Sliding Window (by Number of Words)")
    parser.add_argument("-w", "--window-size",
                        type=int, default=100, help="window size (in words)")
    parser.add_argument("-v", "--view-window-size", type=int, default=1, help="only show results for every specified number of rows (based on window-size")

    parser.add_argument("-n", "--numlines",
                        type=int, default=10, help="maximum lines of output")
    parser.add_argument("-t", "--top",
                        type=int, default=5, help="show top ranked (number of) items")
    parser.add_argument("-z", "--zzz", type=float,
                        help="sleep for seconds (float allowed, e.g. 0.05) between writing output lines", default=0)

    parser.add_argument("-s", "--stop-words",
                        type=str, default=None, help="file containing stop words (words separated by whitespace")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--url",
                       type=str, default=None, help="url to process")
    group.add_argument("-f", "--filename",
                       type=str, default=None, help="filename to process")
    group.add_argument("-i", "--stdin", action="store_true",
                       default=False, help="get text from standard input")
    return parser


# See https://docs.python.org/3/library/signal.html. Python provides full
# support for POSIX in the os module and full support for signal handling.
# Only output pipes require you to address borken pipes, which is also needed
# in C programming.

def main():
    arg_parser = get_argparser()
    args = arg_parser.parse_args()

    if args.stop_words:
        with open(args.stop_words) as infile:
            text = infile.read()
            words = get_words(text)
            exclude_words = set([word.lower() for word in words])
    else:
        exclude_words = set()

    if args.url:
        words = get_words_from_url(args.url)
    elif args.stdin:
        words = get_words_from_stdin()
    elif args.filename:
        words = get_words_from_file(args.filename)
    else:
        arg_parser.print_help()
        sys.stderr.write("\n--url or --stdin not specified (aborting)\n")
        sys.exit(1)

    window_size = max(1, args.window_size)
    view_window_size = max(1, args.view_window_size)

    wc_generator = wc_on_generator(words, window_size, exclude_words)

    # This try/except is straight out of the Python docs (for output SIGPIPE)

    try:
        line_counter = count()
        for wc_result in wc_generator:
            current_count = next(line_counter)
            if current_count >= args.numlines:
                break
            if (current_count+1) % view_window_size != 0:
                continue
            view_start = max(current_count - window_size + 1, 0)
            env = wc_result.copy()
            env['counts'] = get_top_counts(wc_result['word_counts'], args.top)
            env['noise_flag'] = "*" if wc_result['is_stop_word'] else ""
            env['view_start'] = view_start
            sys.stdout.write("[%(view_start)d-%(seq)d = %(word)s%(noise_flag)s]: " % env)
            sys.stdout.write("%(counts)s; %(lru_word)s (dropped)\n\n" % env)
            sys.stdout.flush()
            if args.zzz:
                time.sleep(args.zzz)
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE


if __name__ == '__main__':
    main()
