import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict
import json
import logging

from google.adk.agents import Agent
from app.solar_service_agent.agent import root_agent as solar_service_agent
from app.solar_retail_agent.agent import root_agent as solar_retail_agent
from app.connection_agent.agent import root_agent as connection_agent
from app.prompt_book.homie_agent_prompt import HOMIE_AGENT_SYSTEM_PROMPT
from app.beckn_apis.beckn_client import BAPClient
import app.models 

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



root_agent = Agent(
    name="homie",
    model=app.models.GEMINI_1_5_FLASH,
    instruction=HOMIE_AGENT_SYSTEM_PROMPT,
    sub_agents=[solar_service_agent, solar_retail_agent, connection_agent]
)
