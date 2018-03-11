import unittest
import parser


class TestParser(unittest.TestCase):

    def test_parse_choice(self):
        self.assertTrue(parser.has_choice('1. First choice...'))
        self.assertTrue(parser.has_choice('45. Forty-fifth choice...'))
        self.assertFalse(parser.has_choice('just some narration...'))

        rest, choice = parser.parse_choice('1. First choice\nmore...')
        self.assertEqual(str(choice), 'Choice(ordinal=1, text="First choice")')
        self.assertEqual(rest, 'more...')

        rest, choice = parser.parse_choice('22. far-down choice\nmore...')
        self.assertEqual(str(choice), 'Choice(ordinal=22, text="far-down choice")')
        self.assertEqual(rest, 'more...')

    def test_parse_narration(self):
        narr1 = '~ You wake up.\nmore...'
        self.assertTrue(parser.has_narration(narr1))

        rest, parsed_narr1 = parser.parse_narration(narr1)
        self.assertEqual('Narration(text="You wake up.")',
                         str(parsed_narr1))

    def test_parse_action(self):
        # Test properly reading a transition marker.
        narr1 = '~ You wake up. {hear voice}\nmore...'
        self.assertTrue(parser.has_action(narr1))

        rest, parsed_narr1 = parser.parse_action(narr1)
        self.assertEqual('Action(concrete_action=Narration(text="You wake up."), transition_marker="hear voice")',
                         str(parsed_narr1))
        self.assertEqual('more...', rest)

        # Make sure that markers at the end of the line do not interfere
        # with subsequent lines.
        narr2 = '~ You go inside. {go inside}\n\n{go inside}\n~ You are inside.'
        self.assertTrue(parser.has_action(narr2))

        rest, parsed_narr2 = parser.parse_action(narr2)
        self.assertEqual('Action(concrete_action=Narration(text="You go inside."), transition_marker="go inside")',
                         str(parsed_narr2))
        self.assertEqual('\n{go inside}\n~ You are inside.', rest)

    def test_parse_fork(self):
        fork1 = 'P:\n1. first choice\n2. second choice\nmore...'
        self.assertTrue(parser.has_fork(fork1))
        rest, parsed_fork1 = parser.parse_fork(fork1)
        self.assertEqual(str(parsed_fork1),
                         'Fork(choices=[Choice(ordinal=1, text="first choice"), '
                         'Choice(ordinal=2, text="second choice")], consequences=[])')

        fork2 = ('P:\n1. first choice\n2. second choice\n1->\n~ consequence 1\n'
                 '2->\n~ consequence 2\n\nmore...\nEND')
        rest, parsed_fork2 = parser.parse_fork(fork2)
        self.assertEqual(str(parsed_fork2),
                         'Fork(choices=[Choice(ordinal=1, text="first choice"), '
                         'Choice(ordinal=2, text="second choice")], '
                         'consequences=[Consequence(ordinal=1, actions=['
                         'Action(concrete_action=Narration(text="consequence 1"))]), '
                         'Consequence(ordinal=2, actions=['
                         'Action(concrete_action=Narration(text="consequence 2"))])])')
        self.assertEqual(rest, '\nmore...\nEND')

    def test_parse_episodes(self):
        # Make sure episode names are not accidentally parsed as a fork's transition marker.

        contents = ('{start}\n P:\n1. I have to find her!\n1 ->\n~ {go inside}\n\n\n{go inside}\n'
                    '~ You go inside.\nEND')
        rest, episodes = parser.parse_episodes(contents)
        self.assertEquals(2, len(episodes))


if __name__ == '__main__':
    unittest.main()
