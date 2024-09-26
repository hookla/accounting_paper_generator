import streamlit as st

from accounting_paper_generator.core.events import suggest_events


def render():
    st.header("Step 2: Events")
    st.markdown("List the events related to your product or service.")

    if st.button("Suggest Events", key="suggest_events_button"):
        if not st.session_state.get("product_description"):
            st.error("Please provide a product description to suggest events.")
        else:
            with st.spinner("Generating event suggestions..."):
                try:
                    suggested_events = suggest_events(
                        st.session_state.product_description,
                        st.session_state.llm_provider,
                        st.session_state.llm_model,
                    )
                    st.session_state.events = suggested_events
                    st.success("Events suggested successfully!")
                except Exception as e:
                    st.error(f"An error occurred while suggesting events: {str(e)}")

    events = st.text_area(
        "Events (Markdown format)",
        value=st.session_state.get("events", ""),
        height=300,
        key="events_input",
    )
    st.session_state.events = events

    if events:
        st.markdown(events)
    else:
        st.info(
            "No events suggested yet. Use the 'Suggest Events' button to generate events."
        )
