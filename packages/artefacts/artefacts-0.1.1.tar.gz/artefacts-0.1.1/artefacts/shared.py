from typing import Union
from pydantic import BaseModel


class Metadata(BaseModel):
    class Config:
        extra = "allow"

    dbt_schema_version: str
    dbt_version: str
    user_id: Union[str, None]
    project_id: Union[str, None]
    invocation_id: Union[str, None]
    env: dict
    generated_at: str

    @property
    def schema_version(self):
        return self.dbt_schema_version.split("/")[-1].replace(".json", "")
