class IncrementalLineSplitter(object):
    """
    Split bytes into lines separated by b'\\n' without blocking. The rest of
    the bytes after the last line break will be stored and used in the next
    call to :func:`split()`.

    Note: It is safe to handle UTF-8 data with this class. The byte b'\\n' only
    occurs for the line feed character.
    """

    def __init__(self) -> None:
        self.buffer = b''

    def split(self, s: bytes) -> list[bytes]:
        self.buffer += s
        lines = self.buffer.split(b'\n')
        self.buffer = lines[-1]
        return lines[:-1]

    def has_remaining(self) -> bool:
        return self.buffer != b''

    def read_remaining(self) -> bytes:
        buffer = self.buffer
        self.buffer = b''
        return buffer
