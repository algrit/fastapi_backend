from pydantic import BaseModel


class FeatureAdd(BaseModel):
    title: str


class Feature(FeatureAdd):
    id: int


class RoomFeatureAdd(BaseModel):
    room_id: int
    feature_id: int


class RoomFeature(RoomFeatureAdd):
    id: int
