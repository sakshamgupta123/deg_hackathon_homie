from typing import Dict, Optional

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.beckn_apis.connection_apis import search, select, init, confirm, status
from app.prompt_book.connection_agent_prompt import CONNECTION_AGENT_SYSTEM_PROMPT
from app.store.context_store import ContextStore
from app.beckn_apis.connection import BAPConnectionClient

connection_client = BAPConnectionClient()

def _handle_search() -> Dict:
    """
    Search for electricity connection providers

    Args:
        location: Location to search in
        connection_type: Type of connection (Residential/Commercial)
    """

    # Update context with search parameters
    context_store.update_connection_details(
    )
    context_store.update_user_details(
    )

    response = connection_client.search_connection()
    context_store.add_transaction_history('search', response)
    return response.json()


def _handle_select(provider_id: str, item_id: str) -> Dict:
    """
    Select a specific provider and plan

    Args:
        provider_id: ID of the selected provider
        item_id: ID of the selected plan
        connection_type: Optional connection type (will use from context if not provided)
    """
    if not context_store.get_transaction_history().get('search'):
        raise Exception('Search must be performed before selection')

    if not provider_id or not item_id:
        raise Exception('Provider ID and Item ID are required')

    # Update context with selection details
    context_store.update_connection_details(
        provider_id=provider_id,
        item_id=item_id
    )

    response = connection_client.select_connection(provider_id=provider_id, item_id=item_id)
    context_store.add_transaction_history('select', response)
    return response


def _handle_init(provider_id: str, item_id: str) -> Dict:
    """
    Initialize connection request with customer details

    """
    if not context_store.get_transaction_history().get('select'):
        raise Exception('Selection must be made before initialization')

    init_data = {
        'provider_id': provider_id,
        'item_id': item_id      
    }

    # Update user details in context
    context_store.update_user_details(**init_data)

    response = connection_client.init_connection(provider_id=provider_id, item_id=item_id) 
    context_store.add_transaction_history('init', response)
    return response


def _handle_confirm(provider_id: str, item_id: str, fulfillment_id: str, customer_name: str, customer_phone: str, customer_email: str) -> Dict:
    """
    Confirm connection request with payment details
    """
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

    response = connection_client.confirm_connection(provider_id=provider_id, item_id=item_id, fulfillment_id=fulfillment_id, customer_name=customer_name, customer_phone=customer_phone, customer_email=customer_email)
    context_store.add_transaction_history('confirm', response)
    return response


def _handle_status(order_id: str) -> Dict:
    """
    Check status of a connection request

    Args:
        transaction_id: Optional transaction ID (will use from context if not provided)
    """
    if not context_store.get_transaction_history().get('confirm'):
        raise Exception('Confirmation must be done before status check')

    context_store.update_connection_details(
        order_id=order_id
    )
    response = connection_client.status_connection(order_id=order_id)
    context_store.add_transaction_history('status', response)
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
