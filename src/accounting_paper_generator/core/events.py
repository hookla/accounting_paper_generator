from langchain.prompts import PromptTemplate
from loguru import logger

from ..utils.file_operations import get_prompt
from ..utils.llm import get_llm


def suggest_events(fintech_product_description, provider, model):
    logger.info(f"Starting suggest_events function with {provider} {model}")
    logger.info(f"Product description: {fintech_product_description}")

    suggest_events_prompt = get_prompt("suggest_events_prompt")

    prompt = PromptTemplate(
        input_variables=["fintech_product_description"],
        template=suggest_events_prompt,
        template_format="jinja2",
    )

    logger.info(f"Prompt template: {prompt.template}")

    llm = get_llm(provider, model)

    chain = prompt | llm

    result = chain.invoke({"fintech_product_description": fintech_product_description})
    logger.info("Successfully suggested events")
    return result.content
