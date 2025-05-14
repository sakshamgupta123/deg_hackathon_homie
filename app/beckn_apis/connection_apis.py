import json
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv('environment.env')

# Configuration
OUTPUT_DIR = "test_bap_bpp_responses"
HEADERS = {
    'Content-Type': 'application/json'
}


def setup_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def save_to_json(data, prefix):
    """Save data to a JSON file"""
    filename = f"{OUTPUT_DIR}/{prefix}.json"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Data successfully saved to {filename}")


def search(location: str = "Defaultville", connection_type: str = "Residential"):
    """Mock search function"""
    print(f"API_MOCK: search called with location='{location}', connection_type='{connection_type}'")
    return {
        "status": "success",
        "providers": [
            {
                "id": "prov_123",
                "name": "Mock Electric Co",
                "items": [
                    {"id": "item_resi_001", "name": "Standard Residential Connection", "type": "Residential"},
                    {"id": "item_comm_001", "name": "Basic Commercial Connection", "type": "Commercial"}
                ]
            }
        ]
    }


def select(provider_id: str, item_id: str, connection_type: str = "Residential"):
    """Mock select function"""
    print(f"API_MOCK: select called with provider_id='{provider_id}', item_id='{item_id}', connection_type='{connection_type}'")
    return {
        "status": "success",
        "selection_details": {
            "provider_id": provider_id,
            "item_id": item_id,
            "connection_type": connection_type,
            "estimated_cost": 150.00
        }
    }


def init(selection_id: str = "sel_123", customer_details: dict = None):
    """Mock init function"""
    print(f"API_MOCK: init called with selection_id='{selection_id}', customer_details='{customer_details}'")
    return {
        "status": "success",
        "transaction_id": "txn_" + str(uuid.uuid4()),
        "selection_id": selection_id
    }


def confirm(transaction_id: str = "txn_123", payment_details: dict = None):
    """Mock confirm function"""
    print(f"API_MOCK: confirm called with transaction_id='{transaction_id}', payment_details='{payment_details}'")
    return {
        "status": "success",
        "confirmation_id": "conf_" + str(uuid.uuid4()),
        "transaction_id": transaction_id
    }


def status(transaction_id: str = "txn_123"):
    """Mock status function"""
    print(f"API_MOCK: status called with transaction_id='{transaction_id}'")
    return {
        "status": "success",
        "transaction_status": "processing",
        "transaction_id": transaction_id,
        "estimated_completion": "2024-02-01"
    }
