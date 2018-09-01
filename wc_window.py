#!/usr/bin/env python3

import argparse
import re

from collections import deque
from urllib import request

# Looking for a dataset?
# Try -u http://www.gutenberg.org/files/1524/1524-0.txt


def get_text_from_url(url):
    resource = request.urlopen(url)
    return resource.read().decode("utf-8")


def get_words(text):
    word_pattern = re.compile("\w+")
    return re.findall(word_pattern, text)


def wc_on_generator(word_generator, window_size):
    lru_word_cache = deque()
    wc = {}
    for word in word_generator:
        wc[word] = wc.get(word, 0) + 1
        lru_word_cache.append(word)
        if len(lru_word_cache) > window_size:
            lru_item = lru_word_cache.popleft()
            wc[lru_item] = wc.get(lru_item, 1) - 1
        yield wc


def show_counts(wc, top):
    items = [(wc[word], word) for word in wc]
    items.sort(reverse=True)

    if len(items) > top:
        items = items[0:top]

    return ", ".join(["%(word)s: %(count)d" % vars() for (count, word) in items])


def parse_args():
    parser = argparse.ArgumentParser(description="Word Count / Sliding Stream")
    parser.add_argument("-w", "--window_size",
                        type=int, default=100, help="window size (in words)")
    parser.add_argument("-H", "--head",
                        type=int, default=10, help="number of lines to process")
    parser.add_argument("-t", "--top",
                        type=int, default=5, help="show top ranked (number of) items")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--url",
                       type=str, default=None, help="url to process")
    group.add_argument("-p", "--pipe", action="store_true",
                       default=False, help="pipe from standard input")
    return parser.parse_args()


def main():
    args = parse_args()

    text = ''  # by default, no words to process
    if args.url:
        text = get_text_from_url(args.url)

    words = get_words(text)
    wc_generator = wc_on_generator(words, args.window_size)
    for window in range(0, args.head):
        print("%d:" % window, show_counts(next(wc_generator), args.top))
        print()


if __name__ == '__main__':
    main()
