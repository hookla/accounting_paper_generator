from langchain.prompts import PromptTemplate
from loguru import logger

from ..utils.file_operations import get_prompt
from ..utils.llm import get_llm


def enhance_product_description(product_description, provider, model):
    logger.info(
        f"Starting enhance_product_description function with {provider} {model}"
    )
    logger.debug(
        f"Product description: {product_description[:100]}..."
    )  # Log first 100 chars for debugging

    enhance_description_prompt = get_prompt("enhance_product_description_prompt")
    logger.debug("Loaded enhance_product_description_prompt.txt")

    prompt = PromptTemplate(
        input_variables=["product_description"],
        template=enhance_description_prompt,
        template_format="jinja2",
    )
    logger.debug("Created PromptTemplate")

    llm = get_llm(provider, model)
    chain = prompt | llm

    result = chain.invoke({"product_description": product_description})
    logger.info("Successfully enhanced product description")
    logger.debug(f"Enhanced description (first 100 chars): {result.content[:100]}...")
    return result.content
