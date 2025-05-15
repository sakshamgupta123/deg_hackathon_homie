import os

from typing import Dict
import json
import sys

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.prompt_book.solar_retail_agent_prompt import SOLAR_RETAIL_AGENT_SYSTEM_PROMPT
from app.store.context_store import ContextStore
from app.beckn_apis.beckn_client import BAPClient
import app.models
from app.utils.logging_config import get_logger
from app.utils.progress_tracker import update_progress_by_handler

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Get logger for this module
logger = get_logger('SolarRetail')

client = BAPClient(domain="retail")


def _save_context_store(step: str):
    """
    Save the current state of context store to a file

    Args:
        step: The step name (search/select/init/confirm/status)
    """
    os.makedirs('context_store_history', exist_ok=True)
    filename = f'context_store_history/context_store_{step}.json'

    # Get the current state
    state = {
        'connection_details': context_store.get_connection_details(),
        'user_details': context_store.get_user_details(),
        'transaction_history': context_store.get_transaction_history()
    }

    # Save to file
    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)

    logger.info("Step - Context store saved")


def _handle_search() -> Dict:
    """
    Search for available solar products and services.
    No parameters required as search is performed with default configurations.
    """
    logger.info("Step Search - Starting operation")

    # Update progress tracker for this step
    update_progress_by_handler("solar_retail", "search")

    # Update context with search parameters
    context_store.update_connection_details()
    context_store.update_user_details()

    response = client.search()
    context_store.add_transaction_history('search', response)
    _save_context_store('search')

    logger.info("Step Search - Operation completed")
    return response


def _handle_select(provider_id: str, item_id: str) -> Dict:
    """
    Select a specific solar product or service from a provider.

    Args:
        provider_id (str): ID of the selected provider
        item_id (str): ID of the selected solar product or service
    """
    logger.info("Step Select - Starting operation for provider %s, item %s", provider_id, item_id)

    # Update progress tracker for this step
    update_progress_by_handler("solar_retail", "select")

    if not context_store.get_transaction_history().get('search'):
        logger.error("Step Select - Failed: Search must be performed before selection")
        raise Exception('Search must be performed before selection')

    if not provider_id or not item_id:
        logger.error("Step Select - Failed: Provider ID and Item ID are required")
        raise Exception('Provider ID and Item ID are required')

    # Update context with selection details
    context_store.update_connection_details(
        provider_id=provider_id,
        item_id=item_id
    )

    response = client.select(
        provider_id=provider_id,
        item_id=item_id
    )
    context_store.add_transaction_history('select', response)
    _save_context_store('select')

    logger.info("Step Select - Operation completed")
    return response


def _handle_init(provider_id: str, item_id: str) -> Dict:
    """
    Initialize the solar product/service purchase process.

    Args:
        provider_id (str): ID of the selected provider
        item_id (str): ID of the selected solar product or service
    """
    logger.info("Step Init - Starting operation for provider %s, item %s", provider_id, item_id)

    # Update progress tracker for this step
    update_progress_by_handler("solar_retail", "init")

    if not context_store.get_transaction_history().get('select'):
        logger.error("Step Init - Failed: Selection must be made before initialization")
        raise Exception('Selection must be made before initialization')

    init_data = {
        'provider_id': provider_id,
        'item_id': item_id
    }

    # Update user details in context
    context_store.update_user_details(**init_data)

    response = client.init(
        provider_id=provider_id,
        item_id=item_id
    )
    context_store.add_transaction_history('init', response)
    _save_context_store('init')

    logger.info("Step Init - Operation completed")
    return response


def _handle_confirm(
    provider_id: str,
    item_id: str,
    fulfillment_id: str,
    customer_name: str,
    customer_phone: str,
    customer_email: str
) -> Dict:
    """
    Confirm the solar product/service purchase with customer details.

    Args:
        provider_id (str): ID of the selected provider
        item_id (str): ID of the selected solar product or service
        fulfillment_id (str): ID of the fulfillment from init response
        customer_name (str): Full name of the person making the purchase
        customer_phone (str): Primary contact phone number
        customer_email (str): Customer's email address
    """
    logger.info("Step Confirm - Starting operation for customer %s", customer_name)

    # Update progress tracker for this step
    update_progress_by_handler("solar_retail", "confirm")

    if not context_store.get_transaction_history().get('init'):
        logger.error("Step Confirm - Failed: Initialization must be done before confirmation")
        raise Exception('Initialization must be done before confirmation')

    context_store.update_connection_details(
        provider_id=provider_id,
        item_id=item_id,
        fulfillment_id=fulfillment_id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email
    )

    response = client.confirm(
        provider_id=provider_id,
        item_id=item_id,
        fulfillment_id=fulfillment_id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email
    )
    context_store.add_transaction_history('confirm', response)
    _save_context_store('confirm')

    logger.info("Step Confirm - Operation completed")
    return response


def _handle_status(order_id: str) -> Dict:
    """
    Check the status of a solar product/service purchase.

    Args:
        order_id (str): The order ID obtained from init response
    """
    logger.info("Step Status - Starting check for order %s", order_id)

    # Update progress tracker for this step
    update_progress_by_handler("solar_retail", "status")

    if not context_store.get_transaction_history().get('confirm'):
        logger.error("Step Status - Failed: Confirmation must be done before status check")
        raise Exception('Confirmation must be done before status check')

    context_store.update_connection_details(
        order_id=order_id
    )
    response = client.status(order_id=order_id)
    context_store.add_transaction_history('status', response)
    _save_context_store('status')

    logger.info("Step Status - Operation completed")
    return response


context_store = ContextStore()
current_state = None

root_agent = Agent(
    name="solar_retail_agent",
    model=app.models.GEMINI_2_5_FLASH,
    instruction=SOLAR_RETAIL_AGENT_SYSTEM_PROMPT,
    tools=[
        FunctionTool(
            func=_handle_search,
        ),
        FunctionTool(
            func=_handle_select,
        ),
        FunctionTool(
            func=_handle_init,
        ),
        FunctionTool(
            func=_handle_confirm,
        ),
        FunctionTool(
            func=_handle_status,
        ),
    ],
)

logger.info("Agent initialized with %d tools", len(root_agent.tools))
