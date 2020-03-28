import codecs
import logging
import re


def sanitize(value: str) -> str:
    """
    :param value: String to have all non-Alphanumeric entities removed from.
    :return: Sanitized string containing only Alphanumeric characters.
    """
    return re.sub('[^A-Za-z0-9]+', '', value)


def from_hex(value: str) -> str:
    """
    :param value: Hex string to be converted.
    :return: Human-readable decoded result.
    """
    try:
        return codecs.decode(value, "hex").decode('ascii')
    except (TypeError, UnicodeDecodeError):
        logging.debug("Decode Error - Input is not ASCII")

    try:
        return codecs.decode(value, "hex").decode('utf-8')
    except UnicodeDecodeError:
        logging.debug("Decode Error - Input is not UTF-8")

    try:
        return codecs.decode(value, "hex").decode(encoding='iso-8859-1')
    except UnicodeDecodeError:
        logging.debug("Decode Error - Input is not ISO-8859-1")


def to_hex(value: str) -> str:
    """
    :param value: String to be converted to hex.
    :return: Hexadecimal result.
    """
    return value.encode('iso-8859-1').hex()


# TODO: Convert this to a TKinter UI App for easy Copy/Pasting
logging.getLogger().setLevel(level=logging.DEBUG)

print(from_hex("61286464696458"))

print(from_hex("613c646469252664585e"))

# hex_string = "0x616263"[2:]
user_hex_input = "0x41f4ad265fd1054176ab89bd7dd6c4b43f"[2:]
print(from_hex(sanitize(user_hex_input)))

user_hex_input = "0x41f4adfb5f-d105-4176-ab89-bd7dd6c4b43f"[2:]
print(from_hex(sanitize(user_hex_input)))

user_string_input = "Greetings and salutations!"
hex_string = to_hex(user_string_input)
print(hex_string)
print(from_hex(sanitize(hex_string)))
