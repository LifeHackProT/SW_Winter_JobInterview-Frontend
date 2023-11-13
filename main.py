import cv2
import streamlit as st
import numpy as np
from PIL import Image

# 레이아웃
st.set_page_config(layout="wide")
# 초기화
if 'count' not in st.session_state:  # 버튼 클릭 횟수
    st.session_state.count = 0
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state['caption'] = 'caption place'

# 웹캠으로 읽고, 출력
# cap = cv2.VideoCapture(0)
# if cap.isOpened():
#     while True:
#         ret, img = cap.read()


def caption(button):
    st.session_state['caption'] = button
    st.session_state.count += 1
    if st.session_state.count == 2:
        st.session_state['caption'] = 'caption'  # 버튼 클릭 시 표기
        st.session_state.count = 0


def record():
    st.text_input()


# 사이드 바
def sidebar():
    st.sidebar.title("Chat log")



def main():
    sidebar()
    st.title("User interface")
    st.text("We use OpenCV and Streamlit for this demo")

    col1, col2 = st.columns([1, 1])  # 비율 col1:col2:col3
    with col1:
        st.button(label="caption", on_click=caption('clicked'))
    with col2:
        st.text(st.session_state['caption'])
        st.button(label="record", on_click=' ')


if __name__ == '__main__':
    main()