"""English conversion from number to string"""

__version__ = '1.3.1'

def shortscale(num: int) -> str:
    """
    Return words for integer num
    E.g.
    20_001_001 => twenty million one thousand and one

    The largest scale word is nonillion (10 ** 30)
    Returns "(big number)" when |num| > (10 ** 33 - 1)
    """
    words = ''

    if isMinus := num < 0:
        num = -num

    if num <= 20:
        words += numwords[num]  # 0 - 20
    elif num >= 1000 ** 11:
        words += ' (big number)'
    else:
        exponent = 0
        n = num
        while n:
            next = n // 1000
            words = scale_words(n % 1000, exponent, next > 0) + words
            n = next
            exponent += 1

    if isMinus:
        words = ' minus' + words

    # remove leading space
    return words[1:]


def scale_words(n: int, exponent: int, there_is_more: bool = False):
    """
    Return words for (n, exponent)
    where n = 0 - 999, exponent = 0 - 10
    E.g.
    (102,3) => ' one hundred and two billion'
     (45,2) => ' forty five million'
     (12,0) => ' twelve'
            or ' and twelve' (if there_is_more)
    """
    s_words = ''
    if n == 0:
        return s_words

    if hundreds := n // 100:
        s_words += numwords[hundreds]
        s_words += numwords[100]

    if tens_and_units := n % 100:

        if hundreds or (exponent == 0 and there_is_more):
            s_words += ' and'

        if tens_and_units <= 20:
            s_words += numwords[tens_and_units]

        else:
            if tens := tens_and_units // 10:
                s_words += numwords[tens * 10]

            if units := tens_and_units % 10:
                s_words += numwords[units]

    if exponent:
        s_words += numwords[1000 ** exponent]

    return s_words

numwords = {
    0: ' zero',
    1: ' one',
    2: ' two',
    3: ' three',
    4: ' four',
    5: ' five',
    6: ' six',
    7: ' seven',
    8: ' eight',
    9: ' nine',
    10: ' ten',
    11: ' eleven',
    12: ' twelve',
    13: ' thirteen',
    14: ' fourteen',
    15: ' fifteen',
    16: ' sixteen',
    17: ' seventeen',
    18: ' eighteen',
    19: ' nineteen',
    20: ' twenty',
    30: ' thirty',
    40: ' forty',
    50: ' fifty',
    60: ' sixty',
    70: ' seventy',
    80: ' eighty',
    90: ' ninety',
    100: ' hundred',
    1000: ' thousand',
    1000_000: ' million',  # 1000 ** 2
    1000_000_000: ' billion',  # 1000 ** 3
    1000_000_000_000: ' trillion',  # 1000 ** 4
    1000_000_000_000_000: ' quadrillion',  # 1000 ** 5
    1000_000_000_000_000_000: ' quintillion',  # 1000 ** 6
    1000_000_000_000_000_000_000: ' sextillion',  # 1000 ** 7
    1000_000_000_000_000_000_000_000: ' septillion',  # 1000 ** 8
    1000_000_000_000_000_000_000_000_000: ' octillion',  # 1000 ** 9
    1000_000_000_000_000_000_000_000_000_000: ' nonillion'  # 1000 ** 10
}


def main():
    import sys

    if len(sys.argv) < 2:
        print('usage: shortscale num')
        sys.exit(1)
    try:
        num = int(sys.argv[1], 0)
        print(f'{num:,} => {shortscale(num)}')
        sys.exit(0)
    except Exception as err:
        print(f'Oops! {err}')
        sys.exit(2)


if __name__ == '__main__':
    main()
