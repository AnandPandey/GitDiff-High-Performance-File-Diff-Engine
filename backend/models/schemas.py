from pydantic import BaseModel


class DiffRequest(BaseModel):
    old_text: str
    new_text: str


class DiffOperation(BaseModel):
    type: str
    line: str


class DiffResponse(BaseModel):
    operations: list[DiffOperation]
    added: int
    deleted: int
    unchanged: int