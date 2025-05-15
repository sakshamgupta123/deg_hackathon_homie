import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict
import json
import shutil

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from app.solar_service_agent.agent import root_agent as solar_service_agent
from app.solar_retail_agent.agent import root_agent as solar_retail_agent
from app.connection_agent.agent import root_agent as connection_agent
from app.subsidy_agent.agent import root_agent as subsidy_agent
from app.prompt_book.homie_agent_prompt import HOMIE_AGENT_SYSTEM_PROMPT
from app.world_engine_apis.meter_client import MeterClient
from app.world_engine_apis.energy_resource_client import EnergyResourceClient
import app.models
from app.utils.logging_config import get_logger

logger = get_logger('homie')

# if logs and context_store_history directory   exist, delete them
if os.path.exists('logs'):
    shutil.rmtree('logs', ignore_errors=True)
if os.path.exists('context_store_history'):
    shutil.rmtree('context_store_history', ignore_errors=True)  # force delete


def _create_meter_energy_resource():
    """
    Creates a new meter and associated energy resource.

    Creates a smart meter with default parameters using the MeterClient, then creates
    a consumer energy resource linked to that meter using the EnergyResourceClient.

    Returns
    -------
    tuple
        A tuple containing:
        - meter_id (int): ID of the created meter
        - energy_resource_id (int): ID of the created energy resource
    """

    meter_client = MeterClient()
    meter = meter_client.create_meter(
        code="METER306",
        energy_resource="2230"
    )
    meter_id = meter['data']['id']
    energy_resource_client = EnergyResourceClient()
    energy_resource = energy_resource_client.create_energy_resource(
        name="Saksham's Home",
        type="CONSUMER",
        meter_id=meter_id
    )
    return meter_id, energy_resource['data']['id']

root_agent = Agent(
    name="homie",
    model=app.models.GEMINI_2_5_FLASH,
    instruction=HOMIE_AGENT_SYSTEM_PROMPT,
    sub_agents=[solar_service_agent, solar_retail_agent, connection_agent, subsidy_agent],
    tools = [
        FunctionTool(
            func=_create_meter_energy_resource,
        ),
    ],
)

logger.info("Agent initialized with %d sub-agents", len(root_agent.sub_agents))
