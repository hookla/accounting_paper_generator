from langchain.prompts import PromptTemplate
from loguru import logger

from ..utils.file_operations import get_prompt
from ..utils.llm import get_llm


def generate_test_data_and_template(accounting_paper, provider, model):
    logger.info(
        f"Starting generate_test_data_and_template function with {provider} {model}"
    )

    generate_test_data_prompt = get_prompt("generate_test_data_and_template_prompt")

    prompt = PromptTemplate(
        input_variables=["accounting_paper"],
        template=generate_test_data_prompt,
        template_format="jinja2",
    )

    llm = get_llm(provider, model)
    chain = prompt | llm

    result = chain.invoke({"accounting_paper": accounting_paper})
    logger.info("Successfully generated test data and template")
    return result.content
