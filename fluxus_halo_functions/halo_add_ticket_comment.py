import requests
from typing import Annotated

from fluxus_sdk.logger import logger
from fluxus_sdk.func import fluxus_func
from fluxus.types import ServiceFieldType


@fluxus_func(
    name="halo_add_ticket_comment",
    label="Add Comment to Halo Ticket",
    description="Add a comment to a ticket in Halo.",
    dir_path="halo/",
)
def halo_add_ticket_comment(
    halo_service: Annotated[
        ServiceFieldType, "The Halo service to use for authentication."
    ],
    halo_token: Annotated[str, "Halo bearer token."],
    ticket_id: Annotated[str, "The ID of the ticket to update."],
    note: Annotated[str, "The note to add to the ticket."],
    status: Annotated[int, "The status to set for the ticket."] = None,
) -> Annotated[dict, "The response from the Halo API."]:
    """Add a note to a ticket in Halo.

    Args:
        halo_service (service.halo): The Halo service to use for authentication.
        halo_token (str): Halo bearer token.
        ticket_id (str): The ID of the ticket to update.
        note (str): The note to add to the ticket.
        status (int, optional): The status to set for the ticket.

    Returns:
        dict: The response from the Halo API.
    """
    url = f"{halo_service.get('host')}/api/actions"
    headers = {
        "Authorization": f"Bearer {halo_token}",
        "Content-Type": "application/json",
    }
    data = [
        {
            "ticket_id": ticket_id,
            "outcome": "Fluxus Update",
            "note": note,
        }
    ]
    if status:
        data[0]["new_status"] = status
    logger.info(f"Adding note to ticket {ticket_id} in Halo...")
    response = requests.post(url, headers=headers, json=data, timeout=10)
    if response.status_code != 201:
        logger.error(f"Failed to add note to ticket in Halo: {response.text}")
        return None
    logger.info("Successfully added note to ticket in Halo.")
    return response.json()
