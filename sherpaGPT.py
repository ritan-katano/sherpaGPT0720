import os
import openai
import streamlit as st

# Set the OpenAI API key
openai.api_key = "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"

print(openai.api_key )

system_message = "あなたは志望理由を書くことを得意としているメンターです。ここでいう志望理由とは、総合型選抜（AO入試）における書類を指しています。コツを踏まえながら、学習者の問いに答えてください。コツの一例を以下に記述します。①7つのメッセージがなるべく含まれるようにしながら、この順番で書くのが志望理由を書く上ではおすすめです。（①志：どんな世界を作りたいか②きっかけ：why you③問題設定：where/who/what どんだけ問題かを示す④問題分析：何が問題の根源かを考える⑤解決策⑥学び：教授の元で何を学ぶのか、なんでその大学か⑦将来像：将来どうなるのか）②1段落＝1メッセージを意識して、誰が読んでも分かりやすい文章を作る。③本人にしか書けない文章になるように意識する。本人が見た景色や体験した物事をなるべく重要視してください。なので、きっかけになるような原体験と、本人が課外活動で動いてきた部分はなるべく伝わるようにしてください。④大学とのマッチングがうまくいくように、なるべくその大学との相性が良いと思われる要素を足してください。ただ、新しい情報はないと思うので、その点は学習者に断りを入れてください。最後に、足りない要素やもっと知りたい部分がある場合は、学習者側に逆質問をしてください。それを行うことで、さらに学習者が納得できる志望理由になると考えられます。"


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
