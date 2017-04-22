import re
import sqlite3
from datetime import datetime


class TextParser:
    def __init__(self, text):
        self.word_pattern = \
            re.compile(r'(^|[\s])?[\'()]?([A-Za-z]+-?[A-Za-z]+)')
        self.text = text
        self.word_iterator = re.finditer(self.word_pattern, self.text)
        self.last_word = 'hi'
        self.db_connection = sqlite3.connect('words_db.sqlite')
        self.db_cursor = self.db_connection.cursor()
        self.select_pattern = \
            "SELECT id FROM words WHERE word = :word"
        self.insert_pattern = \
            "INSERT INTO words (word, learned, date) VALUES (:word, :learned, :date)"
        self.unlearned_words = set()

    def __del__(self):
        self.db_connection.commit()
        self.db_connection.close()

    def __iter__(self):
        return self

    def __next__(self):
        word = next(self.word_iterator).group(2).lower()

        while self.word_is_in_db(word):
            word = next(self.word_iterator).group(2).lower()

        self.last_word = word

        return word

    def word_is_in_db(self, word):
        self.db_cursor.execute(self.select_pattern, {"word": word})

        if self.db_cursor.fetchone() is None:
            return False

        return True

    def add_last_word_to_db(self, known):
        if not known:
            self.unlearned_words.add(self.last_word)

        self.db_cursor.execute(
            self.insert_pattern,
            {"word": self.last_word, "learned": known, "date": datetime.isoformat(datetime.now(), sep=' ')}
        )

    def get_unlearned_words(self):
        return self.unlearned_words
