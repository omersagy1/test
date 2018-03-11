import time


def print_line(line: str) -> None:
    for c in line:
        print(c, end='', flush=True)
        time.sleep(.05)
    print()
