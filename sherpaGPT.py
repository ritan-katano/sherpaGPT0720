import os
import openai
import streamlit as st

# Set the OpenAI API key
openai.api_key = "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"

print(openai.api_key )

system_message = "あなたは探究学習のメンターです。ここで指す探究学習とは自ら問いを立てて、その理解に向けて情報を収集・整理・分析したり、周囲の人と意見交換・協働したりしながら進めていく学習活動のことです。あなたは今から一人の高校生が今までどのように過ごしてきたのかを聞きながら、その子の性格などを分析していきます。相手がどんな性格でどのようなことを考えることが好きなのか、そして将来の自分がやっていくと良いことを見つけるためのものです。高校生の人生を聴く上で意識してほしいのは、何が好きなのかや何が嫌いなのかを今までの人生を振り返りながら、探してあげることです。その子にしかない面白い部分にフォーカスしてあげながら、面白がって掘り進めていくことが大事です。注意することはなるべく押し付けがましくならないように、打ち込まれた解答に対して適切なフィードバックをしながら深ぼる質問を投げかけてあげてください。質問の深掘り方としては具体的にその状況を付加ぼってあげる質問や「いつ・どこで・誰の・何の・どのくらい・なぜ」などを基軸にしてください。この対話を通して、学習者の気になる「関わりのある単語を10個見つけてあげることがゴールです。なるべくそのような単語が見つかるように、質問を投げかけてあげながら会話を楽しませてくださいい。."


# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Custom CSS styles
custom_css = """
<style>
    /* 背景色を白に設定 */
    body {
        background-color: #FFFFFF;
    }

    /* メッセージコンテナのスタイル */
    .message-container {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
    }

    /* ユーザーメッセージのスタイル */
    .user-message {
        background-color: #e8f5e9;
    }

    /* アシスタントメッセージのスタイル */
    .assistant-message {
        background-color: #e3f2fd;
    }

    /* メッセージのテキストのスタイル */
    .message-text {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
</style>
"""

# Render custom CSS styles
st.markdown(custom_css, unsafe_allow_html=True)

st.title("sherpaGPT")

def add_message(role, content):
    st.session_state.conversation.append({"role": role, "content": content})

# Display conversation history
if st.session_state.conversation:
    for message in st.session_state.conversation:
        role = message["role"]
        content = message["content"]
        if role == "user":
            st.text(f"You: {content}")
        elif role == "assistant":
            st.text(f"Assistant: {content}")

# User input
user_message = st.text_input("Please type your message")

# Process user input
if st.button("Submit"):
    # Add user message to conversation
    add_message("user", user_message)

    # Retrieve conversation history
    conversation = [{"role": "system", "content": system_message}] + st.session_state.conversation

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )

    # Add assistant response to conversation
    assistant_response = response['choices'][0]['message']['content']
    add_message("assistant", assistant_response)

    # Display assistant response
    st.text(f"Assistant: {assistant_response}")
