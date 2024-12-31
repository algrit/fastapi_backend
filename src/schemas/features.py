from pydantic import BaseModel


class FeaturesAdd(BaseModel):
    title: str


class Features(FeaturesAdd):
    id: int