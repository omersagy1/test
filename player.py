import gametree as t
import gamestate as s
import printer as p


def play(game_tree: t.GameTree) -> None:

    p.print_line('')
    p.print_line('SAMPLE GAME')

    state = s.GameState(game_tree.scene)
    first_episode = game_tree.scene.episodes[0]
    play_episode(first_episode, state)


def play_episode(episode: t.Episode, state: s.GameState) -> None:
    for action in episode.actions:
        play_action(action, state)


def play_action(action: t.Action, state: s.GameState) -> None:
    concrete_action = action.concrete_action
    if isinstance(concrete_action, t.Narration):
        play_narration(concrete_action)
    elif isinstance(concrete_action, t.Dialogue):
        play_dialogue(concrete_action, state)
    elif isinstance(concrete_action, t.Alias):
        play_alias(concrete_action, state)
    elif isinstance(concrete_action, t.Unalias):
        play_unalias(concrete_action, state)
    elif isinstance(concrete_action, t.Fork):
        play_fork(concrete_action, state)

    if action.transition_marker:
        play_episode(look_up_episode(action.transition_marker, state), state)


def play_narration(narration: t.Narration) -> None:
    p.print_line(narration.text)


def play_dialogue(dialogue: t.Dialogue,
                  state: s.GameState) -> None:
    speaker_display_name = str(look_up_character(
        dialogue.speaker_id, state))

    p.print_dialogue(speaker_display_name,
                     dialogue.text)


def play_alias(alias: t.Alias,
               state: s.GameState) -> None:
    char = look_up_character(alias.character_name,
                             state)
    char.assign_alias(alias.alias)


def play_unalias(unalias: t.Unalias,
                 state: s.GameState) -> None:
    char = look_up_character(unalias.character_name,
                             state)
    char.unalias()


def play_fork(fork: t.Fork, state: s.GameState) -> None:

    def is_valid_answer(answer: str):
        return (answer.isdigit()
                and look_up_consequence(int(answer), fork))

    p.print_choices([(choice.ordinal, choice.text)
                     for choice in fork.choices])
    user_answer = p.prompt_user()
    while not (is_valid_answer(user_answer)):
        user_answer = p.prompt_user()

    consequence = look_up_consequence(int(user_answer), fork)
    play_consequence(consequence, state)


def play_consequence(consequence: t.Consequence, state: s.GameState) -> None:
    for action in consequence.actions:
        play_action(action, state)


def look_up_character(speaker_id: str,
                      state: s.GameState) -> s.Character:
    for c in state.characters:
        if (c.real_name == speaker_id
                or c.code_name == speaker_id):
            return c


def look_up_episode(episode_title: str,
                    state: s.GameState) -> t.Episode:
    for episode in state.scene.episodes:
        if episode.title == episode_title:
            return episode
    return None


def look_up_consequence(ordinal: int, fork: t.Fork) -> t.Consequence:
    for consequence in fork.consequences:
        if consequence.ordinal == ordinal:
            return consequence
    return None
