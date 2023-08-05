from .incremental_line_split import IncrementalLineSplitter


def test_split():
    splitter = IncrementalLineSplitter()
    assert splitter.split(b'a b\nc') == [b'a b']
    assert splitter.split(b'd\ne\n') == [b'cd', b'e']


def test_remaining():
    splitter = IncrementalLineSplitter()
    assert splitter.split(b'a b\nc') == [b'a b']
    assert splitter.has_remaining()
    assert splitter.read_remaining() == b'c'
