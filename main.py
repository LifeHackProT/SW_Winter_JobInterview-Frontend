import cv2
import streamlit as st
import OpenCVDemoCode
import numpy as np
from PIL import Image
from streamlit_chat import message

#OpenAI API call
import os
import openai


# Layout
st.set_page_config(layout="wide")


def caption(button):
    st.session_state['caption'] = button
    st.session_state.count += 1
    if st.session_state.count == 2:
        st.session_state['caption'] = 'caption'  # 버튼 클릭 시 표기
        st.session_state.count = 0


def record():
    st.text_input()

# 초기화
if 'count' not in st.session_state:  # 버튼 클릭 횟수
    st.session_state.count = 0
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state['caption'] = 'caption place'
if 'past' not in st.session_state:  # 과거 메시지
    st.session_state.past = []
if 'generated' not in st.session_state:  # 생성된 메시지
    st.session_state.generated = []


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

# 사이드 바
def sidebar():
    st.sidebar.title("Chat log")
    chat_placeholder = st.sidebar.empty()

    # with chat_placeholder.container():
    #     for i in range(len(st.session_state['generated'])):
    #         message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
    #         message(
    #             st.session_state['generated'][i]['data'],
    #             key=f"{i}",
    #             allow_html=True,
    #             is_table=True if st.session_state['generated'][i]['type'] == 'table' else False
    #         )
    #
    #     st.button("Clear message", on_click=on_btn_click)
    #
    # with st.sidebar.container():
    #     st.text_input("User Input:", on_change=on_input_change, key="user_input")

# 웹캠으로 읽고, 출력
# def camera():
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'DataSet/haarcascade_frontalface_default.xml')
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
#
#     while True:
#         ret, frame = cap.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiSacle(gray, 1.3, 5)
#
#         box_size = (100,100)
#         cv2.imshow('frame', frame)

    # cap.release()
    # cv2.destroyAllWindows()

def image():
    st.image("Dataset/Test.jpg")
    cap = cv2.Image.Capture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 100)


def main():
    sidebar()
    st.title("User interface")
    st.text("We use OpenCV and Streamlit for this demo")

    st.camera_input(label="User screen", key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    #OpenCVDemoCode.camera()
    col1, col2 = st.columns([1, 1])  # 비율 col1:col2:col3
    with col1:
        st.button(label="caption", on_click=caption('clicked'))
    with col2:
        # st.text(st.session_state['caption'])
        st.button(label="record", on_click=' ')


if __name__ == '__main__':
    main()