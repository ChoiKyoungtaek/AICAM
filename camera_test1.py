from picamera2 import Picamera2
import cv2

def main():
    # 1. Picamera2 객체 생성
    picam2 = Picamera2()

    # 2. 카메라 설정 (해상도 640x480, RGB 포맷)
    # YOLO를 돌리기에는 640x480 해상도가 연산 속도와 화질 면에서 가장 적절합니다.
    config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)

    # 3. 카메라 시작
    picam2.start()
    print("Picamera2가 시작되었습니다. 종료하려면 'q' 키를 누르세요.")

    try:
        while True:
            # 4. 카메라에서 프레임을 Numpy 배열(행렬)로 바로 가져오기
            frame = picam2.capture_array()            

            # 5. 화면에 출력
            cv2.imshow('Picamera2 View', frame)

            # 'q' 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # 6. 안전하게 카메라 종료
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()