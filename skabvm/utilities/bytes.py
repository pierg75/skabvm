
def convert_bytes(size):
    """Return the amount of bytes from a humanized string (e.g. 10GB)

    Assumes `from __future__ import division`.

    >>> convert_bytes('10GB')
    '10737418240'
    >>> convert_bytes('1KB')
    1024


    """
    abbrevs = {
        'PB': '1 << 50',
        'TB': '1 << 40',
        'GB': '1 << 30',
        'MB': '1 << 20',
        'KB': '1 << 10'
    }

    for suffix, factor in abbrevs.iteritems():
        if suffix in size:
            size = size.rstrip(suffix)
            byte_size = int(size) * eval(factor)
            break
    return byte_size
