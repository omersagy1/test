import gametree as t
import gamestate as s
import printer as p


def play(game_tree: t.GameTree) -> None:
    p.print_line('PLAYING GAME...')

    state = s.GameState(game_tree.scene)
    first_episode = game_tree.episodes[0]
    play_episode(first_episode, state)


def play_episode(episode: t.Episode, state: s.GameState) -> None:
    for action in episode.actions:
        play_action(action, state)


def play_action(action: t.Action, state: s.GameState) -> None:
    if isinstance(action, t.Narration):
        play_narration(action, state)
    elif isinstance(action, t.Dialogue):
        play_dialogue(action, state)
    elif isinstance(action, t.Alias):
        play_alias(action, state)
    elif isinstance(action, t.Unalias):
        play_unalias(action, state)
    elif isinstance(action, t.Fork):
        play_fork(action, state)


def play_narration(narration: t.Narration, state: s.GameState) -> None:




