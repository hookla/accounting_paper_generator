import base64

import streamlit as st
from backend import generate_accounting_paper, suggest_events


def download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'


st.set_page_config(page_title="Accounting Paper Generator", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .output-paper {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    .big-area {
        height: 300px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("Controls")
    st.markdown("Use these controls to generate your accounting paper.")

    product_description = st.text_area(
        "Product Description",
        height=200,
        help="Enter a detailed description of the product or service.",
    )

    if st.button("Suggest Events"):
        if not product_description:
            st.error("Please provide a product description to suggest events.")
        else:
            with st.spinner("Generating event suggestions..."):
                try:
                    suggested_events = suggest_events(product_description)
                    st.session_state.events = "\n".join(suggested_events)
                except Exception as e:
                    st.error(f"An error occurred while suggesting events: {str(e)}")

# Main content
st.title("Accounting Paper Generator")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: Events")
    st.markdown("List the events related to your product or service, one per line.")

    # Initialize session state for events if it doesn't exist
    if "events" not in st.session_state:
        st.session_state.events = ""

    # Display the events text area, using the session state to maintain its content
    events = st.text_area("List of Events", value=st.session_state.events, height=400)

    # Update the session state when the user modifies the events
    if events != st.session_state.events:
        st.session_state.events = events

with col2:
    st.subheader("Step 2: Generate Paper")
    st.markdown("Click the button below to generate your accounting paper.")

    if st.button("Generate Paper"):
        if not product_description or not events:
            st.error("Please provide both a product description and a list of events.")
        else:
            with st.spinner("Generating accounting paper..."):
                try:
                    paper = generate_accounting_paper(product_description, events)
                    st.markdown("### Generated Paper:")
                    st.markdown(paper, unsafe_allow_html=True)
                    # Create download button
                    download_button = download_link(
                        paper, "accounting_paper.txt", "Download Paper"
                    )
                    st.markdown(download_button, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occurred while generating the paper: {str(e)}")

st.markdown("---")
st.markdown("© 2024 Accounting Paper Generator. All rights reserved.")
