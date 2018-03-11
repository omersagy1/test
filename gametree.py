from typing import List

# TODO: The whole game tree is one scene. Allow for multiple
# scenes.


class Character:

    def __init__(self, name: str, code_name: str=None) -> None:
        self.name = name
        self.code_name = code_name

    def __repr__(self) -> str:
        desc = 'Character(name="%s"' % self.name
        if self.code_name:
            desc += ', code_name="%s"' % self.code_name
        desc += ')'
        return desc


class Action:

    def __init__(self, concrete_action, transition_marker=None) -> str:
        self.concrete_action = concrete_action
        self.transition_marker = transition_marker

    def __repr__(self) -> str:
        s = 'Action(concrete_action=%s' % self.concrete_action
        if self.transition_marker:
            s += ', transition_marker="%s"' % self.transition_marker
        s += ')'
        return s


class Dialogue:

    def __init__(self, speaker_id: str, text: str) -> None:
        super().__init__()
        self.speaker_id = speaker_id
        self.text = text

    def __repr__(self) -> str:
        return 'Dialogue(speaker_id="%s", text="%s")' % (
            self.speaker_id, self.text)


class Narration:

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def __repr__(self) -> str:
        return 'Narration(text="%s")' % self.text


class Alias:

    def __init__(self, character_name: str, alias: str):
        super().__init__()
        self.character_name = character_name
        self.alias = alias

    def __repr__(self) -> str:
        return 'Alias(character_name="%s", alias="%s")' % (
            self.character_name, self.alias)


class Unalias:

    def __init__(self, character_name: str):
        super().__init__()
        self.character_name = character_name

    def __repr__(self) -> str:
        return 'Unalias(character_name="%s")' % (
            self.character_name)


class Choice:

    def __init__(self, ordinal: int, text: str) -> None:
        self.ordinal = ordinal
        self.text = text

    def __repr__(self) -> str:
        return 'Choice(ordinal=%s, text="%s")' % (
            self.ordinal, self.text)


class Consequence:

    def __init__(self, ordinal: int, actions: List[Action]):
        self.ordinal = ordinal
        self.actions = actions

    def __repr__(self) -> str:
        return 'Consequence(ordinal=%s, actions=%s)' % (
            self.ordinal, self.actions)


class Fork:

    def __init__(self, choices: List[Choice], consequences: List[Consequence]):
        self.choices = choices
        self.consequences = consequences

    def __repr__(self) -> str:
        return 'Fork(choices=%s, consequences=%s)' % (
            self.choices, self.consequences)


class Episode:

    def __init__(self, title: str, actions):
        self.title = title
        self.actions = actions

    def __repr__(self):
        return 'Episode(title="%s",actions=%s)' % (
            self.title, self.actions)


class Scene:

    def __init__(self, episodes: List[Episode], characters: List[Character]=[]):
        self.episodes = episodes
        self.characters = characters

    def __repr__(self):
        return 'Scene(characters=%s, episodes=%s)' % (
            self.characters,
            self.episodes)


class GameTree:

    def __init__(self, scene: Scene):
        self.scene = scene

    def __repr__(self):
        return repr(self.scene)
