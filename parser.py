import re

from typing import List

from gametree import (Character, Action, Dialogue, Narration,
                      Episode, Scene, GameTree, Alias, Unalias,
                      Fork, Choice, Consequence)

# TOKENS
CHARACTER_LIST = 'CHARACTERS:'
NARRATION_OPEN = '~'
DIALOGUE_OPEN = ': '
ALIAS = 'ALIAS'
AS = 'AS'
UNALIAS = 'UNALIAS'
CONSEQUENCE_OPEN = '->'
END = 'END'
MARKER_OPEN = '{'
MARKER_CLOSE = '}'
FORK_OPEN = 'P:'
CHOICE_OPEN_PATTERN = '^[0-9]*\. '
NUMBER_PATTERN = '[0-9]*'
CONSEQUENCE_OPEN_PATTERN = '^%s *%s' % (NUMBER_PATTERN, CONSEQUENCE_OPEN)
VALID_TEXT_PATTERN = '[^%s%s\n]*' % (MARKER_OPEN, MARKER_CLOSE)


def parse_script(contents: str) -> GameTree:
    # TODO: this should parse multiple scenes.
    rest, scene = parse_scene(contents)
    if consume_space(rest) != '':
        raise ValueError('Malformed GameTree')
    return GameTree(scene)


def parse_scene(contents: str) -> (str, Scene):
    rest = contents
    characters = None
    if has_characters(rest):
        rest, characters = parse_characters(rest)
    rest, episodes = parse_episodes(rest)
    rest = consume(rest, END)
    return rest, Scene(episodes, characters)


def has_characters(contents: str) -> bool:
    return contents.startswith(CHARACTER_LIST)


def parse_characters(contents: str) -> (str, List[Character]):
    rest = consume(contents, CHARACTER_LIST)
    rest = consume_space(rest)
    characters = []
    while not rest.startswith('\n'):
        rest, character = parse_character(rest)
        characters.append(character)
    rest = consume_space(rest)
    return rest, characters


def parse_character(contents: str) -> (str, Character):
    names, rest = read_lines(contents, 1)
    names = [n.lstrip() for n in names.split(',')]
    if len(names) == 2:
        name, code_name = names
    else:
        name = names[0]
        code_name = None
    return rest, Character(name, code_name)


def parse_episodes(contents: str) -> (str, List[Episode]):
    rest = contents
    episodes = []
    while has_episode(rest):
        rest, episode = parse_episode(rest)
        episodes.append(episode)
    rest = consume_space(rest)
    return rest, episodes


def has_episode(contents: str) -> bool:
    return has_marker(contents.lstrip())


def has_marker(contents: str) -> bool:
    return contents.startswith(MARKER_OPEN)


def parse_episode(contents: str) -> (str, Episode):
    rest = contents.lstrip()
    rest, title = parse_marker(rest)
    rest = consume_space(rest)
    rest, actions = parse_actions(rest)
    return rest, Episode(title, actions)


def parse_marker(contents: str) -> (str, str):
    marker_line, rest = read_lines(contents, 1)
    marker = marker_line.strip()[1:-1]
    return rest, marker


def parse_actions(contents: str) -> (str, List[Action]):
    rest = contents
    actions = []
    while has_action(rest):
        rest, action = parse_action(rest)
        actions.append(action)
        rest = consume_space(rest)
    return rest, actions


def has_action(contents: str) -> bool:
    return (has_narration(contents)
            or has_dialogue(contents)
            or has_alias(contents)
            or has_unalias(contents)
            or has_fork(contents))


def has_narration(contents: str) -> bool:
    return contents.lstrip().startswith(NARRATION_OPEN)


def has_dialogue(contents: str) -> bool:
    return DIALOGUE_OPEN in contents.split('\n')[0]


def has_alias(contents: str) -> bool:
    return contents.lstrip().startswith(ALIAS)


def has_unalias(contents: str) -> bool:
    return contents.lstrip().startswith(UNALIAS)


def has_fork(contents: str) -> bool:
    return contents.startswith(FORK_OPEN)


