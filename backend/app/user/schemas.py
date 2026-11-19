from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class UserProfile(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: int
    first_name: str | None
    last_name: str | None
    email: str | None


class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")

    first_name: str | None = Field(default=None, max_length=120)
    last_name: str | None = Field(default=None, max_length=120)
