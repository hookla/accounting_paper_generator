import base64
import yaml
import os

import streamlit as st
from backend import generate_accounting_paper, suggest_events, generate_test_data_and_template, llm_config

def download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'

st.set_page_config(page_title="Accounting Paper Generator", layout="wide")


def set_sample_description():
    st.session_state.product_description = "simple peer to peer transfer between 2 customers in the same branch"

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
    height=200,
    help="Enter a detailed description of the product or service.",
)

# Step 2: Events st.header("Step 2: Events")
st.header("Step 2: Events")
st.markdown("List the events related to your product or service.")

if "events" not in st.session_state:
    st.session_state.events = ""

if st.button("Suggest Events", key="suggest_events_button"):
    if not product_description:
        st.error("Please provide a product description to suggest events.")
    else:
        with st.spinner("Generating event suggestions..."):
            try:
                suggested_events = suggest_events(product_description, llm_provider, llm_model)
                st.session_state.events = suggested_events  # Assuming this is already formatted as markdown
                st.success("Events suggested successfully!")
            except Exception as e:
                st.error(f"An error occurred while suggesting events: {str(e)}")

# Always show events in an editable text area
events = st.text_area(
    "Events (Markdown format)",
    value=st.session_state.events,
    height=300,
    key="events_input"
)

# Update session state with any changes made in the text area
st.session_state.events = events

# Display current events (if any) using st.markdown
if st.session_state.events:
    st.markdown("### Current Events:")
    st.markdown(st.session_state.events)
else:
    st.info("No events suggested yet. Use the 'Suggest Events' button to generate events.")
         
                
# Step 3: Generate or Edit Paper
st.header("Step 3: Generate or Edit Paper")
st.markdown("Generate an accounting paper or paste/edit an existing one.")

if "accounting_paper" not in st.session_state:
    st.session_state.accounting_paper = ""

paper_edit_mode = st.toggle("Edit Paper", value=False, key="paper_edit_toggle")

if paper_edit_mode:
    st.session_state.accounting_paper = st.text_area(
        "Accounting Paper", 
        value=st.session_state.accounting_paper, 
        height=400,
        key="paper_input"
    )
else:
    if st.session_state.accounting_paper:
        st.markdown(st.session_state.accounting_paper, unsafe_allow_html=True)
    
    if st.button("Generate Paper", key="generate_paper_button"):
        if not product_description or not st.session_state.events:
            st.error("Please provide both a product description and a list of events.")
        elif not llm_config:
            st.error("Error loading LLM configuration. Please check the configuration file and logs.")
        else:
            with st.spinner("Generating accounting paper..."):
                try:
                    paper = generate_accounting_paper(product_description, st.session_state.events, llm_provider, llm_model)
                    st.session_state.accounting_paper = paper
                    st.markdown("### Generated Paper:")
                    st.markdown(paper, unsafe_allow_html=True)
                    download_button = download_link(
                        paper, "accounting_paper.txt", "Download Paper"
                    )
                    st.markdown(download_button, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occurred while generating the paper: {str(e)}")

# Step 4: Generate Test Data and Config Template
st.header("Step 4: Generate Test Data and Config Template")
st.markdown("Click the button below to generate test data and a config template based on the accounting paper.")

if st.button("Generate Test Data and Config Template", key="generate_test_data_button"):
    if not st.session_state.accounting_paper:
        st.error("Please generate or paste an accounting paper first.")
    elif not llm_config:
        st.error("Error loading LLM configuration. Please check the configuration file and logs.")
    else:
        with st.spinner("Generating test data and config template..."):
            try:
                test_data_and_template = generate_test_data_and_template(st.session_state.accounting_paper, llm_provider, llm_model)
                st.markdown("### Generated Test Data and Config Template:")
                st.code(test_data_and_template, language="python")
                
                download_button = download_link(
                    test_data_and_template, "test_data_and_config_template.py", "Download Test Data and Config Template"
                )
                st.markdown(download_button, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred while generating test data and config template: {str(e)}")

st.markdown("---")
st.markdown("© 2024 Accounting Paper Generator. All rights reserved.")

st.sidebar.markdown("---")
st.sidebar.subheader("Debug Information")
if st.sidebar.checkbox("Show Debug Info"):
    st.sidebar.json(llm_config)
    if st.sidebar.button("Show Logs"):
        with open("debug.log", "r") as log_file:
            st.sidebar.text_area("Log Contents", log_file.read(), height=300)