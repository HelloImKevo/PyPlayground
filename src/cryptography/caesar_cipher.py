# Caesar Cipher

MAX_KEY_SIZE = 26


def get_mode():
    while True:
        print('Do you wish to encrypt or decrypt a message?')
        mode = input().lower()

        if mode in 'encrypt e decrypt d'.split():
            return mode
        else:
            print('Enter either "encrypt" or "e" or "decrypt" or "d".')


def get_message():
    print('Enter your message:')
    return input()


def get_key():
    while True:
        print('Enter the key number (1-%s)' % MAX_KEY_SIZE)
        key = int(input())
        if 1 <= key <= MAX_KEY_SIZE:
            return key
        # if key >= 1 and key <= MAX_KEY_SIZE:
        #     return key


def get_translated_message(mode, message, key):
    if mode[0] == 'd':
        key = -key
    translated = ''

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26

            translated += chr(num)
        else:
            translated += symbol
    return translated


def main():
    mode = get_mode()
    message = get_message()
    key = get_key()

    print('Your translated text is:')
    print(get_translated_message(mode, message, key))


main()
