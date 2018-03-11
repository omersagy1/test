import gametree


class Character:

    def __init__(self, name: str, code_name: str=None) -> None:
        # Canonical name for the character. Permanent.
        self.real_name = name

        # Optional internal abbreviation used to refer to the
        # character in the script. Permanent.
        if code_name:
            self.code_name = code_name
        else:
            self.code_name = self.real_name[0]

        # Optional alternate display name. Can be altered.
        # If set, overrides the real name as a display name.
        #
        # Characters cannot be internally referenced by their
        # alias, it is only a display name.
        self.alias = None

    def __repr__(self) -> str:
        return 'Character(real_name="%s", code_name="%s", alias="%s"' % (
            self.real_name, self.code_name, self.alias)

    def __str__(self) -> str:
        if self.alias:
            return self.alias
        else:
            return self.real_name

    def assign_alias(self, alias: str) -> None:
        self.alias = alias

    def unalias(self) -> None:
        self.alias = None


class GameState:

    def __init__(self, scene=None):
        self.characters = []
        self.milestones = []
        self.scene = scene
        if scene:
            self.initialize_from_scene()

    def initialize_from_scene(self):
        self.clear_characters()
        for c in self.scene.characters:
            self.characters.append(
                Character(c.name, c.code_name))

    def clear_characters(self):
        self.characters = []

    def clear_milestones(self):
        self.milestones = []
