import openai
import os
import sys
import time
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import tempfile
from datetime import datetime
import paramiko
import soundfile as sf

# ============================================================
# API 정보
# ============================================================
openai.organization = ""
openai.api_key = ""
print("OpenAI API 정보 설정됨.")

# ============================================================
# 설정
# ============================================================
DURATION = 300  # 녹음 시간 (초)
SAMPLE_RATE = 44100  # 샘플 레이트
CHANNELS = 1  # 모노

# ============================================================
# SSH 연결 정보
# ============================================================
SSH_HOST = "your_ssh_host"
SSH_PORT = 22
SSH_USER = "ssh-user"
SSH_KEY_PATH = "C:/path-to-ssh-key-file/key.pem"
REMOTE_DIR = "/path-to-save-dir-at-remote-host/dir"
print("SSH 연결 정보 설정됨.")

# ============================================================
# 디렉토리 확인 및 생성
# ============================================================
if not os.path.exists("./data"):
    os.makedirs("./data")


# ============================================================
# 음성 파일을 텍스트로 변환하는 함수
# ============================================================
def speech_to_text(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        sf.write(temp_audio_file.name, audio_data, sample_rate)
        temp_audio_file.seek(0)
        response = openai.Audio.transcribe(model="whisper-1", file=temp_audio_file)
    return response.text


# ============================================================
# SSH로 원격 호스트에 파일 업로드
# ============================================================
def upload_to_ssh(local_filepath, remote_filepath):
    key = paramiko.RSAKey(filename=SSH_KEY_PATH)
    with paramiko.Transport((SSH_HOST, SSH_PORT)) as transport:
        transport.connect(username=SSH_USER, pkey=key)
        with paramiko.SFTPClient.from_transport(transport) as sftp:
            sftp.put(local_filepath, remote_filepath)
    print(f"파일이 {SSH_USER}@{SSH_HOST}:{remote_filepath}에 업로드됐습니다.")


# ============================================================
# 메인 로직
# ============================================================
if __name__ == "__main__":
    print("녹음을 중지하려면 Ctrl+C를 누르세요...")

    try:
        while True:
            print("녹음 중...")
            audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
            print("녹음 완료. 오디오 처리를 기다리는 중...")
            sd.wait()
            audio_data = np.int16(audio_data)
            print("오디오를 텍스트로 변환 중...")
            result = speech_to_text(audio_data, SAMPLE_RATE)

            # 현재 날짜와 시간을 가져와 파일 이름 및 경로 생성
            current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
            local_filepath = f"./data/{current_datetime}.txt"
            remote_filepath = f"{REMOTE_DIR}/{current_datetime}.txt"

            # 결과를 로컬 파일에 저장
            with open(local_filepath, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            print(f"결과가 {local_filepath}에 저장됐습니다.")

            # 로컬 파일을 SSH로 업로드
            upload_to_ssh(local_filepath, remote_filepath)

            print(f"결과가 {remote_filepath}에 저장됐습니다.")

    except KeyboardInterrupt:
        print("\n녹음이 중지되었습니다.")
