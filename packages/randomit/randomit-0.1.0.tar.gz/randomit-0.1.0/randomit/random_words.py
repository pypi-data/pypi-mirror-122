import random
from pathlib import Path

WORDS_FILE = Path(__file__).parent.resolve() / 'random_words.txt'

# TODO: at some point, make functions chain.
class Words:

    def get_random_word(self):

        with open(WORDS_FILE, 'r') as all_words:
            return random.choice([word.replace('\n', '') for word in all_words])

    # if words_to_return = 0 or not specified -> returns all words.
    def get_random_words(self, words_to_return: int = 0):

        with open(WORDS_FILE, 'r') as all_words:

            list_of_words = []

            for words in all_words:
                word = words.replace('\n', '')
                list_of_words.append(word)

        if words_to_return:
            return [list_of_words[random.randrange(0, len(list_of_words))] for _ in range(words_to_return)]
        else:
            return list_of_words

    # if words_to_return = 0 or not specified -> returns all matched words.
    def get_random_words_that_starts_with(self, letter: str, words_to_return: int = 0):

        found_words = []

        if letter != '':
            with open(WORDS_FILE, 'r') as all_words:
                for words in all_words:
                    word = words.replace('\n', '')

                    if word.startswith(str(letter.lower())):
                        found_words.append(word)

            if words_to_return:
                return found_words[:words_to_return]
            else:
                return found_words