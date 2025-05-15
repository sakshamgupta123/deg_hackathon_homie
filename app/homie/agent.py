import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict
import json
import logging
import shutil

from google.adk.agents import Agent
from app.solar_service_agent.agent import root_agent as solar_service_agent
from app.solar_retail_agent.agent import root_agent as solar_retail_agent
from app.connection_agent.agent import root_agent as connection_agent
from app.subsidy_agent.agent import root_agent as subsidy_agent
from app.prompt_book.homie_agent_prompt import HOMIE_AGENT_SYSTEM_PROMPT
from app.beckn_apis.beckn_client import BAPClient
import app.models 
from app.world_engine_apis.meter_client import MeterClient
from app.world_engine_apis.energy_resource_client import EnergyResourceClient


# if logs and context_store_history directory   exist, delete them
if os.path.exists('logs'):
    shutil.rmtree('logs', ignore_errors=True)
if os.path.exists('context_store_history'):
    shutil.rmtree('context_store_history', ignore_errors=True)  # force delete
    

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

client = BAPClient(domain="retail")              

def _create_meter_energy_resource():
    meter_client = MeterClient()
    meter = meter_client.create_meter(
        code="METER202",
        energy_resource="2105"
    )
    meter_id = meter['data']['id']
    energy_resource_client = EnergyResourceClient()
    energy_resource = energy_resource_client.create_energy_resource(
        name="Saksham's Home2",
        type="CONSUMER",
        meter_id=meter_id
    )
    return meter_id, energy_resource['data']['id']

root_agent = Agent(
    name="homie",
    model=app.models.GEMINI_2_5_FLASH,
    instruction=HOMIE_AGENT_SYSTEM_PROMPT,
    sub_agents=[solar_service_agent, solar_retail_agent, connection_agent, subsidy_agent],
)
    