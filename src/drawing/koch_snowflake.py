"""Draw a Koch Snowflake"""

import turtle


global i
i = 0


# noinspection PyUnresolvedReferences
def koch(a, order):
    global i

    if order > 0:
        for t in [60, -120, 60, 0]:
            print("Forward()...")
            # turtle.forward(a/3)
            i += 1
            if i < 100:
                koch(100, i)
                turtle.left(t)
            else:
                turtle.forward(a/3)
    else:
        turtle.forward(a)


# Test
# koch(100, 0)
turtle.pensize(3)
koch(100, 1)
turtle.done()
