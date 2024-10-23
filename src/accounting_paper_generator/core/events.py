import json5
import re
from langchain.prompts import PromptTemplate

from loguru import logger

from utils.file_operations import get_prompt
from utils.llm import get_llm


def clean_json_string(response_content):
    # Search for the JSON part within the response
    json_match = re.search(r'```json\s*(\[\s*\{[\s\S]*?\}\s*\])\s*```', response_content)
    
    if json_match:
        # Extract the JSON string between the triple backticks
        json_str = json_match.group(1)
        logger.info("Extracted JSON block from response.")
    else:
        logger.error("No JSON block found in the response.")
        return None

    # Try to parse the extracted JSON string using json5
    try:
        parsed_json = json5.loads(json_str)  # Parse using json5
        return json5.dumps(parsed_json, indent=4)  # Return formatted JSON string
    except ValueError as e:  # Catch parsing errors from json5
        logger.error(f"Failed to parse cleaned JSON string with json5: {e}")
        return None


def suggest_events(fintech_product_description, provider, model, max_retries=1):
    logger.info(f"Starting suggest_events function with {provider} {model}")
    logger.info(f"Product description: {fintech_product_description}")

    base_prompt = get_prompt("suggest_events_prompt")
    retry_prompt_addition = "\n\nPlease ensure that you return valid JSON strictly adhering to the specified format, and do not include any analysis or additional text."

    prompt_text = base_prompt
    # Create the prompt with any additional instructions
    prompt = PromptTemplate(
            input_variables=["fintech_product_description"],
            template=prompt_text,
            template_format="jinja2",
        )

    for attempt in range(1, max_retries + 1):
        logger.info(f"Attempt {attempt} of {max_retries}")

        llm = get_llm(provider, model)
        chain = prompt | llm

        result = chain.invoke({"fintech_product_description": fintech_product_description})
        response_content = result.content

        logger.info(prompt)
        logger.info("LLM response received.")
        logger.info(result)
        # Attempt to extract JSON content
        json_str = clean_json_string(response_content)
        if json_str is None:
            logger.error("Failed to extract JSON from the response.")
            # Adjust the prompt for the next attempt
            prompt_text += retry_prompt_addition
            continue

        # Try parsing with json5
        try:
            events = json5.loads(json_str)
            logger.info("Successfully parsed JSON events using json5.")
            return json5.dumps(events, indent=4)
        except ValueError as e:
            logger.error(f"json5 decoding failed: {e}")
            # Adjust the prompt for the next attempt
            prompt_text += retry_prompt_addition

    logger.error("Exceeded maximum number of retries without successful parsing.")
    return None
