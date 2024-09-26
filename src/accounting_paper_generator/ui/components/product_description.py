import streamlit as st

from accounting_paper_generator.core.product_description import \
    enhance_product_description


def render():
    st.header("Step 1: Product Description")
    st.markdown("Enter a detailed description of the product or service.")

    product_description = st.text_area(
        "Product Description",
        value=st.session_state.get("product_description", ""),
        height=200,
        help="Enter a detailed description of the product or service.",
        key="product_description_input",
    )

    # Update session state
    st.session_state.product_description = product_description

    if st.button("Enhance Product Description", key="enhance_description_button"):
        if not product_description:
            st.error("Please provide a product description to enhance.")
        else:
            with st.spinner("Enhancing product description..."):
                try:
                    enhanced_description = enhance_product_description(
                        st.session_state.product_description,
                        st.session_state.llm_provider,
                        st.session_state.llm_model,
                    )
                    st.session_state.product_description = enhanced_description
                    st.success("Product description enhanced successfully!")
                except Exception as e:
                    st.error(
                        f"An error occurred while enhancing the product description: {str(e)}"
                    )

    # Display enhanced description if available
    if st.session_state.get("product_description"):
        st.markdown("### Enhanced Product Description")
        st.write(st.session_state.product_description)
