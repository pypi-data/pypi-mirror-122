import carlo

from random import *
def d(sides, repeat=1):
    """
    Generates a random number by rolling a n-sided dice, e.g. d(6).
    `repeat` allows one to simulate the roll of multiple dices of the same size,
    adding their values.
    """
    return sum(randint(1, sides) for _ in range(repeat))

import sys
import re

if len(sys.argv) > 1:
    # Usage:
    #     $ python -m carlo 'd(6)+d(12)'
    compiled_fns = [compile(arg, f'<argv_function_{i}>', 'eval') for i, arg in enumerate(sys.argv[1:])]
    sequences_or_fns = [lambda compiled_fn=compiled_fn: eval(compiled_fn) for compiled_fn in compiled_fns]
    labels = sys.argv[1:]
else:
    # Usage:
    #     $ echo "1 2 3" | python -m carlo
    sequences_or_fns = [(number for line in sys.stdin for number in map(float, re.findall(r'\d+\.?\d*', line)))]
    labels = ()

print(plot(*sequences_or_fns, labels=labels))