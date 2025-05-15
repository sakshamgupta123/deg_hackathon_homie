import os
import time
import uuid
from typing import Dict, Any, Optional, Literal

import requests


class BAPClient:
    """
    A unified client for interacting with Beckn Protocol APIs.
    This class can handle different domains (retail, connection, solar, etc.) and can be extended for future domains.
    """

    # Default configuration values
    DEFAULT_BAP_ID = "bap-ps-network-deg-team13.becknprotocol.io"
    DEFAULT_BAP_URI = "https://bap-ps-network-deg-team13.becknprotocol.io/"
    DEFAULT_BPP_ID = "bpp-ps-network-deg-team13.becknprotocol.io"
    DEFAULT_BPP_URI = "https://bpp-ps-network-deg-team13.becknprotocol.io/"
    DEFAULT_BASE_URL = "https://bap-ps-client-deg-team13.becknprotocol.io/"
    DEFAULT_COUNTRY_CODE = "USA"
    DEFAULT_CITY_CODE = "NANP:628"
    DEFAULT_TIMEOUT = 100
    DEFAULT_VERSION = "1.1.0"

    # Domain configurations
    DOMAINS = {
        "retail": {
            "domain": "deg:retail",
            "search_intent": "solar"
        },
        "connection": {
            "domain": "deg:service",
            "search_intent": "Connection"
        },
        "solar": {
            "domain": "deg:service",
            "search_intent": "resi"
        }
    }

    def __init__(
        self,
        *,
        domain: Literal["retail", "connection", "solar"],
        base_url: Optional[str] = None,
        bap_id: Optional[str] = None,
        bap_uri: Optional[str] = None,
        bpp_id: Optional[str] = None,
        bpp_uri: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the BAP client with configuration.

        Parameters
        ----------
        domain      The domain to use (retail, connection, or solar)
        base_url    Fully-qualified BAP client URL
        bap_id      Your BAP network identifier
        bap_uri     Your BAP callback URI
        bpp_id      Target BPP network identifier
        bpp_uri     Target BPP URI
        session     Optional pre-configured requests.Session
        """
        if domain not in self.DOMAINS:
            raise ValueError(f"Domain must be one of {list(self.DOMAINS.keys())}")

        self.domain = domain
        self.domain_config = self.DOMAINS[domain]
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.bap_id = bap_id or self.DEFAULT_BAP_ID
        self.bap_uri = bap_uri or self.DEFAULT_BAP_URI
        self.bpp_id = bpp_id or self.DEFAULT_BPP_ID
        self.bpp_uri = bpp_uri or self.DEFAULT_BPP_URI
        self.session = session or requests.Session()

    def _create_context(
        self,
        action: str,
        *,
        country_code: Optional[str] = None,
        city_code: Optional[str] = None,
        extra_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a context dictionary for Beckn API requests.

        Parameters
        ----------
        action         The action being performed (e.g., 'search', 'select')
        country_code   ISO-3166 alpha-3 country code
        city_code      City code
        extra_context  Additional context fields to merge

        Returns
        -------
        Dict containing the context
        """
        now = int(time.time())
        location = {
            "country": {"code": country_code or self.DEFAULT_COUNTRY_CODE}
        }
        if city_code or self.DEFAULT_CITY_CODE:
            location["city"] = {"code": city_code or self.DEFAULT_CITY_CODE}

        context: Dict[str, Any] = {
            "domain": self.domain_config["domain"],
            "action": action,
            "location": location,
            "version": self.DEFAULT_VERSION,
            "bap_id": self.bap_id,
            "bap_uri": self.bap_uri,
            "bpp_id": self.bpp_id,
            "bpp_uri": self.bpp_uri,
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": str(now),
        }

        if extra_context:
            context.update(extra_context)

        return context

    def search(self) -> Dict[str, Any]:
        """
        Send a Beckn *search* request for the configured domain.
        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/search"

        context = self._create_context(
            "search",
        )

        payload = {
            "context": context,
            "message": {
                "intent": {
                    "item": {"descriptor": {"name": self.domain_config["search_intent"]}}
                }
            },
        }

        headers = {"Content-Type": "application/json"}
        resp = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()

    def select(
        self,
        provider_id: str,
        item_id: str,
    ) -> Dict[str, Any]:
        """
        Send a Beckn *select* request.

        Parameters
        ----------
        provider_id    ID of the service provider
        item_id        ID of the item to select

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/select"

        context = self._create_context(
            "select"
        )

        payload = {
            "context": context,
            "message": {
                "order": {
                    "provider": {
                        "id": provider_id
                    },
                    "items": [
                        {
                            "id": item_id
                        }
                    ]
                }
            },
        }

        headers = {"Content-Type": "application/json"}
        resp = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()

    def init(
        self,
        provider_id: str,
        item_id: str,
    ) -> Dict[str, Any]:
        """
        Send a Beckn *init* request.

        Parameters
        ----------
        provider_id    ID of the service provider
        item_id        ID of the item to initialize

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/init"

        context = self._create_context(
            "init"
        )

        payload = {
            "context": context,
            "message": {
                "order": {
                    "provider": {
                        "id": provider_id
                    },
                    "items": [
                        {
                            "id": item_id
                        }
                    ]
                }
            },
        }

        headers = {"Content-Type": "application/json"}
        resp = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()

    def confirm(
        self,
        provider_id: str,
        item_id: str,
        fulfillment_id: str,
        customer_name: str,
        customer_phone: str,
        customer_email: str,
    ) -> Dict[str, Any]:
        """
        Send a Beckn *confirm* request.

        Parameters
        ----------
        provider_id      ID of the service provider
        item_id          ID of the item to confirm
        fulfillment_id   ID of the fulfillment
        customer_name    Name of the customer
        customer_phone   Phone number of the customer
        customer_email   Email address of the customer

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/confirm"

        context = self._create_context(
            "confirm"
        )

        payload = {
            "context": context,
            "message": {
                "order": {
                    "provider": {
                        "id": provider_id
                    },
                    "items": [
                        {
                            "id": item_id
                        }
                    ],
                    "fulfillments": [
                        {
                            "id": fulfillment_id,
                            "customer": {
                                "person": {
                                    "name": customer_name
                                },
                                "contact": {
                                    "phone": customer_phone,
                                    "email": customer_email
                                }
                            }
                        }
                    ]
                }
            },
        }

        headers = {"Content-Type": "application/json"}
        resp = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()

    def status(
        self,
        order_id: str,
    ) -> Dict[str, Any]:
        """
        Send a Beckn *status* request.

        Parameters
        ----------
        order_id       ID of the order to check status

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/status"

        context = self._create_context(
            "status"
        )

        payload = {
            "context": context,
            "message": {
                "order_id": order_id
            },
        }

        headers = {"Content-Type": "application/json"}
        resp = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        return resp.json()


# --------------------------------------------------------------------------- #
# Example usage
if __name__ == "__main__":
    import json
    from datetime import datetime

    # Create clients for different domains
    # client = BAPClient(domain="retail")
    client = BAPClient(domain="retail")

    timestamp = 1
    # Example search
    search_response = client.search()
    with open(f"retail_search_response_{timestamp}.json", "w") as f:
        json.dump(search_response, f, indent=2)

    # Extract provider and item IDs from search response
    provider_id = search_response["responses"][0]["message"]["catalog"]["providers"][0]["id"]
    item_id = search_response["responses"][0]["message"]["catalog"]["providers"][0]["items"][0]["id"]

    # Example select
    select_response = client.select(
        provider_id=provider_id,
        item_id=item_id,
    )
    with open(f"retail_select_response_{timestamp}.json", "w") as f:
        json.dump(select_response, f, indent=2)

    # Example init
    init_response = client.init(
        provider_id=provider_id,
        item_id=item_id,
    )
    with open(f"retail_init_response_{timestamp}.json", "w") as f:
        json.dump(init_response, f, indent=2)

    # Extract order ID from init response
    order_id = init_response["responses"][0]["message"]["order"]["provider"]["id"]

    # Example confirm
    confirm_response = client.confirm(
        provider_id=provider_id,
        item_id=item_id,
        fulfillment_id=init_response["responses"][0]["message"]["order"]["fulfillments"][0]["id"],
        customer_name="Lisa",
        customer_phone="876756454",
        customer_email="LisaS@mailinator.com",
    )
    with open(f"retail_confirm_response_{timestamp}.json", "w") as f:
        json.dump(confirm_response, f, indent=2)
    order_id = confirm_response["responses"][0]["message"]["order"]["id"]
    # Example status
    status_response  = {}
    while not status_response.get("responses") and timestamp <10:
        timestamp = timestamp + 1
        status_response = client.status(
            order_id=order_id,
        )
        with open(f"retail_status_response_{timestamp}.json", "w") as f:
            json.dump(status_response, f, indent=2)

    from pprint import pprint
    print("\nSearch Response:")
    pprint(search_response)
    print("\nSelect Response:")
    pprint(select_response)
    print("\nInit Response:")
    pprint(init_response)
    print("\nConfirm Response:")
    pprint(confirm_response)
    print("\nStatus Response:")
    pprint(status_response)