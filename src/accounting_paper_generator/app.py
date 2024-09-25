import base64
import yaml
import os

import streamlit as st
from backend import generate_accounting_paper, suggest_events, generate_test_data_and_template, llm_config, enhance_product_description

def download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'

st.set_page_config(page_title="Accounting Paper Generator", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Controls")

    # LLM Provider and Model Selection
    if llm_config:
        provider_options = list(llm_config['providers'].keys())
        llm_provider = st.selectbox(
            "Select LLM Provider",
            options=provider_options,
            format_func=lambda x: llm_config['providers'][x]['name'],
            help="Choose the AI provider for generating the paper.",
        )

        model_options = [model['name'] for model in llm_config['providers'][llm_provider]['models']]
        model_display_names = {model['name']: model['display_name'] for model in llm_config['providers'][llm_provider]['models']}
        llm_model = st.selectbox(
            f"Select {llm_config['providers'][llm_provider]['name']} Model",
            options=model_options,
            format_func=lambda x: model_display_names[x],
            help=f"Choose the {llm_config['providers'][llm_provider]['name']} model to use.",
        )
    else:
        st.error("Error loading LLM configuration. Please check the configuration file and logs.")

# Main content
st.title("Accounting Paper Generator")





# Step 1: Product Description
st.header("Step 1: Product Description")
st.markdown("Enter a detailed description of the product or service.")

product_description = st.text_area(
    "Product Description",
    value=st.session_state.get("product_description", ""),
    height=200,
    help="Enter a detailed description of the product or service.",
    key="product_description_input"
)

# Update session state
st.session_state.product_description = product_description

# Button for enhancing product description
if st.button("Enhance Product Description", key="enhance_description_button"):
    if not product_description:
        st.error("Please provide a product description to enhance.")
    else:
        with st.spinner("Enhancing product description..."):
            try:
                enhanced_description = enhance_product_description(
                    product_description, 
                    llm_provider, 
                    llm_model
                )
                st.session_state.product_description = enhanced_description
                st.success("Product description enhanced successfully!")
            except Exception as e:
                st.error(f"An error occurred while enhancing the product description: {str(e)}")

# Display enhanced description if available
if st.session_state.get("product_description"):
    st.markdown("### Enhanced Product Description")
    st.write(st.session_state.product_description)



# Step 2: Events
st.header("Step 2: Events")
st.markdown("List the events related to your product or service.")

if st.button("Suggest Events", key="suggest_events_button"):
    if not product_description:
        st.error("Please provide a product description to suggest events.")
    else:
        with st.spinner("Generating event suggestions..."):
            try:
                suggested_events = suggest_events(product_description, llm_provider, llm_model)
                st.session_state.events = suggested_events
                st.success("Events suggested successfully!")
            except Exception as e:
                st.error(f"An error occurred while suggesting events: {str(e)}")

events = st.text_area(
    "Events (Markdown format)",
    value=st.session_state.get("events", ""),
    height=300,
    key="events_input"
)
st.session_state.events = events

if events:
    st.markdown(events)
else:
    st.info("No events suggested yet. Use the 'Suggest Events' button to generate events.")







# Step 3: Generate or Edit Paper
st.header("Step 3: Generate or Edit Paper")
st.markdown("Generate an accounting paper or edit the existing one.")

if st.button("Generate Paper", key="generate_paper_button"):
    if not product_description or not events:
        st.error("Please provide both a product description and a list of events.")
    elif not llm_config:
        st.error("Error loading LLM configuration. Please check the configuration file and logs.")
    else:
        with st.spinner("Generating accounting paper..."):
            try:
                paper = generate_accounting_paper(product_description, events, llm_provider, llm_model)
                st.session_state.accounting_paper = paper
                st.success("Paper generated successfully!")
            except Exception as e:
                st.error(f"An error occurred while generating the paper: {str(e)}")

accounting_paper = st.text_area(
    "Accounting Paper",
    value=st.session_state.get("accounting_paper", ""),
    height=400,
    key="paper_input"
)
st.session_state.accounting_paper = accounting_paper

if accounting_paper:
    st.markdown("### Current Paper:")
    st.markdown(accounting_paper, unsafe_allow_html=True)
    download_button = download_link(
        accounting_paper, "accounting_paper.txt", "Download Paper"
    )
    st.markdown(download_button, unsafe_allow_html=True)

# Step 4: Generate Test Data and Config Template
st.header("Step 4: Generate Test Data and Config Template")
st.markdown("Generate test data and a config template based on the accounting paper.")

if st.button("Generate Test Data and Config Template", key="generate_test_data_button"):
    if not accounting_paper:
        st.error("Please generate or paste an accounting paper first.")
    elif not llm_config:
        st.error("Error loading LLM configuration. Please check the configuration file and logs.")
    else:
        with st.spinner("Generating test data and config template..."):
            try:
                test_data_and_template = generate_test_data_and_template(accounting_paper, llm_provider, llm_model)
                st.session_state.test_data_and_template = test_data_and_template
                st.success("Test data and config template generated successfully!")
            except Exception as e:
                st.error(f"An error occurred while generating test data and config template: {str(e)}")

if "test_data_and_template" in st.session_state and st.session_state.test_data_and_template:
    st.markdown("### Generated Test Data and Config Template:")
    st.code(st.session_state.test_data_and_template, language="python")
    
    download_button = download_link(
        st.session_state.test_data_and_template, 
        "test_data_and_config_template.py", 
        "Download Test Data and Config Template"
    )
    st.markdown(download_button, unsafe_allow_html=True)

st.markdown("---")
st.markdown("© 2024 Accounting Paper Generator. All rights reserved.")

st.sidebar.markdown("---")
st.sidebar.subheader("Debug Information")
if st.sidebar.checkbox("Show Debug Info"):
    st.sidebar.json(llm_config)
    if st.sidebar.button("Show Logs"):
        with open("debug.log", "r") as log_file:
            st.sidebar.text_area("Log Contents", log_file.read(), height=300)