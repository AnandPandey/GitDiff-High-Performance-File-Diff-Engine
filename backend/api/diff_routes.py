from fastapi import APIRouter

from models.schemas import (
    DiffRequest,
    DiffResponse,
    LineOperation,
    CharacterChange,
    CharacterDiff
)

from services.myers_diff import (
    myers_diff,
    myers_character_diff
)


router = APIRouter()


def build_character_changes(old_line, new_line):

    operations = myers_character_diff(
        old_line,
        new_line
    )

    changes = []

    current_type = None
    current_text = ""

    for operation_type, character in operations:

        if operation_type != current_type:

            if current_type is not None:
                changes.append(
                    CharacterChange(
                        type=current_type,
                        text=current_text
                    )
                )

            current_type = operation_type
            current_text = character

        else:
            current_text += character

    if current_type is not None:

        changes.append(
            CharacterChange(
                type=current_type,
                text=current_text
            )
        )

    return changes


def build_line_operations(line_operations):

    result = []

    old_line_number = 1
    new_line_number = 1

    for operation_type, line in line_operations:

        if operation_type == "equal":

            result.append(
                LineOperation(
                    type="equal",
                    line=line,
                    old_line_number=old_line_number,
                    new_line_number=new_line_number
                )
            )

            old_line_number += 1
            new_line_number += 1

        elif operation_type == "delete":

            result.append(
                LineOperation(
                    type="delete",
                    line=line,
                    old_line_number=old_line_number,
                    new_line_number=None
                )
            )

            old_line_number += 1

        elif operation_type == "insert":

            result.append(
                LineOperation(
                    type="insert",
                    line=line,
                    old_line_number=None,
                    new_line_number=new_line_number
                )
            )

            new_line_number += 1

    return result


def build_character_diffs(line_operations):

    character_diffs = []

    old_line_number = 1
    new_line_number = 1

    index = 0

    while index < len(line_operations):

        operation_type, line = line_operations[index]

        if operation_type == "equal":

            old_line_number += 1
            new_line_number += 1
            index += 1

            continue

        # Collect consecutive deleted lines
        deleted_lines = []

        while (
            index < len(line_operations)
            and line_operations[index][0] == "delete"
        ):
            deleted_lines.append(
                line_operations[index][1]
            )

            index += 1

        # Collect consecutive inserted lines
        inserted_lines = []

        while (
            index < len(line_operations)
            and line_operations[index][0] == "insert"
        ):
            inserted_lines.append(
                line_operations[index][1]
            )

            index += 1

        pair_count = min(
            len(deleted_lines),
            len(inserted_lines)
        )

        for pair_index in range(pair_count):

            old_line = deleted_lines[pair_index]
            new_line = inserted_lines[pair_index]

            changes = build_character_changes(
                old_line,
                new_line
            )

            character_diffs.append(
                CharacterDiff(
                    old_line_number=old_line_number,
                    new_line_number=new_line_number,
                    old_line=old_line,
                    new_line=new_line,
                    changes=changes
                )
            )

            old_line_number += 1
            new_line_number += 1

        old_line_number += (
            len(deleted_lines) - pair_count
        )

        new_line_number += (
            len(inserted_lines) - pair_count
        )

    return character_diffs


@router.post("/diff", response_model=DiffResponse)
def calculate_diff(request: DiffRequest):

    old_lines = request.old_text.splitlines()
    new_lines = request.new_text.splitlines()

    line_operations = myers_diff(
        old_lines,
        new_lines
    )

    line_results = build_line_operations(
        line_operations
    )

    character_results = build_character_diffs(
        line_operations
    )

    added = 0
    deleted = 0
    unchanged = 0

    for operation_type, line in line_operations:

        if operation_type == "insert":
            added += 1

        elif operation_type == "delete":
            deleted += 1

        elif operation_type == "equal":
            unchanged += 1

    return DiffResponse(
        line_operations=line_results,
        character_diffs=character_results,
        added=added,
        deleted=deleted,
        unchanged=unchanged
    )