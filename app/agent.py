from typing import Dict, Optional

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.beckn_apis.connection_apis import search, select, init, confirm, status
from app.prompt_book.connection_agent_prompt import CONNECTION_AGENT_SYSTEM_PROMPT
from app.store.context_store import ContextStore


def _handle_search(location: str, connection_type: str) -> Dict:
    """
    Search for electricity connection providers

    Args:
        location: Location to search in
        connection_type: Type of connection (Residential/Commercial)
    """
    if not location or not connection_type:
        raise Exception('Location and connection type are required for search')

    # Update context with search parameters
    context_store.update_connection_details(
        connection_type=connection_type
    )
    context_store.update_user_details(
        location=location
    )

    response = search(location=location, connection_type=connection_type)
    context_store.add_transaction_history('search', response)
    return response.json()


def _handle_select(provider_id: str, item_id: str, connection_type: Optional[str] = None) -> Dict:
    """
    Select a specific provider and plan

    Args:
        provider_id: ID of the selected provider
        item_id: ID of the selected plan
        connection_type: Optional connection type (will use from context if not provided)
    """
    if not context_store.get_transaction_history().get('search'):
        raise Exception('Search must be performed before selection')

    conn_type = connection_type or context_store.get_value('connection_details', 'connection_type')
    if not provider_id or not item_id or not conn_type:
        raise Exception('Provider ID, Item ID, and connection type are required')

    # Update context with selection details
    context_store.update_connection_details(
        provider_id=provider_id,
        item_id=item_id
    )

    response = select(provider_id=provider_id, item_id=item_id, connection_type=conn_type)
    context_store.add_transaction_history('select', response)
    return response


def _handle_init(name: str, phone: str, email: str, address: str) -> Dict:
    """
    Initialize connection request with customer details

    Args:
        name: Customer name
        phone: Phone number
        email: Email address
        address: Installation address
    """
    if not context_store.get_transaction_history().get('select'):
        raise Exception('Selection must be made before initialization')

    init_data = {
        'name': name,
        'phone': phone,
        'email': email,
        'address': address
    }

    # Update user details in context
    context_store.update_user_details(**init_data)

    selection_details = context_store.get_transaction_history()['select'].get('selection_details', {})
    selection_id = selection_details.get('selection_id')

    if not selection_id:
        raise Exception('Selection ID not found')

    context_store.update_connection_details(selection_id=selection_id)

    response = init(selection_id=selection_id, customer_details=init_data)
    context_store.add_transaction_history('init', response)
    return response


def _handle_confirm(payment_method: str, payment_id: str) -> Dict:
    """
    Confirm connection request with payment details

    Args:
        payment_method: Method of payment (UPI/Card/etc)
        payment_id: Payment identifier
    """
    if not context_store.get_transaction_history().get('init'):
        raise Exception('Initialization must be done before confirmation')

    payment_details = {
        'payment_method': payment_method,
        'payment_id': payment_id
    }

    transaction_id = context_store.get_transaction_history()['init'].get('transaction_id')
    if not transaction_id:
        raise Exception('Transaction ID not found')

    context_store.update_connection_details(transaction_id=transaction_id)

    response = confirm(transaction_id=transaction_id, payment_details=payment_details)
    context_store.add_transaction_history('confirm', response)
    return response


def _handle_status(transaction_id: Optional[str] = None) -> Dict:
    """
    Check status of a connection request

    Args:
        transaction_id: Optional transaction ID (will use from context if not provided)
    """
    tx_id = (
        transaction_id or
        context_store.get_value('connection_details', 'transaction_id')
    )

    if not tx_id:
        raise Exception('Transaction ID is required')

    response = status(transaction_id=tx_id)
    context_store.add_transaction_history('status', response)
    return response


def reset():
    """Reset the agent state and context store"""
    global current_state
    current_state = None
    context_store.reset()


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
