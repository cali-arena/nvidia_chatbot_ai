import streamlit as st

# Simple test app
st.title("🧪 TEST APP - Streamlit Cloud Debug")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Simple chat
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = f"🎯 TEST SUCCESS! You asked: {prompt}. This is a test response. Version: {hash(prompt) % 1000}"
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
