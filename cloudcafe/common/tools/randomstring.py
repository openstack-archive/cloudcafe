from uuid import uuid4


def get_random_string(prefix=None, suffix=None, size=8):
    """
        Return exactly size bytes worth of base_text as a string
        surrounded by any defined pre or suf-fixes
    """
    body = ''
    base_text = str(uuid4()).replace('-','0')

    if size <= 0:
        body = '{0}{1}'.format(prefix, suffix)
    else:
        extra = size % len(base_text)
    
        if extra == 0:
            body = base_text * size
    
        if extra == size:
            body = base_text[:size]
    
        if (extra > 0) and (extra < size):
            temp_len = (size / len(base_text))
            base_one = base_text * temp_len
            base_two = base_text[:extra]
            body = '{0}{1}'.format(base_one, base_two)

        if prefix is not None:
            body = '{0}{1}'.format(str(prefix), str(body))

        if suffix is not None:
            body = '{0}{1}'.format(str(body), str(suffix))

    return body
