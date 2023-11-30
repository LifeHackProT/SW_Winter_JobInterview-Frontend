import streamlit as st
import base64
from openai import OpenAI
# speech to text
from bokeh.models import CustomJS, Button, Toggle
from streamlit_bokeh_events import streamlit_bokeh_events
# video
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from streamlit_float import *


# 레이아웃
st.set_page_config(layout="wide")
# 초기화
if 'caption' not in st.session_state:  # 버튼 내용
    st.session_state.caption = ""

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# AI response
question = "Hello, this is AI mock Interview."

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": question}]


# 자막 버튼
def caption():
    col_buttonl, col_buttonr = st.columns([1, 1])  # 비율 col_buttonl : col_buttonr
    with col_buttonl:
        if st.button('caption'):
            with st.chat_message("assistant"):
                st.markdown(st.session_state.messages[-1].get("content"))
            with col_buttonr:
                st.button('cancel')


# TTS from AI
def tts():
    tts_button = Button(label="AI Answer", width=100)
    tts_button.js_on_event("button_click", CustomJS(code=f"""
                var u = new SpeechSynthesisUtterance();
                u.text = "{st.session_state.messages[-1].get("content")}";
                u.lang = 'en-US';

                speechSynthesis.speak(u);
                """))
    st.bokeh_chart(tts_button)


# speech to text
def record():
    # speech to text
    stt_button = Button(label="Speak", width=100, align='center')

    stt_button.js_on_event("button_click", CustomJS(code="""
        
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        
        recognition.onresult = function(e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=40,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            userinput = result.get("GET_TEXT")
            with st.chat_message("user"):
                st.write(userinput)
            return userinput


# 사이드 바
def chatlog():
    st.sidebar.title("Chat Log")
    # Display chat history
    for messages in st.session_state.messages:
        with st.sidebar.chat_message(messages["role"]):
            st.markdown(messages["content"])
    # recording & AI speaking
    rec_col1, rec_col2 = st.columns([1, 1])  # 비율 rec_col1 : rec_rol2
    with rec_col1:
        tts()  # AI tts
    with rec_col2:
        userinput = record()  # user recording
    # Chat Input & AI question
    prompt = st.chat_input("Type in your answer")
    if userinput is not None:
        response(userinput)
    if prompt:
        response(prompt)
    userinput = None


# AI chat response
def response(prompt):
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
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# AI 화면
def aivideo():
    file_ = open("jobinterview.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="job-interview" width="100%">',
        unsafe_allow_html=True,
    )


# 사용자 화면
def uservideo():
    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )


# 메인
def main():
    # 제목 및 내용
    st.title("AI mock interview")
    # 화면
    col1, col2, col3 = st.columns([0.2, 1, 0.2])  # 비율 col1:col2:col3
    with col2:
        # AI 화면
        aivideo()
        # 사용자 화면
        uservideo()
    # 사이드 바
    chatlog()
    # AI 자막
    caption()


if __name__ == '__main__':
    main()
