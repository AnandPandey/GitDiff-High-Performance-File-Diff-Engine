from services.myers_diff import myers_diff


def apply_operations(old_lines, operations):
    result = []
    old_index = 0

    for operation_type, line in operations:

        if operation_type == "equal":
            assert old_lines[old_index] == line

            result.append(line)
            old_index += 1

        elif operation_type == "delete":
            assert old_lines[old_index] == line

            old_index += 1

        elif operation_type == "insert":
            result.append(line)

    return result


def test_reconstruction():

    old_lines = [
        "line 1",
        "line 2",
        "line 3",
        "line 4"
    ]

    new_lines = [
        "line 1",
        "new line",
        "line 3",
        "line 4",
        "line 5"
    ]

    operations = myers_diff(
        old_lines,
        new_lines
    )

    reconstructed = apply_operations(
        old_lines,
        operations
    )

    assert reconstructed == new_lines