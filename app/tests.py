from utils import allowed_file


def test_allowed_file():
    assert not allowed_file(None), "None is not an allowed filename."
    assert not allowed_file([]), "Empty list is not an allowed filename."
    assert not allowed_file(42), "Numbers are not an allowed filename."
    assert not allowed_file(""), "Empty string is not an allowed filename."
    assert not allowed_file("/foo/bar"), "Files without extensions are not allowed."
    assert not allowed_file("/foo/bar.txt"), "Files with unsupported extensions are not allowed."
    assert allowed_file("/foo/bar.mp4"), "Files with supported extensions are allowed."