def parse_action(contents: str) -> (str, Action):
    rest, concrete_action = parse_concrete_action(contents)
    rest = consume_sameline_space(rest)
    marker = None
    if has_marker(rest):
        rest, marker = parse_marker(rest)
    return rest, Action(concrete_action=concrete_action,
                        transition_marker=marker)


def parse_concrete_action(contents: str):
    if has_narration(contents):
        return parse_narration(contents)
    elif has_dialogue(contents):
        return parse_dialogue(contents)
    elif has_alias(contents):
        return parse_alias(contents)
    elif has_unalias(contents):
        return parse_unalias(contents)
    elif has_fork(contents):
        return parse_fork(contents)
    else:
        assert False


def parse_narration(contents: str) -> (str, Narration):
    # TODO: this assumes the narration is all on one line.
    rest = contents.lstrip().lstrip(NARRATION_OPEN).lstrip()
    narrative_text = re.match(VALID_TEXT_PATTERN, rest).group(0).strip()
    rest = rest.replace(narrative_text, '', 1)
    return rest, Narration(text=narrative_text)


def parse_dialogue(contents: str) -> (str, Dialogue):
    # TODO: this assumes the dialogue is all on one line.
    speaker_id, rest = contents.lstrip().split(DIALOGUE_OPEN, 1)
    dialogue_text = re.match(VALID_TEXT_PATTERN, rest).group(0)
    rest = rest.replace(dialogue_text, '', 1)
    return rest, Dialogue(speaker_id=speaker_id, text=dialogue_text)


def parse_alias(contents: str) -> (str, Alias):
    alias_action, rest = read_lines(contents, 1)
    name, alias = [s.strip() for s in
                   alias_action.strip().lstrip(ALIAS).split(AS, 1)]
    return rest, Alias(character_name=name, alias=alias)


def parse_unalias(contents: str) -> (str, Unalias):
    unalias_action, rest = read_lines(contents, 1)
    name = unalias_action.lstrip().lstrip(UNALIAS).strip()
    return rest, Unalias(character_name=name)


def parse_fork(contents: str) -> (str, Fork):
    rest = contents.strip(FORK_OPEN)
    rest = consume_space(rest)
    choices = []
    while has_choice(rest):
        rest, choice = parse_choice(rest)
        choices.append(choice)

    rest = consume_space(rest)
    consequences = []
    while has_consequence(rest):
        rest, consequence = parse_consequence(rest)
        consequences.append(consequence)

    # TODO: this hack is to keep the 'actions' subrule
    # of 'consequence' from consuming all the newlines
    # up to the next episode title, which makes it look
    # like a transition marker of the 'fork' action.
    # A solution here is to make the transition markers
    # and the episode titles different.
    if consequences:
        rest = '\n' + rest

    return rest, Fork(choices=choices, consequences=consequences)


def has_choice(contents: str) -> bool:
    return bool(re.match(CHOICE_OPEN_PATTERN, contents))


def has_consequence(contents: str) -> bool:
    return bool(re.match(CONSEQUENCE_OPEN_PATTERN, contents))


def parse_choice(contents: str) -> (str, Choice):
    ordinal = int(re.match('^' + NUMBER_PATTERN, contents).group(0))
    rest = re.sub(CHOICE_OPEN_PATTERN, '', contents, count=1)
    text, rest = read_lines(rest, 1)
    return rest, Choice(ordinal=ordinal, text=text)


def parse_consequence(contents: str) -> (str, Consequence):
    ordinal = int(re.match('^' + NUMBER_PATTERN, contents).group(0))
    rest = re.sub(CONSEQUENCE_OPEN_PATTERN, '', contents)
    rest = consume_space(rest)
    rest, actions = parse_actions(rest)
    return rest, Consequence(ordinal=ordinal, actions=actions)


# Utility functions:

def consume(contents: str, to_consume: str) -> str:
    if not contents.startswith(to_consume):
        raise ValueError('Failed to consume %s' % to_consume)
    else:
        return contents.lstrip(to_consume)


def consume_space(contents: str) -> str:
    return contents.lstrip()


def consume_sameline_space(contents: str) -> str:
    return contents.lstrip(' ').lstrip('\t')


def read_lines(contents: str, num_lines: int) -> (str, str):
    return contents.split('\n', num_lines)
