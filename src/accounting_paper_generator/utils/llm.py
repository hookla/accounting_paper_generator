import os

import streamlit as st
import yaml
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from loguru import logger

from ..utils import project_root

# Load environment variables
load_dotenv()


logger.info(f"Project root: {project_root}")

config_path = os.path.join(
    project_root, "src", "accounting_paper_generator", "config", "llm_config.yaml"
)


def load_llm_config():
    """Load the LLM configuration from a YAML file."""
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            logger.info(f"Loaded llm_config: {config}")
            return config
    except Exception as e:
        logger.error(f"Error loading llm_config: {str(e)}")
        return None


# Load config once and use it to populate picklists
LLM_CONFIG = load_llm_config()


def get_llm(provider, model):
    if provider == "anthropic":
        api_key = st.secrets["anthropic"]["api_key"]
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not found in environment variables")
            raise ValueError("ANTHROPIC_API_KEY not set")
        return ChatAnthropic(model=model, anthropic_api_key=api_key, max_tokens=4096)

    if provider == "openai":
        api_key = st.secrets["openai"]["api_key"]
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY not set")
        return ChatOpenAI(model=model, openai_api_key=api_key)

    raise ValueError(f"Unsupported provider: {provider}")
