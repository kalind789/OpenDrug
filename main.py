import streamlit as st
from src.agent import run_agent
from src.utils import TOP_DRUGS

# Page config
st.set_page_config(
    page_title="MedQuery AI",
    page_icon="💊",
    layout="centered"
)

st.title("💊 MedQuery AI")
st.caption("Drug information powered by FDA data")

with st.sidebar:
    st.warning("This app is not a substitute for professional medical advice. Always consult your doctor or pharmacist.")
    st.header("Available Drugs")
    st.caption("Detailed summaries are available for these 15 drugs. You can still ask specific questions about other medications.")
    for drug in TOP_DRUGS:
        st.markdown(f"- {drug.title()}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about any medication..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get response from agent
    with st.spinner("Looking up FDA data..."):
        response = run_agent(prompt)

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)