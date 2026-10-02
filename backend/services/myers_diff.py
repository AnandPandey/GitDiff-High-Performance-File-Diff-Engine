def myers_diff(old_lines, new_lines):
    n = len(old_lines)
    m = len(new_lines)

    max_d = n + m

    # V[k] stores the furthest x-coordinate
    # reached on diagonal k.
    v = {1: 0}

    # Store V from every iteration.
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

            # Follow matching lines.
            while (
                x < n
                and y < m
                and old_lines[x] == new_lines[y]
            ):
                x += 1
                y += 1

            v[k] = x

            # Reached the end of both files.
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

        # Move backwards through matching lines.
        while x > previous_x and y > previous_y:
            operations.append(
                ("equal", old_lines[x - 1])
            )

            x -= 1
            y -= 1

        # Insert
        if x == previous_x:
            operations.append(
                ("insert", new_lines[y - 1])
            )
            y -= 1

        # Delete
        else:
            operations.append(
                ("delete", old_lines[x - 1])
            )
            x -= 1

    # Handle remaining equal lines.
    while x > 0 and y > 0:
        operations.append(
            ("equal", old_lines[x - 1])
        )

        x -= 1
        y -= 1

    # If anything remains on either side.
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