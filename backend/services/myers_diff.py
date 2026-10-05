def myers_diff(old_lines, new_lines):
    n = len(old_lines)
    m = len(new_lines)

    max_d = n + m
    v = {1: 0}
    trace = []

    for d in range(max_d + 1):
        trace.append(v.copy())

        for k in range(-d, d + 1, 2):

            if k == -d:
                x = v.get(k + 1, 0)

            elif k == d:
                x = v.get(k - 1, 0) + 1

            elif v.get(k - 1, 0) < v.get(k + 1, 0):
                x = v.get(k + 1, 0)

            else:
                x = v.get(k - 1, 0) + 1

            y = x - k

            while (
                x < n
                and y < m
                and old_lines[x] == new_lines[y]
            ):
                x += 1
                y += 1

            v[k] = x

            if x >= n and y >= m:
                return backtrack(
                    trace,
                    old_lines,
                    new_lines,
                    d
                )

    return []


def backtrack(trace, old_lines, new_lines, d):
    operations = []

    x = len(old_lines)
    y = len(new_lines)

    for current_d in range(d, 0, -1):

        v = trace[current_d]
        k = x - y

        if k == -current_d:
            previous_k = k + 1

        elif k == current_d:
            previous_k = k - 1

        elif v.get(k - 1, 0) < v.get(k + 1, 0):
            previous_k = k + 1

        else:
            previous_k = k - 1

        previous_x = v.get(previous_k, 0)
        previous_y = previous_x - previous_k

        while x > previous_x and y > previous_y:
            operations.append(
                ("equal", old_lines[x - 1])
            )

            x -= 1
            y -= 1

        if x == previous_x:
            operations.append(
                ("insert", new_lines[y - 1])
            )
            y -= 1

        else:
            operations.append(
                ("delete", old_lines[x - 1])
            )
            x -= 1

    while x > 0 and y > 0:
        operations.append(
            ("equal", old_lines[x - 1])
        )

        x -= 1
        y -= 1

    while x > 0:
        operations.append(
            ("delete", old_lines[x - 1])
        )

        x -= 1

    while y > 0:
        operations.append(
            ("insert", new_lines[y - 1])
        )

        y -= 1

    operations.reverse()

    return operations


# ---------------------------------------------------------
# Character-level Myers Diff
# ---------------------------------------------------------

def myers_character_diff(old_text, new_text):
    old_chars = list(old_text)
    new_chars = list(new_text)

    n = len(old_chars)
    m = len(new_chars)

    max_d = n + m
    v = {1: 0}
    trace = []

    for d in range(max_d + 1):

        trace.append(v.copy())

        for k in range(-d, d + 1, 2):

            if k == -d:
                x = v.get(k + 1, 0)

            elif k == d:
                x = v.get(k - 1, 0) + 1

            elif v.get(k - 1, 0) < v.get(k + 1, 0):
                x = v.get(k + 1, 0)

            else:
                x = v.get(k - 1, 0) + 1

            y = x - k

            while (
                x < n
                and y < m
                and old_chars[x] == new_chars[y]
            ):
                x += 1
                y += 1

            v[k] = x

            if x >= n and y >= m:
                return backtrack_characters(
                    trace,
                    old_chars,
                    new_chars,
                    d
                )

    return []


def backtrack_characters(
    trace,
    old_chars,
    new_chars,
    d
):
    operations = []

    x = len(old_chars)
    y = len(new_chars)

    for current_d in range(d, 0, -1):

        v = trace[current_d]
        k = x - y

        if k == -current_d:
            previous_k = k + 1

        elif k == current_d:
            previous_k = k - 1

        elif v.get(k - 1, 0) < v.get(k + 1, 0):
            previous_k = k + 1

        else:
            previous_k = k - 1

        previous_x = v.get(previous_k, 0)
        previous_y = previous_x - previous_k

        while x > previous_x and y > previous_y:
            operations.append(
                ("equal", old_chars[x - 1])
            )

            x -= 1
            y -= 1

        if x == previous_x:
            operations.append(
                ("insert", new_chars[y - 1])
            )

            y -= 1

        else:
            operations.append(
                ("delete", old_chars[x - 1])
            )

            x -= 1

    while x > 0 and y > 0:

        operations.append(
            ("equal", old_chars[x - 1])
        )

        x -= 1
        y -= 1

    while x > 0:

        operations.append(
            ("delete", old_chars[x - 1])
        )

        x -= 1

    while y > 0:

        operations.append(
            ("insert", new_chars[y - 1])
        )

        y -= 1

    operations.reverse()

    return operations