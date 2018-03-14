def bind(parser, f):

    def rtn(input_string):
        res = parser(input_string)
        if not res:
            return []
        else:
            tup = res[0]
            parsed = tup[0]
            rest = tup[1]
            return f(parsed)(rest)
    return rtn


# turns a value into a parser.
def pure(val):

    def rtn(input_string):
        if not input_string:
            return []
        else:
            return [(val, input_string)]

    return rtn


def eat_digit(input_string):
    if not input_string or not input_string[0].isdigit():
        return []
    else:
        return [(int(input_string[0]), input_string[1:])]


def eat_char(input_string):
    if not input_string or not input_string[0].isalpha():
        return []
    else:
        return [(input_string[0], input_string[1:])]




def eat_three_digits(input_string):
    return bind(eat_digit,
                lambda _: bind(eat_digit,
                               lambda _: eat_digit))(input_string)


def eat_digit_char_digit(input_string):
    return bind(eat_digit,
                lambda _: bind(eat_char,
                               lambda _: eat_digit))(input_string)


def get_two_digits(input_string):
    return bind(eat_digit,
                lambda x: bind(eat_digit,
                               lambda y: pure([x, y])))(input_string)


print(get_two_digits('4961a20'))


