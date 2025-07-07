import streamlit as st
from PIL import Image
from main import assistant

# Setting page config
st.set_page_config(
    page_title="ImmigrantAI Assistant",
    page_icon="logo.png",
    layout="centered"
)


def load_css():
    bg_color = "#121212"            
    sidebar_bg = "#0D0D0D"          
    message_bg = "#1E1E1E"          
    text_color = "#FFFFFF"          

    st.markdown(f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            background-color: {bg_color};
        }}

        .stSidebar {{
            background-color: {sidebar_bg} !important;
        }}

        .stChatMessage {{
            background-color: {message_bg} !important;
            color: {text_color} !important;
            border-radius: 10px;
            padding: 10px;
        }}

        p, h1, h2, h3, h4, h5, h6 {{
            color: {text_color};
        }}

        .welcome-message {{
            text-align: center;
            margin-bottom: 2rem;
            color: {text_color};
        }}

        .stTextInput input {{
            background-color: {message_bg};
            color: {text_color};
        }}
    </style>
    """, unsafe_allow_html=True)


def main():
    load_css()

    # ===== CHAT INTERFACE CODE STARTS HERE =====
    # Display logo and welcome message for new chat
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("logo-removebg-preview.png", width=100)
        with col2:
            st.markdown("""
            <div class="welcome-message">
                <h1>Hi, I'm ImmigrantAI</h1>
                <p>Ask me about visas, immigration policies, or application procedures.</p>
                <p>How can I help you today?</p>
            </div>
            """, unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Type your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Stream the response
            for chunk in assistant.run(prompt):
                if hasattr(chunk, 'content'):
                    full_response += chunk.content
                else:
                    full_response += str(chunk)
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
