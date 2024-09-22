from pydantic import BaseModel, Field


class CityDTO(BaseModel):
    """Schema representing a city response."""

    id: int = Field(..., description="The unique identifier of the city.")
    name: str = Field(..., description="The name of the city.")

    class Config:
        from_attributes = True


class FavoriteCityDTO(BaseModel):
    """Schema representing a favorite city response."""

    id: int = Field(..., description="The unique identifier of the city.")
    name: str = Field(..., description="The name of the city.")
    allow_notifications: bool = Field(
        ...,
        description="Whether notifications are allowed for the city.",
    )

    class Config:
        from_attributes = True
