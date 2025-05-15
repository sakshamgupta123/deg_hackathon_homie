from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
import requests
import json


class MeterClient:
    """
    A client for interacting with meter-related APIs.
    Provides methods for CRUD operations on meters and accessing meter data.
    """

    def __init__(
        self,
    ):
        """
        Initialize the meter client.

        Parameters
        ----------
        base_url    Base URL for the world engine API
        session     Optional pre-configured requests.Session
        """
        self.base_url = "http://world-engine-team13.becknprotocol.io/meter-data-simulator"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def create_meter(
        self,
        code: str,
        energy_resource: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new meter.

        Parameters
        ----------
        code            Unique identifier for the meter
        energy_resource Optional energy resource identifier

        Returns
        -------
        Dict containing the API response
        """
        url = f"{self.base_url}/meters"
        
        payload = {
            "data": {
                "code": code,
                "parent": None,
                "energyResource": energy_resource,
                "consumptionLoadFactor": 1.0,
                "productionLoadFactor": 0.0,
                "type": "SMART",
                "city": "San Francisco",
                "state": "California",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "pincode": "94103"
            }
        }

        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_all_meters(
        self,
        *,
        sort_by: str = "children.code:desc"
    ) -> Dict[str, Any]:
        """
        Get all meters by automatically handling pagination.
        If there are more than 10000 meters, it will fetch all pages and combine the results.

        Parameters
        ----------
        sort_by     Field to sort by (default: children.code:desc)

        Returns
        -------
        Dict containing the API response with all meters combined
        """
        url = f"{self.base_url}/meters"
        page_size = 10000
        page = 1
        all_data = []
        total_pages = 1

        while page <= total_pages:
            params = {
                "pagination[page]": page,
                "pagination[pageSize]": page_size,
                "populate[0]": "parent",
                "populate[1]": "energyResource",
                "populate[2]": "children",
                "populate[3]": "appliances",
                "sort[0]": sort_by
            }

            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            # Get total pages from the first response
            if page == 1:
                total_pages = (data.get('data', {}).get('pagination', {}).get('pageCount', 1))

            # Append the data from current page
            all_data.extend(data['data']['results'])
            # if 'data' in data:
            #     all_data.extend(data['data'])
            page += 1

        # Construct the final response in the same format as the API
        return all_data
    
    def delete_meter(self, meter_id: Union[int, str]) -> Dict[str, Any]:
        """
        Delete a meter by its ID.

        Parameters
        ----------
        meter_id    ID of the meter to delete

        Returns
        -------
        Dict containing the API response
        """
        url = f"{self.base_url}/meters/{meter_id}"
        
        resp = self.session.delete(url)
        resp.raise_for_status()
        return resp.json()

    def get_meter_by_id(
        self,
        meter_id: Union[int, str],
        *,
        populate_parent: bool = True,
        populate_children: bool = True
    ) -> Dict[str, Any]:
        """
        Get a specific meter by its ID.

        Parameters
        ----------
        meter_id          ID of the meter to retrieve
        populate_parent   Whether to populate parent data
        populate_children Whether to populate children data

        Returns
        -------
        Dict containing the meter data
        """
        url = f"{self.base_url}/meters/{meter_id}"
        
        params = {}
        if populate_parent:
            params["populate[0]"] = "parent"
        if populate_children:
            params["populate[1]"] = "children"

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_meter_historical_data(self, dataset_id: Union[int, str]) -> Dict[str, Any]:
        """
        Get historical data for a meter dataset.

        Parameters
        ----------
        dataset_id    ID of the meter dataset

        Returns
        -------
        Dict containing the historical data
        """
        url = f"{self.base_url}/meter-datasets/{dataset_id}"
        
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()


# --------------------------------------------------------------------------- #
# Example usage
if __name__ == "__main__":
    # Initialize client
    client = MeterClient()
    
    # Create a new meter
    create_response = client.create_meter(
        code="METER201",
        energy_resource="2105"
    )
    print("Created meter:", create_response)
    
    # Get all meters in one request (handles pagination automatically)
    all_meters = client.get_all_meters()
    # dump to file
    with open("all_meters.json", "w") as f:
        json.dump(all_meters, f)
    print(f"Total meters retrieved: {len(all_meters)}")
    
    # Get specific meter
    meter = client.get_meter_by_id(1833)
    print("Specific meter:", meter)
    
    # Get historical data
    historical_data = client.get_meter_historical_data(1682)
    print("Historical data:", historical_data)
    # dump to file
    with open("historical_data.json", "w") as f:
        json.dump(historical_data, f)
    # Delete meter
    delete_response = client.delete_meter(1833)
    print("Delete response:", delete_response) 