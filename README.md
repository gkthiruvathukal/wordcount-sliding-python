This is not a beautiful README file yet.

This repo contains a Python (imperative but hopefully elegant) version of Konstantin Laufer's delightful variant of word count, which does word count on an indefinite (potentially infinite) stream with a sliding window, where the window size is based on a number of words.

In the Python solution, we take advantage of _generators_, which is Python's way of being able to support _infinitary programming_. It is similar to the iterator concept in Java and Scala but is more similar to the backtracking mechanism found in Prolog and Icon (Griswold), which allows functions to be "suspended" and, therefore, to yield multiple results. In Python, the results of a generator are triggered by next().

./wc_window.py --help shows you the various options.

Here are some examples:


Via stdin.

```
$ cat hamlet.txt | ./wc_window.py --stdin  --numlines 1000 --top 8 --window_size 500 
```

Via stdin one page at a time (to test output piping):

```
$ cat hamlet.txt | ./wc_window.py --stdin  --numlines 1000 --top 8 --window_size 500 | less
```

Via stdin and slowing down the output with 0.05 second delay:
```
$ cat hamlet.txt | ./wc_window.py --stdin  --numlines 1000 --top 8 --window_size 500 --zzz 0.05
```

Via URL

```
./wc_window.py --url http://www.gutenberg.org/files/1524/1524-0.txt  --head 1000 --top 8 --window_size 500 | less
```

This is kind of fun:

```
yes a b c d e f g h i j k l m n o p q r s t u v w x y z  | ./wc_sliding.py --stdin --numlines 10000 --top 5 --window_size 500 --zzz 0.01
```

Excluding stop words from a known corpus:

```
./wc_sliding.py --url http://www.gutenberg.org/files/1524/1524-0.txt  --numlines 100 --top 10 --window_size 1000 --stop_words data/stop-word-list.txt | less

``` 

Pedagogical ideas demonsrated:

- Incremental data structure to address least-recently used words (and new worsd) within window.
- Learning to program in the infinite
- Argument parsing / professional packaging of a command
  + Mutually-exclusive command line options (recently discovered by GKT!)
- SIGPIPE handling and Python's delightful os module
- Thinking about the user

Things I still want to do:

- Filter out noise words (a, and, the, etc.)
  + found http://xpo6.com/wp-content/uploads/2015/01/stop-word-list.txt (seems like a good choice for English, anyway)



