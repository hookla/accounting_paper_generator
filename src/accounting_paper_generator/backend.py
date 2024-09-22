import os
import sys

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_anthropic import ChatAnthropic
from loguru import logger

# model='claude-3-haiku-20240307'
model = "claude-3-5-sonnet-20240620"

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    logger.error("ANTHROPIC_API_KEY not found in environment variables")
    raise ValueError("ANTHROPIC_API_KEY not set")

llm = ChatAnthropic(model=model, anthropic_api_key=api_key, max_tokens=4096)


# Remove default logger and set up a new one
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("debug.log", rotation="500 MB", level="DEBUG")

# Load environment variables
load_dotenv()

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

logger.info(f"Current directory: {current_dir}")
logger.info(f"Project root: {project_root}")


def load_file(filename):
    logger.debug(f"Attempting to load file: {filename}")
    # First, try to load from the local directory
    local_path = os.path.join(current_dir, filename)
    if os.path.exists(local_path):
        logger.debug(f"File found in local directory: {local_path}")
        with open(local_path, "r") as file:
            content = file.read()
            logger.debug(f"File content (first 100 chars): {content[:100]}...")
            return content

    logger.error(f"File not found: {filename}")
    raise FileNotFoundError(
        f"Could not find {filename} in either {current_dir} or {os.path.join(project_root, 'docs')}"
    )


def generate_accounting_paper(fintech_product_description, events):
    logger.info("Starting generate_accounting_paper function")
    try:
        accounting_paper_template = load_file("accounting_paper_template.md")
        generate_accounting_paper_instructions = load_file(
            "generate_accounting_paper_instructions.md"
        )
        generate_accounting_paper_prompt = load_file(
            "generate_accounting_paper_prompt.txt"
        )
        chart_of_accounts = load_file("chart_of_accounts.md")
    except FileNotFoundError as e:
        logger.error(f"Error loading markdown files: {str(e)}")
        raise

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

    # Create a runnable sequence
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

        # Log the generated prompt
        formatted_prompt = prompt.format(
            accounting_paper_template=accounting_paper_template,
            generate_accounting_paper_instructions=generate_accounting_paper_instructions,
            fintech_product_description=fintech_product_description,
            events=events,
            chart_of_accounts=chart_of_accounts,
        )
        logger.info(f"Generated Prompt: {formatted_prompt}")
        logger.info("Successfully generated accounting paper")
        return result.content
    except Exception as e:
        logger.error(f"Error invoking LLM chain: {str(e)}")
        raise


def suggest_events(fintech_product_description):
    logger.info("Starting suggest_events function")
    logger.info(fintech_product_description)

    try:
        suggest_events_prompt = load_file("suggest_events_prompt.txt")
    except FileNotFoundError as e:
        logger.error(f"Error loading suggest_events_template.txt: {str(e)}")
        raise

    prompt = PromptTemplate(
        input_variables=[fintech_product_description],
        template=suggest_events_prompt,
        template_format="jinja2",
    )
    logger.info(prompt)
    chain = prompt | llm

    try:
        result = chain.invoke(
            {"fintech_product_description": fintech_product_description}
        )
        events = [
            event.strip() for event in result.content.split("\n") if event.strip()
        ]
        formatted_prompt = prompt.format(
            fintech_product_description=fintech_product_description,
        )
        logger.info(f"Generated Prompt: {formatted_prompt}")
        logger.info(f"Successfully suggested {len(events)} events")
        return events
    except Exception as e:
        logger.error(f"Error suggesting events: {str(e)}")
        raise


# Log that the module has been loaded
logger.info("Backend module loaded successfully")
