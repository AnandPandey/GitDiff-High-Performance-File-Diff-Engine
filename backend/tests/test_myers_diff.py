from services.myers_diff import myers_diff
from services.myers_diff import myers_character_diff


def test_character_diff_equal():
    result = myers_character_diff(
        "hello",
        "hello"
    )

    assert "".join(
        character
        for operation, character in result
        if operation == "equal"
    ) == "hello"


def test_character_diff_insert():
    result = myers_character_diff(
        "hello",
        "hello!"
    )

    assert ("insert", "!") in result


def test_character_diff_delete():
    result = myers_character_diff(
        "hello!",
        "hello"
    )

    assert ("delete", "!") in result


def test_character_diff_replacement():
    result = myers_character_diff(
        "hello world",
        "hello GitDiff"
    )

    types = [
        operation
        for operation, character in result
    ]

    assert "delete" in types
    assert "insert" in types


def test_identical_files():
    old = ["hello", "world"]
    new = ["hello", "world"]

    result = myers_diff(old, new)

    assert result == [
        ("equal", "hello"),
        ("equal", "world")
    ]


def test_insertion():
    old = ["hello"]
    new = ["hello", "world"]

    result = myers_diff(old, new)

    assert result == [
        ("equal", "hello"),
        ("insert", "world")
    ]


def test_deletion():
    old = ["hello", "world"]
    new = ["hello"]

    result = myers_diff(old, new)

    assert result == [
        ("equal", "hello"),
        ("delete", "world")
    ]


def test_replacement():
    old = ["hello"]
    new = ["hi"]

    result = myers_diff(old, new)

    assert result == [
        ("delete", "hello"),
        ("insert", "hi")
    ]

def test_multiple_changes():
    old = [
        "line 1",
        "line 2",
        "line 3",
        "line 4"
    ]

    new = [
        "line 1",
        "new line",
        "line 3",
        "line 4",
        "line 5"
    ]

    result = myers_diff(old, new)

    assert result == [
        ("equal", "line 1"),
        ("delete", "line 2"),
        ("insert", "new line"),
        ("equal", "line 3"),
        ("equal", "line 4"),
        ("insert", "line 5")
    ]

def test_empty_old_file():
    old = []
    new = ["A", "B", "C"]

    result = myers_diff(old, new)

    assert result == [
        ("insert", "A"),
        ("insert", "B"),
        ("insert", "C")
    ]


def test_empty_new_file():
    old = ["A", "B", "C"]
    new = []

    result = myers_diff(old, new)

    assert result == [
        ("delete", "A"),
        ("delete", "B"),
        ("delete", "C")
    ]


def test_completely_different_files():
    old = ["A", "B"]
    new = ["X", "Y"]

    result = myers_diff(old, new)

    assert result == [
        ("delete", "A"),
        ("delete", "B"),
        ("insert", "X"),
        ("insert", "Y")
    ]