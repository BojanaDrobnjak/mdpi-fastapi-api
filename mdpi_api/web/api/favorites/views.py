from fastapi import APIRouter, Depends, Query
from loguru import logger
from mdpi_api.services.city_service import CityService
from mdpi_api.web.api.schemas.city import FavoriteCityDTO
from mdpi_api.web.api.schemas.common import APIResponse, EmptyData
from mdpi_api.web.dependencies import get_user

router = APIRouter()


@router.get("/", response_model=APIResponse[FavoriteCityDTO])
async def get_favorite_cities(
    user_id: str = Depends(get_user),
    city_service: CityService = Depends(),
) -> APIResponse[FavoriteCityDTO]:
    """
    This endpoint is used to get the list of favorite cities for the user.

    :param user_id: The ID of the user.
    :param city_service: The city service.
    :return: APIResponse.
    """
    logger.info(f"Getting list of favorite cities for user {user_id}.")
    favorite_cities = await city_service.get_favorite_cities(user_id)
    return APIResponse.create(
        message="Success",
        data=favorite_cities,
    )


@router.post("/", response_model=APIResponse[EmptyData])
async def add_favorite_city(
    user_id: str = Depends(get_user),
    city_id: int = Query(..., description="The ID of the city to add."),
    city_service: CityService = Depends(),
) -> APIResponse[EmptyData]:
    """
    This endpoint is used to add a city to the user's list of favorite cities.

    :param user_id: The ID of the user.
    :param city_id: The ID of the city to add.
    :param city_service: The city service.
    :return: APIResponse.
    """
    logger.info(f"Adding city {city_id} to favorites for user {user_id}.")
    await city_service.add_favorite_city(user_id, city_id)
    return APIResponse.create(
        message="Success",
        data=EmptyData(),
    )


@router.delete("/", response_model=APIResponse[EmptyData])
async def remove_favorite_city(
    user_id: str = Depends(get_user),
    city_id: int = Query(..., description="The ID of the city to remove."),
    city_service: CityService = Depends(),
) -> APIResponse[EmptyData]:
    """
    This endpoint is used to remove a city from the user's list of favorite cities.

    :param user_id: The ID of the user.
    :param city_id: The ID of the city to remove.
    :param city_service: The city service.
    :return: APIResponse.
    """
    logger.info(f"Removing city {city_id} from favorites for user {user_id}.")
    await city_service.remove_favorite_city(user_id, city_id)
    return APIResponse.create(
        message="Success",
        data=EmptyData(),
    )


@router.put("/notifications_toggle", response_model=APIResponse[EmptyData])
async def toggle_notifications(
    user_id: str = Depends(get_user),
    city_id: int = Query(
        ...,
        description="The ID of the city to toggle notifications for.",
    ),
    city_service: CityService = Depends(),
) -> APIResponse[EmptyData]:
    """
    Toggle notifications for a city in the user's list of favorite cities.

    This endpoint is used to toggle notifications for a city in the user's list of
    favorite cities.

    :param user_id: The ID of the user.
    :param city_id: The ID of the city to toggle notifications for.
    :param city_service: The city service.
    :return: APIResponse.
    """
    logger.info(f"Toggling notifications for city {city_id} for user {user_id}.")
    await city_service.toggle_notifications(user_id, city_id)
    return APIResponse.create(
        message="Success",
        data=EmptyData(),
    )
