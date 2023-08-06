def read_file_as_bytes_array(file_path: str, buffsize: int = 8 * 1024) -> bytes:
    # from filecmp import cmpfiles, cmp
    bytes_str = b''
    with open(file_path, 'rb') as fp:
        while True:
            file_buffer = fp.read(buffsize)
            bytes_str += file_buffer
            if not file_buffer:
                break
    return bytes_str
