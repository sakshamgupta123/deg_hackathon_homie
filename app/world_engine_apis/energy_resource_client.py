from typing import Dict, Any, Optional, Union
import requests


class EnergyResourceClient:
    """
    A client for interacting with energy resource-related APIs.
    Provides methods for CRUD operations on energy resources.
    """

    def __init__(
        self,
    ):
        """
        Initialize the energy resource client.

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

    def create_energy_resource(
        self,
        name: str,
        type: str,
        meter_id: Union[int, str],
    ) -> Dict[str, Any]:
        """
        Create a new energy resource.

        Parameters
        ----------
        name        Name of the energy resource
        type        Type of the energy resource (e.g., "CONSUMER")
        meter_id    ID of the associated meter

        Returns
        -------
        Dict containing the API response
        """
        url = f"{self.base_url}/energy-resources"
        
        payload = {
            "data": {
                "name": name,
                "type": type,
                "meter": meter_id
            }
        }

        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_energy_resource_by_id(
        self,
        resource_id: Union[int, str],
        *,
        populate_meter_parent: bool = True,
        populate_meter_children: bool = True,
        populate_meter_appliances: bool = True
    ) -> Dict[str, Any]:
        """
        Get a specific energy resource by its ID.

        Parameters
        ----------
        resource_id              ID of the energy resource to retrieve
        populate_meter_parent    Whether to populate meter parent data
        populate_meter_children  Whether to populate meter children data
        populate_meter_appliances Whether to populate meter appliances data

        Returns
        -------
        Dict containing the energy resource data
        """
        url = f"{self.base_url}/energy-resources/{resource_id}"
        
        params = {}
        if populate_meter_parent:
            params["populate[0]"] = "meter.parent"
        if populate_meter_children:
            params["populate[1]"] = "meter.children"
        if populate_meter_appliances:
            params["populate[2]"] = "meter.appliances"

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def delete_energy_resource(self, resource_id: Union[int, str]) -> Dict[str, Any]:
        """
        Delete an energy resource by its ID.

        Parameters
        ----------
        resource_id    ID of the energy resource to delete

        Returns
        -------
        Dict containing the API response
        """
        url = f"{self.base_url}/energy-resources/{resource_id}"
        
        resp = self.session.delete(url)
        resp.raise_for_status()
        return resp.json()


# --------------------------------------------------------------------------- #
# Example usage
if __name__ == "__main__":
    # Initialize client
    client = EnergyResourceClient()
    
    # # Create a new energy resource
    # create_response = client.create_energy_resource(
    #     name="Saksham's Home",
    #     type="CONSUMER",
    #     meter_id=1832
    # )
    # print("Created energy resource:", create_response)
    # id = create_response['data']['id']
    # # Get specific energy resource
    # resource = client.get_energy_resource_by_id(id)
    # print("Specific energy resource:", resource)
    
    # Delete energy resource
    delete_response = client.delete_energy_resource(2228)
    print("Delete response:", delete_response) 