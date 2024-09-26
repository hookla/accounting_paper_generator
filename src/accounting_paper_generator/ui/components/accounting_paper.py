import streamlit as st

from accounting_paper_generator.core.accounting_paper import \
    generate_accounting_paper
from accounting_paper_generator.utils.file_operations import download_link


def render():
    st.header("Step 3: Generate or Edit Paper")
    st.markdown("Generate an accounting paper or edit the existing one.")

    if st.button("Generate Paper", key="generate_paper_button"):
        if not st.session_state.get("product_description") or not st.session_state.get(
            "events"
        ):
            st.error("Please provide both a product description and a list of events.")
        else:
            with st.spinner("Generating accounting paper..."):
                try:
                    paper = generate_accounting_paper(
                        st.session_state.product_description,
                        st.session_state.events,
                        st.session_state.llm_provider,
                        st.session_state.llm_model,
                    )
                    st.session_state.accounting_paper = paper
                    st.success("Paper generated successfully!")
                except Exception as e:
                    st.error(f"An error occurred while generating the paper: {str(e)}")

    accounting_paper = st.text_area(
        "Accounting Paper",
        value=st.session_state.get("accounting_paper", ""),
        height=400,
        key="paper_input",
    )
    st.session_state.accounting_paper = accounting_paper

    if accounting_paper:
        st.markdown("### Current Paper:")
        st.markdown(accounting_paper, unsafe_allow_html=True)
        download_button = download_link(
            accounting_paper, "accounting_paper.txt", "Download Paper"
        )
        st.markdown(download_button, unsafe_allow_html=True)
