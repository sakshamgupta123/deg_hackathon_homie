import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict
import json
import logging

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.prompt_book.connection_agent_prompt import CONNECTION_AGENT_SYSTEM_PROMPT
from app.store.context_store import ContextStore
from app.beckn_apis.beckn_client import BAPClient


# Configure simple progress logger
progress_logger = logging.getLogger('progress')
progress_logger.setLevel(logging.INFO)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create file handler for progress logs
progress_handler = logging.FileHandler('logs/progress.log')
progress_handler.setLevel(logging.INFO)

# Create simple formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
progress_handler.setFormatter(formatter)

# Add handler to logger
progress_logger.addHandler(progress_handler)

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


def _handle_search() -> Dict:
    """
    Search for electricity connection providers

    Args:
        location: Location to search in
        connection_type: Type of connection (Residential/Commercial)
    """
    progress_logger.info("Step 1/5: Search")

    # Update context with search parameters
    context_store.update_connection_details()
    context_store.update_user_details()

    response = connection_client.search()
    context_store.add_transaction_history('search', response)
    _save_context_store('search')
    return response


def _handle_select(provider_id: str, item_id: str) -> Dict:
    """
    Select a specific provider and plan

    Args:
        provider_id: ID of the selected provider
        item_id: ID of the selected plan
        connection_type: Optional connection type (will use from context if not provided)
    """
    progress_logger.info("Step 2/5: Select")

    if not context_store.get_transaction_history().get('search'):
        raise Exception('Search must be performed before selection')

    if not provider_id or not item_id:
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
    return response


def _handle_init(provider_id: str, item_id: str) -> Dict:
    """
    Initialize connection request with customer details
    """
    progress_logger.info("Step 3/5: Initialize")

    if not context_store.get_transaction_history().get('select'):
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
    Confirm connection request with payment details
    """
    progress_logger.info("Step 4/5: Confirm")

    if not context_store.get_transaction_history().get('init'):
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
    return response


def _handle_status(order_id: str) -> Dict:
    """
    Check status of a connection request

    Args:
        transaction_id: Optional transaction ID (will use from context if not provided)
    """
    progress_logger.info("Step 5/5: Status Check")

    if not context_store.get_transaction_history().get('confirm'):
        raise Exception('Confirmation must be done before status check')

    context_store.update_connection_details(
        order_id=order_id
    )
    response = connection_client.status(order_id=order_id)
    context_store.add_transaction_history('status', response)
    _save_context_store('status')
    return response


context_store = ContextStore()
current_state = None

root_agent = Agent(
    name="ruchir_connection_agent",
    model="gemini-1.5-flash",
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
