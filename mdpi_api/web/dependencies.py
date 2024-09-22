from fastapi import Request
from mdpi_api.web.api.errors.auth import NotAuthorizedError


def get_user(request: Request) -> str:
    """
    Get the user from the request.

    :param request: The request object.
    :return: The user object.

    :raises NotAuthorizedError: If the user ID is not found in the session.
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        raise NotAuthorizedError(
            detail="User ID not found in this session",
        )
    return str(user_id)
