import streamlit as st
import base64
from st_audiorec import st_audiorec
from openai import OpenAI

# 레이아웃
st.set_page_config(layout="wide")
# 초기화
if 'count' not in st.session_state:  # 버튼 클릭 횟수
    st.session_state.count = 0
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state['caption'] = 'caption place'

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# AI response
question = "Hello, this is AI mock Interview."

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "user", "content": ""}]


def caption(string):
    st.session_state['caption'] = string
    st.session_state.count += 1
    if st.session_state.count == 2:
        st.session_state['caption'] = 'caption place'  # 버튼 클릭 시 표기
        st.session_state.count = 0


def record():
    # recodring
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')


# 사이드 바
def sidebar():
    st.sidebar.title("Chat Log")
    # Display chat history
    for messages in st.session_state.messages:
        with st.sidebar.chat_message(messages["role"]):
            st.markdown(messages["content"])
    # Chat Input & AI question
    if prompt := st.chat_input("Type in your Answer"):
        st.session_state.messages.append({"role": "user", "content": prompt})  # Add to chat history
        with st.sidebar.chat_message("user"):
            st.markdown(prompt)  # Display user message
        with st.sidebar.chat_message("assistant"):  # Display assistant response in chat message container
            message_placeholder = st.empty()
            full_response = ""
        for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def main():
    # 사이드 바
    sidebar()
    # 내용
    st.title("AI mock interview")
    st.text("To start the mock Interview, answer the following question")

    # AI 비디오
    file_ = open("jobinterview.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    
    # User 비디오
    st.camera_input(label="User screen", key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False,
                    label_visibility="visible")

    # 화면
    col1, col2, col3 = st.columns([0.2, 1, 0.2])  # 비율 col1:col2:col3
    with col2:
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="job-interview" width="100%">',
            unsafe_allow_html=True,
        )
        col_l, col_m, col_r = st.columns([0.1, 1, 0.1])  # 비율 col_l:col_m:col_r
        with col_m:
            # Recording
            record()
    co_button, co_caption = st.columns([0.4, 1])  # 비율 co_button:co_caption
    # 사용자 화면
    st.camera_input(label="User screen", key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False,
                    label_visibility="visible")

    # 버튼
    with co_button:
        st.text('')  # 줄바꿈
        st.button(label="caption", on_click=caption(question))
    with co_caption:
        st.text('')  # 줄바꿈
        st.text(st.session_state['caption'])


if __name__ == '__main__':
    main()