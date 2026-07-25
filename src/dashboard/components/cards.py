import streamlit as st

def metric_card(title, value, delta=None):

    col = st.container(border=True)

    with col:

        st.caption(title)

        st.metric(
            label="",
            value=value,
            delta=delta
        )