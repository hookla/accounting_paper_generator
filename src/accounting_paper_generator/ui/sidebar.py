import streamlit as st

from accounting_paper_generator.utils.llm import LLM_CONFIG


def render_sidebar():
    with st.sidebar:
        st.title("Controls")

        provider_options = list(LLM_CONFIG["providers"].keys())
        llm_provider = st.selectbox(
            "Select LLM Provider",
            options=provider_options,
            format_func=lambda x: LLM_CONFIG["providers"][x]["name"],
            help="Choose the AI provider for generating the paper.",
        )

        model_options = [
            model["name"] for model in LLM_CONFIG["providers"][llm_provider]["models"]
        ]
        model_display_names = {
            model["name"]: model["display_name"]
            for model in LLM_CONFIG["providers"][llm_provider]["models"]
        }
        llm_model = st.selectbox(
            f"Select {LLM_CONFIG['providers'][llm_provider]['name']} Model",
            options=model_options,
            format_func=lambda x: model_display_names[x],
            help=f"Choose the {LLM_CONFIG['providers'][llm_provider]['name']} model to use.",
        )

        # Store selected provider and model in session state
        st.session_state.llm_provider = llm_provider
        st.session_state.llm_model = llm_model

        st.sidebar.markdown("---")
        st.sidebar.subheader("Debug Information")
        if st.sidebar.checkbox("Show Debug Info"):
            st.sidebar.json(LLM_CONFIG)
            if st.sidebar.button("Show Logs"):
                with open("debug.log", "r", encoding="utf-8") as log_file:
                    st.sidebar.text_area("Log Contents", log_file.read(), height=300)
