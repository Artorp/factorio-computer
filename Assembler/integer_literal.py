# utility function for literals ("-2", "0x42", "-0b42" etc)


def is_number_or_literal(n):
    prefix = str(n).lower()
    if prefix.startswith("0x") or prefix.startswith("-0x"):
        try:
            int(n, base=16)
            return True
        except ValueError:
            return False
    elif prefix.startswith("0b") or prefix.startswith("-0b"):
        try:
            int(n, base=2)
            return True
        except ValueError:
            return False
    else:
        try:
            int(n)
            return True
        except ValueError:
            return False


def to_number_or_literal(n):
    prefix = str(n).lower()
    if prefix.startswith("0x") or prefix.startswith("-0x"):
        return int(n, base=16)
    elif prefix.startswith("0b") or prefix.startswith("-0b"):
        return int(n, base=2)
    else:
        return int(n)


def verify_number_range(n):
    int32_min = -2**31
    int32_max = 2**31 - 1
    return int32_min <= n <= int32_max
