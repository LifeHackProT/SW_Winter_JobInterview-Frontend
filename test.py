import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_chat import message
import keyboard
import openai
import time


def update_theme(primary_color, background_color, secondary_background_color):
    with open(file_path, 'r') as fr:
        lines = fr.readlines()

    with open(file_path, 'w') as fw:
        for i, line in enumerate(lines):
            if 'primaryColor' in line:
                lines[i] = f'primaryColor = "{primary_color}"\n'
            if 'backgroundColor' in line:
                lines[i] = f'backgroundColor = "{background_color}"\n'
            if 'secondaryBackgroundColor' in line:
                lines[i] = f'secondaryBackgroundColor = "{secondary_background_color}"\n'
        fw.writelines(lines)



# 레이아웃 설정
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

file_path = './.streamlit/config.toml'

message_history = []

with st.sidebar:
    choose = option_menu(
        "Company", ['Amazon', 'Apple', 'Microsoft', 'Google', 'Meta'],
        icons=['bi bi-heart-fill', 'bi bi-apple', 'bi bi-microsoft', 'bi bi-google', 'bi bi-meta'],
        styles={
            "container": {"padding": "4!important"},
            "icon": {"font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
        }
    )

theme_settings = {
    "Amazon": ("#ffb03b", "#FFFFFF", "#faca82"),
    "Apple": ("#000000", "#FFFFFF", "#bdbdbd"),
    "Microsoft": ("#7CBB00", "#FFFFFF", "#c8e889"),
    "Google": ("#EA4335", "#FFFFFF", "#e38f88"),
    "Meta": ("#0078D7", "#FFFFFF", "#a4d1f5")
}

if choose in theme_settings and not st.session_state.get("theme_selected", False):
    primary_color, background_color, secondary_background_color = theme_settings[choose]
    update_theme(primary_color, background_color, secondary_background_color)
    keyboard.press_and_release('enter')

# OpenAI API 키 설정
openai.api_key = " "
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "ft:davinci-002:personal::8J2Uy4zo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 면접 시작 버튼
if not st.session_state.get("interview_started", False):
    start_button_clicked = st.button("Mock_interview Start", key="start_button")
    if start_button_clicked:
        st.session_state.interview_started = True

def generate_question(prompt, model):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=30
    )
    question = response.choices[0].text.strip()
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

                # 면접관(모델)이 점수를 매깁니다.
                with st.chat_message("assistant"):
                    # score = model_scoring_function(user_answer)
                    score = 90  # 임시로 점수를 설정함 (모델에서 생성한 가짜 점수)

                    st.markdown(f"**Scoring**: {score}/100")

                    st.session_state.interview_records.append({
                        "question": question,
                        "answer": user_answer,
                        "score": score
                    })

                # 다음 질문이 있는지 확인합니다.
                st.session_state.interview_questions.pop(question)

    # 기록된 답변과 점수를 표시
    if st.sidebar.checkbox("Show Interview Records"):
        if st.session_state.interview_records:
            st.sidebar.header("Interview Records")
            for record in st.session_state.interview_records:
                st.sidebar.markdown(f"**Question**: {record['question']}")
                st.sidebar.markdown(f"**Your Answer**: {record['answer']}")
                st.sidebar.markdown(f"**Score**: {record['score']}/100")
                st.sidebar.markdown("---")

    styl = f"""
    <style>
        .stTextInput {{
          position: fixed;
          bottom: 3rem;
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)



# import streamlit as st
# import numpy as np
# import sounddevice as sd
# from pydub import AudioSegment
# import openai
#
# # Load OpenAI API key
# openai.api_key = "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"
#
# # Streamlit layout configuration
# st.set_page_config(page_title="Voice Assistant", layout="wide")
# st.title("실시간 음성 전사 및 출력")
#
# # Placeholder for transcribed text
# transcribed_text = st.empty()
#
# # Function to transcribe audio asynchronously
# @st.cache(allow_output_mutation=True)
# def transcribe_audio(audio_data):
#     response = openai.Transcription.create(model="whisper-1", audio=audio_data)
#     return response['text']
#
# # Function to record audio and transcribe
# def record_and_transcribe():
#     # Record audio
#     st.text("말하고 있는 중입니다...")
#     audio_data = sd.rec(int(44100 * 5), channels=2, dtype=np.int16)
#     sd.wait()
#
#     # Convert to AudioSegment for OpenAI API
#     audio_segment = AudioSegment(
#         audio_data.tobytes(),
#         frame_rate=44100,
#         sample_width=audio_data.dtype.itemsize,
#         channels=2
#     )
#
#     # Transcribe audio
#     transcription_result = transcribe_audio(audio_segment)
#
#     # Display transcribed text
#     transcribed_text.text(transcription_result)
#     st.success("전사가 완료되었습니다.")
#
# # Streamlit UI
# if st.button("음성 전사 시작"):
#     record_and_transcribe()
