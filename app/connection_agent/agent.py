import json
import os
import sys
from typing import Dict

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

import app.models
from app.beckn_apis.beckn_client import BAPClient
from app.prompt_book.connection_agent_prompt import CONNECTION_AGENT_SYSTEM_PROMPT
from app.store.context_store import ContextStore
from app.utils.logging_config import get_logger
from app.utils.progress_tracker import update_progress_by_handler

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Get logger for this module
logger = get_logger('Connection')

connection_client = BAPClient(domain="connection")


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
    Search for electricity connection providers.
    No parameters required as search is performed with default configurations.
    
    Returns:
        Dict: Response containing available connection providers and their plans
    """
    logger.info("Step Search - Starting operation")

    # Update progress tracker for this step
    update_progress_by_handler("connection", "search")

    # Update context with search parameters
    context_store.update_connection_details()
    context_store.update_user_details()

    response = connection_client.search()
    context_store.add_transaction_history('search', response)
    _save_context_store('search')

    logger.info("Step Search - Operation completed")
    return response


def _handle_select(provider_id: str, item_id: str) -> Dict:
    """
    Select a specific provider and plan for electricity connection.

    Args:
        provider_id (str): ID of the selected provider
        item_id (str): ID of the selected plan

    Returns:
        Dict: Response containing details of the selected provider and plan

    Raises:
        Exception: If search hasn't been performed or if provider_id/item_id are missing
    """
    logger.info("Step Select - Starting operation for provider %s, item %s", provider_id, item_id)

    # Update progress tracker for this step
    update_progress_by_handler("connection", "select")

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

    response = connection_client.select(
        provider_id=provider_id,
        item_id=item_id
    )
    context_store.add_transaction_history('select', response)
    _save_context_store('select')

    logger.info("Step Select - Operation completed")
    return response


def _handle_init(provider_id: str, item_id: str) -> Dict:
    """
    Initialize connection request with customer details.

    Args:
        provider_id (str): ID of the selected provider
        item_id (str): ID of the selected plan

    Returns:
        Dict: Response containing initialization details including fulfillment_id

    Raises:
        Exception: If selection hasn't been made
    """
    logger.info("Step Init - Starting operation for provider %s, item %s", provider_id, item_id)

    # Update progress tracker for this step
    update_progress_by_handler("connection", "init")

    if not context_store.get_transaction_history().get('select'):
        logger.error("Step Init - Failed: Selection must be made before initialization")
        raise Exception('Selection must be made before initialization')

    init_data = {
        'provider_id': provider_id,
        'item_id': item_id
    }

    # Update user details in context
    context_store.update_user_details(**init_data)

    response = connection_client.init(
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
    Confirm connection request with customer details.

    Args:
        provider_id (str): ID of the selected provider
        item_id (str): ID of the selected plan
        fulfillment_id (str): ID of the fulfillment from init response
        customer_name (str): Full name of the person requesting connection
        customer_phone (str): Primary contact phone number
        customer_email (str): Customer's email address

    Returns:
        Dict: Response containing confirmation details including order_id

    Raises:
        Exception: If initialization hasn't been done
    """
    logger.info("Step Confirm - Starting operation for customer %s", customer_name)

    # Update progress tracker for this step
    update_progress_by_handler("connection", "confirm")

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

    response = connection_client.confirm(
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
    Check status of a connection request.

    Args:
        order_id (str): The order ID obtained from confirm response

    Returns:
        Dict: Response containing current status of the connection request

    Raises:
        Exception: If confirmation hasn't been done
    """
    logger.info("Step Status - Starting check for order %s", order_id)

    # Update progress tracker for this step
    update_progress_by_handler("connection", "status")

    if not context_store.get_transaction_history().get('confirm'):
        logger.error("Step Status - Failed: Confirmation must be done before status check")
        raise Exception('Confirmation must be done before status check')

    context_store.update_connection_details(
        order_id=order_id
    )
    response = connection_client.status(order_id=order_id)
    context_store.add_transaction_history('status', response)
    _save_context_store('status')

    logger.info("Step Status - Operation completed")
    return response


context_store = ContextStore()
current_state = None

root_agent = Agent(
    name="ruchir_connection_agent",
    model=app.models.GEMINI_2_5_FLASH,
    instruction=CONNECTION_AGENT_SYSTEM_PROMPT,
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
