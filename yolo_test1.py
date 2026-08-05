from picamera2 import Picamera2
import cv2
from ultralytics import YOLO
import torch

#torch.set_num_threads(2)

def main():
    # 1. YOLO 모델 로드
    # (앞서 NCNN 변환을 했다면 "yolov8n_ncnn_model"을 입력하고,
    # 변환하지 않았다면 기본 파일인 "yolov8n.pt"를 입력하세요.)
    #modelpath = '/home/robotpi/PTZ_PRJ/yolov8n_ncnn_model'
    #modelpath = '/home/robotpi/PTZ_PRJ/yolo11n_ncnn_model'
    #modelpath = 'yolo26n.pt'
    #modelpath = '/home/robotpi/PTZ_PRJ/yolov8s_ncnn_model'
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
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()