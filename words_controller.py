from words_model import TextParser
from pynput.keyboard import Key, Listener
import queue
import time


q = queue.Queue()


def on_press(key):
    global q

    if key == Key.right:
        q.put(True)

    if key == Key.left:
        q.put(False)

listener = Listener(on_press=on_press)


class Controller:
    global listener

    def __init__(self):
        listener.start()

    def __del__(self):
        listener.stop()

    def is_known(self):
        while q.empty():
            time.sleep(0.1)

        return q.get()


def main(filename):
    try:
        with open(filename) as fin:
            text = fin.read()

        text_parser = TextParser(text)
        controller = Controller()

        for word in text_parser:
            print(word)
            text_parser.add_last_word_to_db(controller.is_known())

        with open("output.txt", "w") as fout:
            fout.write('\n'.join(text_parser.get_unlearned_words()))

    except FileNotFoundError:
        print('File "' + filename + '" was not found')

main("input.txt")
