"""I have no idea how this works!"""


def message(text, plain, encryp):
    dictionary = dict(zip(plain, encryp))
    newmessage = ''
    for char in text:
        try:
            newmessage += dictionary[char]
        except StopIteration:
            newmessage += ' '
        except IOError:
            newmessage += ' '
    print(text + '\nhas been encrypted to:')
    print(newmessage)


message("Hello World", "Hello World", "MD5")
