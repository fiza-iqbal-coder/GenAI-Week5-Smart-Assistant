
import streamlit as st
from agent import run_agent

# ==========================================
# STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="GenAI Smart Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 GenAI Smart Assistant")
st.caption("AI-powered assistant for Weather and Loan EMI calculations.")

# ==========================================
# INITIALIZE CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("Assistant Settings")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("**Available Tools**")
    st.write("🌤️ Weather Information")
    st.write("💰 Loan EMI Calculator")

# ==========================================
# DISPLAY PREVIOUS MESSAGES
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================

if prompt := st.chat_input("Ask about weather or calculate EMI..."):

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ======================================
    # ASSISTANT RESPONSE
    # ======================================

    with st.chat_message("assistant"):

        # Display live agent status
        status_box = st.status(
            "Thinking...",
            expanded=True
        )

        def show_status(message):
            status_box.write(message)

        try:

            # Run Gemini Agent
            response = run_agent(
                prompt,
                status_callback=show_status
            )

            # Mark processing as complete
            status_box.update(
                label="Completed",
                state="complete",
                expanded=False
            )

            # Display final response
            st.markdown(response)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

        except Exception as error:

            status_box.update(
                label="An error occurred",
                state="error",
                expanded=True
            )

            st.error(str(error))
