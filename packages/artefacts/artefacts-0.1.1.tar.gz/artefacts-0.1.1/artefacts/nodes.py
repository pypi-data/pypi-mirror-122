from pydantic import BaseModel
from artefacts.mixins import ContextReader


class BaseNode(ContextReader, BaseModel):

    unique_id: str

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    def __hash__(self):
        return hash(self.unique_id)

    def __str__(self):
        return self.unique_id

    def __repr__(self):
        return f"<Node {self.unique_id}>"


class BaseNodeReference(ContextReader, str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("NodeReferences must be strings")
        else:
            return cls(v)

    def __str__(self):
        return self.unique_id

    def __repr__(self):
        return f"<Node {self.unique_id}>"
