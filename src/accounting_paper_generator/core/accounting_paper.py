from langchain.prompts import PromptTemplate
from loguru import logger

from ..utils.file_operations import get_context, get_prompt
from ..utils.llm import get_llm


def generate_accounting_paper(fintech_product_description, events, provider, model):
    logger.info(f"Starting generate_accounting_paper function with {provider} {model}")

    accounting_paper_template = get_context("accounting_paper_template.md")
    generate_accounting_paper_instructions = get_context(
        "generate_accounting_paper_instructions.md"
    )
    generate_accounting_paper_prompt = get_prompt("generate_accounting_paper_prompt")
    chart_of_accounts = get_context("chart_of_accounts.md")

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
