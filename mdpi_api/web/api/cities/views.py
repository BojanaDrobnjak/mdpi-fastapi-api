from fastapi import APIRouter, Depends, Query
from loguru import logger
from mdpi_api.services.city_service import CityService
from mdpi_api.services.weather_service import WeatherService
from mdpi_api.web.api.schemas.city import CityDTO
from mdpi_api.web.api.schemas.common import APIResponse, PaginationParams
from mdpi_api.web.api.schemas.weather import WeatherDTO

router = APIRouter()


@router.get("/", response_model=APIResponse[CityDTO])
async def get_cities(
    pagination: PaginationParams = Depends(),
    city_service: CityService = Depends(),
) -> APIResponse[CityDTO]:
    """
    This endpoint is used to get the list of cities.

    :param pagination: The pagination parameters.
    :param city_service: The city service.
    :return: APIResponse.
    """
    logger.info("Getting list of cities.")
    cities = await city_service.get_all_cities(pagination)
    return APIResponse.create(
        message="Success",
        data=cities,
    )


@router.get("/weather", response_model=APIResponse[WeatherDTO])
async def get_weather(
    city_id: int = Query(
        ...,
        description="The ID of the city to get weather for.",
    ),
    weather_service: WeatherService = Depends(),
) -> APIResponse[WeatherDTO]:
    """
    Get the weather for a city in the user's list of favorite cities.

    This endpoint is used to get the weather for a city in the user's list of
    favorite cities.

    :param city_id: The ID of the city to get weather for.
    :param weather_service: The weather service.
    :return: APIResponse.
    """
    logger.info(f"Getting weather for city {city_id}.")
    weather = await weather_service.get_weather_by_city_id(city_id)
    return APIResponse.create(
        message="Success",
        data=weather,
    )
