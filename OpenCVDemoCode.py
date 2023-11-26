import cv2

def camera():
    # 얼굴 검출을 위한 분류기 로드
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 웹캠으로부터 영상을 받아오기 위한 VideoCapture 객체 생성
    cap = cv2.VideoCapture(0)

    # 영상 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # 영상 프레임 읽기
        ret, frame = cap.read()

        # 얼굴 검출 수행
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # 얼굴이 검출된 경우
        if len(faces) > 0:
            # 가장 큰 얼굴 하나 선택
            biggest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = biggest_face

            # 얼굴이 바운딩 박스 내에 들어오는지 검사
            box_center = (int(x + w / 2), int(y + h / 2))
            box_size = (100, 100)
            if box_center[0] > box_size[0] / 2 and box_center[0] < frame.shape[1] - box_size[0] / 2 and \
                    box_center[1] > box_size[1] / 2 and box_center[1] < frame.shape[0] - box_size[1] / 2:
                cv2.putText(frame, "탐지완료", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # #바운딩 박스 크기 고정
            #     bbox_size = (300, 300)

            for (x, y, w, h) in faces:
            # 얼굴 중심 좌표 계산
                center_x, center_y = int(x + w/2), int(y + h/2)

                # 바운딩 박스 시작점 계산
                bbox_x, bbox_y = int(center_x - box_size[0]/2), int(center_y - box_size[1]/2)

                # 바운딩 박스 그리기
                cv2.rectangle(frame, (bbox_x, bbox_y), (bbox_x + box_size[0], bbox_y + box_size[1]), (255, 0, 0), 2)

        # 영상 출력
        cv2.imshow('frame', frame)

        # q를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료
    cap.release()
    cv2.destroyAllWindows()

