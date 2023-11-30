import openai
import streamlit as st
from PIL import Image
import torch
import numpy as np

from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av

# Layout
st.set_page_config(layout="wide")

def sidebar():
    st.sidebar.title("Chat log")

file_path = './.streamlit/config.toml'

# Set OpenAI API Key
openai.api_key = " "
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "ft:gpt-3.5-turbo-0613:personal::8QHA21Zj"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Interview start button
if not st.session_state.get("interview_started", False):
    start_button_clicked = st.button("Interview Start", key="start button")
    if start_button_clicked:
        st.session_state.interview_started = True

def generate_question(prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=30
    )
    question = response.choices[0].message['content'].strip()
    return question


def generate_amazon_interview_question():
    prompt = "Create questions for interviewers to ask about your IT experience.."
    model = st.session_state.openai_model
    generated_question = generate_question(prompt, model)
    return generated_question



# generated_question3 = generate_amazon_interview_question()
# 버튼을 누른 후에만 질문 및 답변 단계를 실행
if st.session_state.get("interview_started", False):
    if "interview_questions" not in st.session_state:
        generated_question = generate_amazon_interview_question()
        generated_question2 = generate_amazon_interview_question()
        st.session_state.interview_questions = {
            "Tell me about yourself.": None,
            generated_question: None,
            generated_question2: None,
            # generated_question3: None,
        }

    if "interview_records" not in st.session_state:
        st.session_state.interview_records = []

    if st.session_state.interview_questions:
        question = list(st.session_state.interview_questions.keys())[0]

        if st.session_state.interview_questions[question] is None:
            # 면접관(모델)이 질문을 제시합니다.
            with st.chat_message("assistant"):
                st.markdown(f"**Interviewer**: {question}")

            # 사용자에게 답변을 입력받습니다.
            user_answer = st.text_input("Your answer:", key=f"answer_{question}")

            if user_answer:
                # 사용자의 답변을 기록하고, 다음 질문을 준비합니다.
                st.session_state.interview_questions[question] = user_answer

                # 사용자의 답변을 st.chat_message로 화면에 표시
                with st.chat_message("user"):
                    st.markdown(user_answer)

                # 다음 질문이 있는지 확인
                st.session_state.interview_questions.pop(question)


device = 'cpu'
if not hasattr(st, 'classifier'):
    st.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)
    # st.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', _verbose=False)
    


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # vision processing
        flipped = img[:, ::-1, :]

        # model processing
        im_pil = Image.fromarray(flipped)
        results = st.model(im_pil, size=112)
        bbox_img = np.array(results.render()[0])

        return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")


webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=False,
)
