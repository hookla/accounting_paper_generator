import os
import sys
import yaml
import streamlit as st

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from loguru import logger

# Load environment variables
load_dotenv()

# Remove default logger and set up a new one
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("debug.log", rotation="500 MB", level="DEBUG")

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

logger.info(f"Current directory: {current_dir}")
logger.info(f"Project root: {project_root}")


 
def load_file(filename, apply_cache=True):
    logger.debug(f"Attempting to load file: {filename}")
    # First, try to load from the local directory
    local_path = os.path.join(current_dir, filename)
    if os.path.exists(local_path):
        logger.debug(f"File found in local directory: {local_path}")
        with open(local_path, "r") as file:
            content = file.read()
            logger.debug(f"File content (first 100 chars): {content[:100]}...")
            # if apply_cache:
            #     content = f"{{#cached}}\n{content}\n{{/cached}}"
            return content

    logger.error(f"File not found: {filename}")
    raise FileNotFoundError(
        f"Could not find {filename} in either {current_dir} or {os.path.join(project_root, 'docs')}"
    )
    
    
config_path = os.path.join(current_dir, "llm_config.yaml")

try:
    with open(config_path, "r") as config_file:
        llm_config = yaml.safe_load(config_file)
    logger.info(f"Loaded llm_config: {llm_config}")
except Exception as e:
    logger.error(f"Error loading llm_config: {str(e)}")
    llm_config = None
    
def get_llm(provider, model):
    if provider == "anthropic":
        api_key = st.secrets["anthropic"]["api_key"]
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not found in environment variables")
            raise ValueError("ANTHROPIC_API_KEY not set")
        return ChatAnthropic(model=model, anthropic_api_key=api_key, max_tokens=4096)
    elif provider == "openai":
        api_key = st.secrets["openai"]["api_key"]
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY not set")
        return ChatOpenAI(model=model, openai_api_key=api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def generate_accounting_paper(fintech_product_description, events, provider, model):
    logger.info(f"Starting generate_accounting_paper function with {provider} {model}")

    accounting_paper_template = load_file("accounting_paper_template.md")
    generate_accounting_paper_instructions = load_file("generate_accounting_paper_instructions.md")
    generate_accounting_paper_prompt = load_file("generate_accounting_paper_prompt.txt")
    chart_of_accounts = load_file("chart_of_accounts.md")

    prompt = PromptTemplate(
        input_variables=[
            "accounting_paper_template",
            "generate_accounting_paper_instructions",
            "fintech_product_description",
            "events",
            "chart_of_accounts",
        ],
        template=generate_accounting_paper_prompt,
        template_format="jinja2",
    )

    # Create a runnable sequence with the selected LLM
    llm = get_llm(provider, model)
    chain = prompt | llm

    # Invoke the chain
    try:
        result = chain.invoke(
            {
                "accounting_paper_template": accounting_paper_template,
                "generate_accounting_paper_instructions": generate_accounting_paper_instructions,
                "fintech_product_description": fintech_product_description,
                "events": events,
                "chart_of_accounts": chart_of_accounts,
            }
        )

        logger.info("Successfully generated accounting paper")
        return result.content
    except Exception as e:
        logger.error(f"Error invoking LLM chain: {str(e)}")
        raise
    
    
def suggest_events(fintech_product_description, provider, model):
    logger.info(f"Starting suggest_events function with {provider} {model}")
    logger.info(f"Product description: {fintech_product_description}")

    suggest_events_prompt = load_file("suggest_events_prompt.txt")

    try:
        prompt = PromptTemplate(
            input_variables=["fintech_product_description"],
            template=suggest_events_prompt,
            template_format="jinja2",
        )
    except Exception as e:
        logger.error(f"Error creating PromptTemplate: {str(e)}")
        raise

    logger.info(f"Prompt template: {prompt.template}")
    
    try:
        llm = get_llm(provider, model)
    except Exception as e:
        logger.error(f"Error getting LLM: {str(e)}")
        raise

    chain = prompt | llm

    try:
        result = chain.invoke(
            {"fintech_product_description": fintech_product_description}
        )
        logger.info(f"Successfully suggested events")
        return result.content
    except Exception as e:
        logger.error(f"Error suggesting events: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error args: {e.args}")
        raise


def generate_test_data_and_template(accounting_paper, provider, model):
    logger.info(f"Starting generate_test_data_and_template function with {provider} {model}")

    generate_test_data_prompt = load_file("generate_test_data_and_template_prompt.txt")

    prompt = PromptTemplate(
        input_variables=["accounting_paper"],
        template=generate_test_data_prompt,
        template_format="jinja2",
    )

    llm = get_llm(provider, model)
    chain = prompt | llm

    try:
        result = chain.invoke({"accounting_paper": accounting_paper})
        logger.info("Successfully generated test data and template")
        return result.content
    except Exception as e:
        logger.error(f"Error generating test data and template: {str(e)}")
        raise
    


def enhance_product_description(product_description, provider, model):
    logger.info(f"Starting enhance_product_description function with {provider} {model}")
    logger.debug(f"Product description: {product_description[:100]}...")  # Log first 100 chars for debugging

    try:
        enhance_description_prompt = load_file("enhance_product_description_prompt.txt")
        logger.debug(f"Loaded enhance_product_description_prompt.txt")
    except Exception as e:
        logger.error(f"Error loading enhance_product_description_prompt.txt: {str(e)}")
        raise

    try:
        prompt = PromptTemplate(
            input_variables=["product_description"],
            template=enhance_description_prompt,
            template_format="jinja2",
        )
        logger.debug("Created PromptTemplate")
    except Exception as e:
        logger.error(f"Error creating PromptTemplate: {str(e)}")
        raise

    try:
        llm = get_llm(provider, model)
        logger.debug(f"Got LLM: {provider} {model}")
    except Exception as e:
        logger.error(f"Error getting LLM: {str(e)}")
        raise

    chain = prompt | llm

    try:
        result = chain.invoke({"product_description": product_description})
        logger.info("Successfully enhanced product description")
        logger.debug(f"Enhanced description (first 100 chars): {result.content[:100]}...")
        return result.content
    except Exception as e:
        logger.error(f"Error enhancing product description: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error args: {e.args}")
        raise





# Log that the module has been loaded
logger.info("Backend module loaded successfully")