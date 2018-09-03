# Synopsis

This repo contains a Python (imperative but hopefully elegant) version of Konstantin Laufer's delightful variant of word count, which does word count on an indefinite (potentially infinite) stream with a sliding window, where the window size is based on a number of words.

In the Python solution, we take advantage of _generators_, which is Python's way of being able to support _infinitary programming_. It is similar to the iterator concept in Java and Scala but is more similar to the backtracking mechanism found in Prolog and Icon (Griswold), which allows functions to be "suspended" and, therefore, to yield multiple results. In Python, the results of a generator are triggered by next().

# Usage

./sliding-wc.py --help shows you the various options.

# Examples

Process sliding word count from standard in.

```
$ cat hamlet.txt | ./sliding-wc.py --stdin  --numlines 1000 --top 8 --window_size 500 
```

Ditto but use the `less` pager. Should not result in a broken pipe.


```
$ cat hamlet.txt | ./sliding-wc.py --stdin  --numlines 1000 --top 8 --window_size 500 | less
```

Read from standard in but slow the output down with a 0.05 second delay between lines of output written.

```
$ cat hamlet.txt | ./sliding-wc.py --stdin  --numlines 1000 --top 8 --window_size 500 --zzz 0.05
```

Read from URL. This example is the original source for `hamlet.txt` in the preceding exmaples.

```
./sliding-wc.py --url http://www.gutenberg.org/files/1524/1524-0.txt  --head 1000 --top 8 --window_size 500 | less
```

Use an infinite stream producer like `yes` to calculate sliding word count indefinitely.

```
yes a b c d e f g h i j k l m n o p q r s t u v w x y z  | ./sliding-wc.py --stdin --numlines 10000 --top 5 --window_size 500 --zzz 0.01
```

Exclude stop words from consideration (`data/stop-word-list.txt` contains some common/known English words but may not be exhaustive).

```
./sliding-wc.py --url http://www.gutenberg.org/files/1524/1524-0.txt  --numlines 100 --top 10 --window_size 1000 --stop_words data/stop-word-list.txt | less

``` 

By default, sliding-wc shows the analysis for _every_ word in the stream. We have an option to set a _view window_, which is how many words at a time you'd like to see the analysis.

In the following, we show only the sliding word count every 1000 words. The number of previous words considered is 1500. 

As you can see in the output, the first range is `0-999` (as only 1000 words have been seen at that point. When we get to the next range (500-1999) we have seen more than 1500 words. The program is smart enough to know when the window size and view window size are different.

In case there is any confusion, 0-999 means that the counts reported are only for words from position 0 through 999 in the input.

```
./sliding-wc.py --filename data/hamlet.txt  --numlines 10000 --top 10 --window-size 1500 --view-window-size 1000 --zzz 0.0 

[0-999 = of]: the (40), of (25), Scene (20), in (19), A (19), I (18), and (17), BARNARDO (17), to (16), Castle (16); * (dropped)

[500-1999 = this]: with (17), that (15), by (12), we (11), his (11), so (8), be (8), which (7), on (7), like (7); awhile (dropped)

[1500-2999 = father]: your (10), KING (7), shall (6), Laertes (6), HAMLET (6), nature (5), must (5), leave (5), father (5), duty (5); god (dropped)

[2500-3999 = The]: would (7), HORATIO (7), was (6), had (6), see (5), as (5), very (4), upon (4), she (4), saw (4); Of (dropped)

[3500-4999 = are]: OPHELIA (9), POLONIUS (8), LAERTES (7), Ophelia (5), yourself (4), soul (4), oft (4), loves (4), honour (4), Give (4); hands (dropped)

[4500-5999 = done]: go (8), ll (6), follow (6), GHOST (5), yourself (4), call (4), What (4), waves (3), vows (3), thus (3); ear (dropped)

[5500-6999 = sorry]: GHOST (9), villain (5), into (4), horrible (4), ho (4), ghost (4), foul (4), away (4), _Within (4), _ (4); and (dropped)

[6500-7999 = takes]: or (9), REYNALDO (9), lord (8), There (7), Swear (7), him (6), villain (5), sword (5), so (5), sir (5); off (dropped)

[7500-8999 = our]: He (6), sir (5), did (5), Rosencrantz (5), Guildenstern (5), son (4), other (4), much (4), he (4), closes (4); REYNALDO (dropped)

[8500-9999 = a]: QUEEN (8), KING (8), time (6), from (5), Rosencrantz (5), Guildenstern (5), think (4), much (4), dear (4), daughter (4); _ (dropped)

```

