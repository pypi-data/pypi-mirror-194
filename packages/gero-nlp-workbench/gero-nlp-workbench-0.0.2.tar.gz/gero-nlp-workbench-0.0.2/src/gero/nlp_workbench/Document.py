from os import PathLike

import nltk as nltk


class Document:
    content: str
    words: [str]

    def __init__(self, path: str | bytes | PathLike[str]):
        with open(path) as file:
            self.content = file.read()
            self.words = nltk.word_tokenize(self.content)

    def __str__(self):
        return self.content

    def get_character_amount(self) -> int:
        return len(self.content)

    def find(self, substring: str) -> [str]:
        return self.content.find(substring)

    def number_of_words(self) -> int:
        return len(self.words)

    def get_unique_words(self) -> set:
        return set(self.words)

    def number_of_unique_words(self) -> int:
        return len(self.get_unique_words())

    def get_inverted_index(self) -> {str: [int]}:
        inverted_index = {}
        for (index, word) in enumerate(self.words):
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(index)
        return inverted_index

    def get_character_set(self) -> set:
        return set(self.content)

    def get_character_occurrences(self) -> {chr: int}:
        character_occurrences = {}
        for character in self.content:
            if character not in character_occurrences:
                character_occurrences[character] = 0
            character_occurrences[character] += 1
        return character_occurrences
