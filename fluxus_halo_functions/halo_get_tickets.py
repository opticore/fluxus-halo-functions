import requests
from typing import Annotated

from fluxus_sdk.logger import logger
from fluxus_sdk.func import fluxus_func
from fluxus_sdk.types import ServiceFieldType


@fluxus_func(
    name="halo_get_tickets",
    label="Get Halo API Token",
    description="Authenticate with Halo and retrieve a bearer token.",
    dir_path="halo/",
)
def halo_get_tickets(
    halo_service: Annotated[
        ServiceFieldType, "The Halo service to use for authentication."
    ],
    halo_token: Annotated[str, "Halo bearer token."],
) -> Annotated[str, "Halo bearer token."]:
    """Get tickets from Halo.

    Args:
        halo_service (service.halo): The Halo service to use for authentication.
        halo_token (str): Halo bearer token.

    Returns:
        dict: The response from the Halo API.
    """
    url = f"{halo_service.get('host')}/api/Tickets"
    headers = {
        "Authorization": f"Bearer {halo_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        logger.error(f"Failed to get tickets from Halo: {response.text}")
        return None
    logger.info("Successfully retrieved tickets from Halo.")
    return response.json()
