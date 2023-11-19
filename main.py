import streamlit as st
from PIL import Image
import base64
from st_audiorec import st_audiorec

# 레이아웃
st.set_page_config(layout="wide")
# 초기화
if 'count' not in st.session_state:  # 버튼 클릭 횟수
    st.session_state.count = 0
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state['caption'] = 'caption place'
if 'message' not in st.session_state:  # chat history
    st.session_state.message = []


def caption(button):
    st.session_state['caption'] = button
    st.session_state.count += 1
    if st.session_state.count == 2:
        st.session_state['caption'] = 'caption'  # 버튼 클릭 시 표기
        st.session_state.count = 0


def record():
    # recodring
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')


# 사이드 바
def sidebar():
    st.sidebar.title("Chat Log")
    for message in st.session_state.message:  # Display chat history
        with st.sidebar.chat_message(message["role"]):
            st.markdown(message["content"])
    # Chat Input
    if prompt := st.chat_input("Type in your Answer"):
        with st.sidebar.chat_message("user"):
            st.markdown(prompt)  # Display user message
        st.session_state.message.append({"role": "user", "content": prompt})  # Add to chat history
    # AI response
    question = "Hello, this is AI mock Interview."
    with st.sidebar.chat_message("assistant"):
        st.markdown(question)  # Display assistant response
    st.session_state.message.append({"role": "assistant", "content": question})  # Add to chat history


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
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="job-interview" width="100%">',
        unsafe_allow_html=True,
    )
    # 버튼
    col1, col2 = st.columns([1, 1])  # 비율 col1:col2
    with col1:
        st.text('')  # 줄바꿈
        st.button(label="caption", on_click=caption('clicked'))
    with col2:
        st.text('')  # 줄바꿈
        st.text(st.session_state['caption'])
    # Recording
    record()


if __name__ == '__main__':
    main()