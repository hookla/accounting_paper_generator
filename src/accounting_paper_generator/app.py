import streamlit as st

from accounting_paper_generator.ui.components import (accounting_paper, events,
                                                      product_description,
                                                      test_data)
from accounting_paper_generator.ui.sidebar import render_sidebar

st.set_page_config(page_title="Accounting Paper Generator", layout="wide")


def main():
    render_sidebar()

    st.title("Accounting Paper Generator")

    product_description.render()
    events.render()
    accounting_paper.render()
    test_data.render()

    st.markdown("---")
    st.markdown("© 2024 Accounting Paper Generator. All rights reserved.")


if __name__ == "__main__":
    main()
