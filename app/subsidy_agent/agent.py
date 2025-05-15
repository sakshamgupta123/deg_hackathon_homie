import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict
import json
import logging

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.prompt_book.subsidy_agent_prompt import SUBSIDY_AGENT_SYSTEM_PROMPT
from app.store.context_store import ContextStore
from app.beckn_apis.subsidy_client import SubsidyClient
from app.models import GEMINI_2_5_FLASH

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

client = SubsidyClient()


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
    Search for available subsidies based on the user's context.
    Uses information from previous stages to find applicable subsidies.
    """
    progress_logger.info("[SUBSIDY]:Step 1/3: Search")

    # Get solar and service details to determine subsidy eligibility
    solar_details = context_store.get_solar_details()
    service_details = context_store.get_service_details()

    # Use the information to search for applicable subsidies
    response = client.search()
    context_store.add_transaction_history('search', response)
    _save_context_store('search')
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
    Automatically confirm the subsidy application using information from previous stages.

    Args:
        provider_id (str): ID of the subsidy provider
        item_id (str): ID of the specific subsidy
        fulfillment_id (str): ID of the fulfillment from init response
        customer_name (str): Full name of the person applying for subsidy
        customer_phone (str): Primary contact phone number
        customer_email (str): Customer's email address
    """
    progress_logger.info("[SUBSIDY]:Step 2/3: Confirm")

    if not context_store.get_transaction_history().get('init'):
        raise Exception('Initialization must be done before confirmation')

    # Update subsidy details in context
    context_store.update_subsidy_details(
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
    return response


def _handle_status(order_id: str) -> Dict:
    """
    Check the status of a subsidy application.

    Args:
        order_id (str): The order ID obtained from init response
    """
    progress_logger.info("[SUBSIDY]:Step 3/3: Status Check")

    if not context_store.get_transaction_history().get('confirm'):
        raise Exception('Confirmation must be done before status check')

    # Update subsidy details with order ID
    context_store.update_subsidy_details(order_id=order_id)
    
    response = client.status(order_id=order_id)
    context_store.add_transaction_history('status', response)
    _save_context_store('status')
    return response


context_store = ContextStore()
current_state = None

root_agent = Agent(
    name="subsidy_agent",
    model=GEMINI_2_5_FLASH,
    instruction=SUBSIDY_AGENT_SYSTEM_PROMPT,
    tools=[
        FunctionTool(
            func=_handle_search,
        ),
        FunctionTool(
            func=_handle_confirm,
        ),
        FunctionTool(
            func=_handle_status,
        ),
    ],
)
