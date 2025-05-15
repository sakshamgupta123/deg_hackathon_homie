from typing import Dict, Any, Optional, Union
import requests
import uuid
import time


class SubsidyClient:
    """
    A client for interacting with subsidy-related Beckn Protocol APIs.
    Provides methods for searching, confirming, and checking status of subsidies.
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
    DEFAULT_DOMAIN = "deg:schemes"

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,     
        bap_id: Optional[str] = None,
        bap_uri: Optional[str] = None,
        bpp_id: Optional[str] = None,
        bpp_uri: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the subsidy client with configuration.

        Parameters
        ----------
        base_url    Fully-qualified BAP client URL
        bap_id      Your BAP network identifier
        bap_uri     Your BAP callback URI
        bpp_id      Target BPP network identifier
        bpp_uri     Target BPP URI
        session     Optional pre-configured requests.Session
        """
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
        action         The action being performed (e.g., 'search', 'confirm', 'status')
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
            "domain": self.DEFAULT_DOMAIN,
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
        Send a Beckn *search* request for subsidies.

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/search"
        
        context = self._create_context("search")

        payload = {
            "context": context,
            "message": {
                "intent": {
                    "item": {
                        "descriptor": {
                            "name": "incentive"
                        }
                    }
                }
            }
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
        Send a Beckn *confirm* request for a subsidy.

        Parameters
        ----------
        provider_id      ID of the subsidy provider
        item_id          ID of the subsidy item
        fulfillment_id   ID of the fulfillment
        customer_name    Name of the customer
        customer_phone   Phone number of the customer
        customer_email   Email address of the customer

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/confirm"
        
        context = self._create_context("confirm")

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
            }
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
        Send a Beckn *status* request for a subsidy.

        Parameters
        ----------
        order_id       ID of the subsidy order to check status

        Returns
        -------
        Parsed JSON response (``dict``). Raises ``requests.HTTPError`` on non-2xx.
        """
        url = f"{self.base_url.rstrip('/')}/status"
        
        context = self._create_context("status")

        payload = {
            "context": context,
            "message": {
                "order_id": order_id
            }
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
    
    # Initialize client
    client = SubsidyClient()
    
    # Example search
    search_response = client.search()
    with open("subsidy_search_response.json", "w") as f:
        json.dump(search_response, f, indent=2)
    
    # Example confirm
    confirm_response = client.confirm(
        provider_id="323",
        item_id="459",
        fulfillment_id="615",
        customer_name="Lisa",
        customer_phone="876756454",
        customer_email="LisaS@mailinator.com"
    )
    with open("subsidy_confirm_response.json", "w") as f:
        json.dump(confirm_response, f, indent=2)
    
    # Example status
    status_response = client.status(
        order_id="3778"
    )
    with open("subsidy_status_response.json", "w") as f:
        json.dump(status_response, f, indent=2)
    
    from pprint import pprint
    print("\nSearch Response:")
    pprint(search_response)
    print("\nConfirm Response:")
    pprint(confirm_response)
    print("\nStatus Response:")
    pprint(status_response) 