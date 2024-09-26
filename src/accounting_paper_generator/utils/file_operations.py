import base64
import os

from dotenv import load_dotenv
from loguru import logger

from ..utils import current_dir, project_root

# Load environment variables
load_dotenv()


logger.info(f"Current directory: {current_dir}")
logger.info(f"Project root: {project_root}")


def load_file(filename):
    logger.debug(f"Attempting to load file: {filename}")
    # First, try to load from the local directory
    local_path = os.path.join(current_dir, filename)
    if os.path.exists(local_path):
        logger.debug(f"File found in local directory: {local_path}")
        with open(local_path, "r", encoding="utf-8") as file:
            content = file.read()
            logger.debug(f"File content (first 100 chars): {content[:100]}...")
            return content

    logger.error(f"File not found: {filename}")
    raise FileNotFoundError(
        f"Could not find {filename} in either {local_path} or {os.path.join(project_root, 'docs')}"
    )


def download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'


def get_prompt(prompt_name: str):
    prompt_path = os.path.join(
        project_root,
        "src",
        "accounting_paper_generator",
        "prompts",
        f"{prompt_name}.txt",
    )
    return load_file(prompt_path)


def get_context(context_file: str):
    context_path = os.path.join(
        project_root,
        "src",
        "accounting_paper_generator",
        "prompts",
        f"{context_file}",
    )
    return load_file(context_path)
