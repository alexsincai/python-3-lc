A quick and sorta buggy implementation of [Chris Pound's lc](http://generators.christopherpound.com/)

Either include the file and use the generate() or generate_word() methods, or call from command line:

Command line arguments:

    -f=[FILENAME], --file=[FILENAME]    The dictionary file; defaults to 'barsoom.txt' (included)
    -c=[NUMBER], --count=[NUMBER]       How many words to be generated; defaults to 5
    -m=[NUMBER], --min=[NUMBER]         Minimum word length; defaults to 3
    -x=[NUMBER], --max=[NUMBER]         Maximum word length; defauls to 8

The actual word length is chosen randomly, between min and max.

TODO: make not buggy
