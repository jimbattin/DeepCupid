from __future__ import print_function

import sys
import random


if sys.version_info < (3,):
    range = xrange


class Markov(object):
    def __init__(self, words):
        self.words = words
        self.word_size = len(words)
        self.database = {}

        if self.word_size < 3:
            raise Exception('Word chunk size should be less than word dictionary size')

        self.build_database()

    def build_database(self):
        for i in range(self.word_size - 3):
            chunk = self.words[i:i + 3]
            key = tuple(chunk[0:2])
            value = chunk[-1]

            if key in self.database:
                self.database[key].append(value)
            else:
                self.database[key] = [value]

    def chain(self, size=50, seed_word=None):
        if seed_word is None:
            seed = random.randint(0, self.word_size - 3)
        else:
            for index, word in enumerate(self.words):
                if index == self.word_size - 2:
                    raise Exception("Can't seed with word: '{0}'".format(seed_word))
                elif word == seed_word:
                    seed = index
                    break

        w1, w2 = self.words[seed:seed + 2]
        gen_words = []

        for i in range(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.database[(w1, w2)])
        gen_words.append(w2)

        return ' '.join(gen_words)


if __name__ == '__main__':
    with open(sys.argv[1]) as word_file:
        words = word_file.read().split()
        markov = Markov(words=words)

        print(markov.chain(
            size=int(sys.argv[2]) if len(sys.argv) > 2 else 50,
            seed_word=sys.argv[3] if len(sys.argv) > 3 else None
        ))
