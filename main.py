import parser
import player

STORY_FILE = 'scripts/sample_input.txt'


if __name__ == '__main__':
    with open(STORY_FILE) as f:
        player.play(parser.parse_script(f.read()))
