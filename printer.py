import time
from typing import List, Tuple


CHARACTER_PAUSE = .07
MID_PUNCTUATION_PAUSE = .15
END_SENTENCE_PAUSE = .2
END_OF_LINE_PAUSE = .5
SPEAKER_NAME_PAUSE = .2

CHARACTERS_PER_LINE = 80

MID_SENTENCE_PUNCTUATION = {',', ';', ':'}
END_SENTENCE_PUNCTUATION = {'.', '!', '?'}

FAST_TEXT_PAUSE = .01


class Color:

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# TODO: make sure the punctuation pauses don't
# interfere with possible cases where punctuation
# markers are not used as punctuation.
def put(text: str, plain=False) -> None:
    newline_on_next_space = False
    chars_on_line = 0
    for c in text:
        if c == ' ' and newline_on_next_space:
            print()
            newline_on_next_space = False
            continue

        print(c, end='', flush=True)
        if not plain and c in MID_SENTENCE_PUNCTUATION:
            pause(MID_PUNCTUATION_PAUSE)
        elif not plain and c in END_SENTENCE_PUNCTUATION:
            pause(END_SENTENCE_PAUSE)
        else:
            pause(CHARACTER_PAUSE)

        chars_on_line += 1
        if chars_on_line % CHARACTERS_PER_LINE == 0:
            newline_on_next_space = True


def pause(seconds: float) -> None:
    time.sleep(seconds)


def print_line(line: str) -> None:
    put(line)
    pause(END_OF_LINE_PAUSE)
    print()
    print()


def print_dialogue(speaker_name: str,
                   line: str) -> None:
    put(Color.GREEN + speaker_name + ': ' + Color.END, plain=True)
    pause(SPEAKER_NAME_PAUSE)
    print_line(line)


def put_fast(text: str) -> None:
    for c in text:
        print(c, end='', flush=True)
        pause(FAST_TEXT_PAUSE)


def print_choices(choices: List[Tuple[int, str]]) -> None:
    for ordinal, text in choices:
        put_fast(str(ordinal) + '. ' + text)
        print()
    print()


def prompt_user() -> str:
    response = input('>> ')
    print()
    return response
