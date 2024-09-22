# Accounting Paper Generator

## Overview

The Accounting Paper Generator is a web application that helps users create detailed accounting papers for fintech products. It uses AI to generate accounting treatments and explanations based on user input.

## Features

- Generate accounting papers from product descriptions and financial events
- Suggest relevant financial events based on product descriptions
- Interactive web interface using Streamlit
- AI-powered content generation using Anthropic's Claude model

## Project Structure

- `src/accounting_paper_generator/app.py`: Main Streamlit application
- `src/accounting_paper_generator/backend.py`: Core logic for generating accounting papers and suggesting events
- `accounting_paper_template.md`: Template for the accounting paper structure
- `.env`: Environment variables (make sure to create this file)

## Setup

1. Clone the repository
2. Install Poetry if you haven't already:
   ```
   pip install poetry
   ```
3. Install project dependencies:
   ```
   poetry install
   ```
4. Create a `.env` file in the project root and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Activate the Poetry environment:
   ```
   poetry shell
   ```
2. Run the Streamlit app:
   ```
   streamlit run src/accounting_paper_generator/app.py
   ```
3. Open the provided URL in your browser
4. Enter your product description and list of events
5. Click "Generate Paper" to create your accounting paper

## Dependencies

Main dependencies include:
- Streamlit
- Langchain
- Anthropic API (Claude model)
- python-dotenv

For a full list of dependencies, refer to the `pyproject.toml` file.

## Notes

- Ensure all required markdown files are in the correct directory relative to the Python scripts
- The application uses Claude 3.5 Sonnet model by default

## License

This project is licensed under the MIT License with Commons Clause. See the [LICENSE](LICENSE) file for details.