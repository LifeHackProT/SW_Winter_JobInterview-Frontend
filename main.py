import cv2
import streamlit as st
from OpenCVDemoCode import camera
import numpy as np
from PIL import Image

# 레이아웃
st.set_page_config(layout="wide")
# 초기화
if 'count' not in st.session_state:  # 버튼 클릭 횟수
    st.session_state.count = 0
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state['caption'] = 'caption place'


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
    # code =
    st.camera_input(label="User screen", key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    col1, col2 = st.columns([1, 1])  # 비율 col1:col2:col3
    with col1:
        st.button(label="caption", on_click=caption('clicked'))
    with col2:
        st.text(st.session_state['caption'])
        st.button(label="record", on_click=' ')


if __name__ == '__main__':
    main()