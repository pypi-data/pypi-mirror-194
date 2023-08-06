"""Library defining the interface to a Detection Event."""

from rime_sdk.swagger.swagger_client.api_client import ApiClient


class DetectionEvent:
    """An interface to a RI Detection Event.

    The RI Platform surfaces Detection Events to indicate problems with your
    model in-production or during validation.
    """

    def __init__(self, api_client: ApiClient, event_dict: dict) -> None:
        """Initialize a new Detection Event object.

        Args:
            api_client: ApiClient
                The client to query for the up-to-date status of the Event.
            event_dict: dict
                Dictionary with the contents of the event object.
        """
        self._api_client = api_client
        self._event_dict = event_dict

    def to_dict(self) -> dict:
        """Return a dictionary representation of the object."""
        return self._event_dict
