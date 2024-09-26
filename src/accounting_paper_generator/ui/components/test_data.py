import streamlit as st

from accounting_paper_generator.core.test_data import \
    generate_test_data_and_template
from accounting_paper_generator.utils.file_operations import download_link


def render():
    st.header("Step 4: Generate Test Data and Config Template")
    st.markdown(
        "Generate test data and a config template based on the accounting paper."
    )

    if st.button(
        "Generate Test Data and Config Template", key="generate_test_data_button"
    ):
        if not st.session_state.get("accounting_paper"):
            st.error("Please generate or paste an accounting paper first.")
        else:
            with st.spinner("Generating test data and config template..."):
                try:
                    test_data_and_template = generate_test_data_and_template(
                        st.session_state.accounting_paper,
                        st.session_state.llm_provider,
                        st.session_state.llm_model,
                    )
                    st.session_state.test_data_and_template = test_data_and_template
                    st.success("Test data and config template generated successfully!")
                except Exception as e:
                    st.error(
                        f"An error occurred while generating test data and config template: {str(e)}"
                    )

    if (
        "test_data_and_template" in st.session_state
        and st.session_state.test_data_and_template
    ):
        st.markdown("### Generated Test Data and Config Template:")
        st.code(st.session_state.test_data_and_template, language="python")

        download_button = download_link(
            st.session_state.test_data_and_template,
            "test_data_and_config_template.py",
            "Download Test Data and Config Template",
        )
        st.markdown(download_button, unsafe_allow_html=True)
