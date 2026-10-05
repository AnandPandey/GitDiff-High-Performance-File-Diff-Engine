from pydantic import BaseModel


class DiffRequest(BaseModel):
    old_text: str
    new_text: str


class CharacterChange(BaseModel):
    type: str
    text: str


class LineOperation(BaseModel):
    type: str
    line: str
    old_line_number: int | None = None
    new_line_number: int | None = None


class CharacterDiff(BaseModel):
    old_line_number: int
    new_line_number: int
    old_line: str
    new_line: str
    changes: list[CharacterChange]


class DiffResponse(BaseModel):
    line_operations: list[LineOperation]
    character_diffs: list[CharacterDiff]

    added: int
    deleted: int
    unchanged: int