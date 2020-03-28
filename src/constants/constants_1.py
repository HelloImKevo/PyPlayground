def constant(f):
    # noinspection SpellCheckingInspection
    def fset(_self, _value):
        raise TypeError

    # noinspection SpellCheckingInspection
    def fget(_self):
        return f()
    return property(fget, fset)


# noinspection PyPep8Naming, PyMethodParameters
class _Const:
    @constant
    def FOO():
        return 0xBAADFACE

    @constant
    def BAR():
        return 0xDEADBEEF


CONST = _Const()

print(CONST.FOO)
print(CONST.BAR)

# These will raise error!
# CONST.FOO = 1
# CONST.BAR = 5
