from __future__ import annotations
from typing import List, Optional, Dict


class LanguageConfluxer:
    """
    A quick and sorta buggy implementation of Chris Pound's lc
    See http://generators.christopherpound.com/ for details

    Either include the file and use the generate() or generate_word() methods, or call from command line:

    Command line arguments:
        -f=[FILENAME], --file=[FILENAME]    The dictionary file; defaults to 'barsoom.txt' (included)
        -c=[NUMBER], --count=[NUMBER]       How many words to be generated; defaults to 5
        -m=[NUMBER], --min=[NUMBER]         Minimum word length; defaults to 3
        -x=[NUMBER], --max=[NUMBER]         Maximum word length; defauls to 8

    The actual word length is chosen randomly, between min and max.

    TODO: make not buggy
    """

    def __init__(
        self,
        file: str = "barsoom.txt",
        count: int = 5,
        min: int = 3,
        max: int = 8,
    ):
        self.file = file
        self._file = file
        self.count = count
        self.min = min
        self.max = max

        self.words = []
        self.inits = []
        self.pairs = {}

        self.extract_words()
        self.split_words()

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, newfile):
        self._file = newfile
        self.extract_words()
        self.split_words()

    def extract_words(self) -> List[str]:
        """
        Processes the file to extract words
        """

        from re import sub, split

        words: Optional[List[str]] = []

        with open(self.file) as f:
            for line in f:
                line = sub(pattern=r"#.+$", repl="", string=line)
                line = split(pattern=r"\s+", string=line)
                words.extend(line)

        self.words = sorted([w for w in words if len(w) > 0])

    def split_words(self) -> None:
        """
        Splits words into letter pairs
        "word" becomes ["wo", "or", "rd"]
        """

        inits = set()
        pairs = {}

        for word in self.words:
            fragments = [word[i : i + 2] for i in range(len(word) - 1)]
            if len(fragments) > 0:
                inits.add(fragments[0].lower())

                for i in range(len(fragments) - 1):
                    k = fragments[i].lower()
                    f = fragments[i + 1].lower()
                    try:
                        pairs[k].append(f)
                    except KeyError:
                        pairs[k] = [f]

        self.inits = list(inits)
        self.pairs = pairs

    def generate(self) -> List[str]:
        """
        Generates a list of as many words as specified in contructor
        """

        output: List[str] = []

        for _ in range(self.count):
            output.append(self.generate_word())

        return output

    def generate_word(self) -> str:
        """
        Generates a single word
        """

        from random import choice, randint

        ret = choice(self.inits)
        count = randint(self.min, self.max)

        while len(ret) < count:
            try:
                arr = self.pairs[ret[-2:]]
                ret += choice(arr)[1:]
            except KeyError:
                ret = ret[:-2]

                if len(ret) < 2:
                    ret = choice(self.inits)

        return ret.title()


def from_command_line():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        help=f"(str) The file containing your dictionaries; default is 'barsoom.txt'",
        type=str,
        default="barsoom.txt",
    )
    parser.add_argument(
        "--count",
        "-c",
        help="(int) How many words to generate; default is 5",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--min",
        "-m",
        help="(int) Minimum word length; default is 3",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--max",
        "-x",
        help="(int) Maximum word length; default is 8",
        type=int,
        default=8,
    )
    args = parser.parse_args()

    # usage = "Used with "
    for k in args.__dict__.keys():
        usage += f"{k}={args.__dict__.get(k)}, "

    lc = LanguageConfluxer(
        file=args.file,
        count=args.count,
        min=args.min,
        max=args.max,
    )
    print("\n".join(lc.generate()))


if __name__ == "__main__":
    from_command_line()
