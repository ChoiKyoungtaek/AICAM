import time
from adafruit_servokit import ServoKit
from picamera2 import Picamera2
import cv2
from ultralytics import YOLO

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT = 65362, 65364, 65361, 65363
kit = ServoKit(channels=16)
# B0283 보드의 서보 모터 연결 채널 (기본값: Pan=0번, Tilt=1번)
PAN_CHANNEL = 0
TILT_CHANNEL = 1
# 서보 모터 이동 가능 범위 제한 (기구물 파손 방지)
PAN_MIN, PAN_MAX = 0, 180
TILT_MIN, TILT_MAX = 0, 180
angle_delta = 5

def set_angle(channel, angle):
    """지정한 채널의 서보 모터 각도를 변경 (안전 범위 적용)"""
    if channel == PAN_CHANNEL:
        angle = max(PAN_MIN, min(PAN_MAX, angle))
    elif channel == TILT_CHANNEL:
        angle = max(TILT_MIN, min(TILT_MAX, angle))    
    kit.servo[channel].angle = angle
    return angle

def main():
    current_pan = 90
    current_tilt= 90
    set_angle(PAN_CHANNEL,current_pan)
    set_angle(TILT_CHANNEL,current_tilt)
    time.sleep(1.0)
    
    modelpath = 'yolo26n.pt'
    print("YOLO 모델을 불러오는 중...")
    model = YOLO(modelpath)     
    # 2. Picamera2 설정 및 시작
    picam2 = Picamera2()
    # 해상도를 640x480으로 설정 (YOLO 처리 속도를 위해 너무 높이지 않는 것이 좋습니다)
    config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()    
    print("카메라 및 AI 인식 시작! (종료하려면 화면 클릭 후 'q' 누르기)")
    try:
        while True:
            # 프레임 읽기 및 BGR 변환 (OpenCV 표준)
            frame_bgr = picam2.capture_array()
            # 3. YOLO 물체 검출 수행
            # verbose=False를 넣어 터미널에 로그가 계속 찍히는 것을 방지합니다.
            # imgsz=320을 추가하면 내부적으로 이미지를 줄여서 분석하므로 속도가 더 빨라집니다.
            results = model.track(frame_bgr, verbose=False, imgsz=320, conf=0.5, classes=0, persist=True,tracker='bytetrack.yaml')
            # 4. 검출된 물체에 네모 박스와 이름(라벨) 그리기
            # results[0].plot()은 박스가 그려진 새로운 이미지(Numpy 배열)를 반환합니다.
            annotated_frame = results[0].plot()
            # 5. 화면에 출력
            cv2.imshow('YOLOv8 Object Detection', annotated_frame)
            # 'q' 키로 종료
            key = cv2.waitKeyEx(1)
            if key>0:
                print(key)
                if key & 0xFF == ord('q'):
                    break
                elif key==KEY_UP:
                    current_tilt=set_angle(TILT_CHANNEL,current_tilt+angle_delta)
                elif key==KEY_DOWN:
                    current_tilt=set_angle(TILT_CHANNEL,current_tilt-angle_delta)
                elif key==KEY_LEFT:
                    current_pan=set_angle(PAN_CHANNEL,current_pan+angle_delta)
                elif key==KEY_RIGHT:
                    current_pan=set_angle(PAN_CHANNEL,current_pan-angle_delta)
                else:
                    current_pan=set_angle(PAN_CHANNEL,90)
                    current_tilt=set_angle(TILT_CHANNEL,90)            
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    main()