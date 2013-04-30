import hashlib

from md5 import md5


def get_md5_hash(data, block_size_multiplier=1):
    """
    returns an md5 sum. data is a string or file pointer.
    block size is 512 (md5 msg length).
    """
    hash_ = None
    default_block_size = 2**9
    blocksize = block_size_multiplier * default_block_size
    md5 = hashlib.md5()

    if type(data) is file:
        while True:
            read_data = data.read(block_size)
            if not read_data:
                break
            md5.update(read_data)
        data.close()
    else:
        md5.update(str(data))

    hash_ = md5.hexdigest()

    return hash_