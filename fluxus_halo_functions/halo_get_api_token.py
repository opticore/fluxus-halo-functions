import requests
from typing import Annotated

from fluxus_sdk.logger import logger
from fluxus_sdk.func import fluxus_func
from fluxus.types import ServiceFieldType


@fluxus_func(
    name="halo_get_api_token",
    label="Get Halo API Token",
    description="Authenticate with Halo and retrieve a bearer token.",
    dir_path="halo/",
)
def halo_get_api_token(
    halo_service: Annotated[
        ServiceFieldType, "The Halo service to use for authentication."
    ],
) -> Annotated[str, "Halo bearer token."]:
    """Authenticate with Halo and retrieve a bearer token.

    Args:
        halo_service (service.halo): The Halo service to use for authentication.

    Returns:
        halo_token (str): Halo bearer token.
    """
    url = f"{halo_service.get('host')}/auth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(
        url,
        headers=headers,
        data={
            "grant_type": "client_credentials",
            "client_id": halo_service.get("client_id"),
            "client_secret": halo_service.get("client_secret"),
            "scope": halo_service.get("scope"),
        },
        timeout=10,
    )
    if response.status_code != 200:
        logger.error(f"Failed to authenticate with Halo: {response.text}")
        return None
    token_data = response.json()
    halo_token = token_data.get("access_token")
    if not halo_token:
        logger.error("Failed to retrieve Halo token.")
        return None
    logger.info("Successfully authenticated with Halo.")

    return halo_token
