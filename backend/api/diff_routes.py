from fastapi import APIRouter

from models.schemas import (
    DiffRequest,
    DiffResponse,
    DiffOperation
)

from services.myers_diff import myers_diff


router = APIRouter()


@router.post("/diff", response_model=DiffResponse)
def calculate_diff(request: DiffRequest):

    old_lines = request.old_text.splitlines()
    new_lines = request.new_text.splitlines()

    operations = myers_diff(
        old_lines,
        new_lines
    )

    result = []

    added = 0
    deleted = 0
    unchanged = 0

    for operation_type, line in operations:

        result.append(
            DiffOperation(
                type=operation_type,
                line=line
            )
        )

        if operation_type == "insert":
            added += 1

        elif operation_type == "delete":
            deleted += 1

        elif operation_type == "equal":
            unchanged += 1

    return DiffResponse(
        operations=result,
        added=added,
        deleted=deleted,
        unchanged=unchanged
    )