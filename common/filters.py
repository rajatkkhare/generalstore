def is_list(value):
    return isinstance(value, list)


def decode_byte(val):
    if val:
        return val.decode('utf-8')
    return ''
