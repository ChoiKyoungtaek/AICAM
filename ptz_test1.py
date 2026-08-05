import time
from adafruit_servokit import ServoKit
# -------------------------------------------------------------
# 1. ServoKit 초기화
# PCA9685 보드는 기본적으로 16채널을 지원합니다.
# -------------------------------------------------------------
kit = ServoKit(channels=16)
# B0283 보드의 서보 모터 연결 채널 (기본값: Pan=0번, Tilt=1번)
PAN_CHANNEL = 0
TILT_CHANNEL = 1
# 서보 모터 이동 가능 범위 제한 (기구물 파손 방지)
PAN_MIN, PAN_MAX = 0, 180
TILT_MIN, TILT_MAX = 0, 180

def set_angle(channel, angle):
    """지정한 채널의 서보 모터 각도를 변경 (안전 범위 적용)"""
    if channel == PAN_CHANNEL:
        angle = max(PAN_MIN, min(PAN_MAX, angle))
    elif channel == TILT_CHANNEL:
        angle = max(TILT_MIN, min(TILT_MAX, angle))
    
    kit.servo[channel].angle = angle
    return angle

def main():
    print("=== Arducam B0283 팬틸트 제어 시작 ===")    
    # 1. 초기 위치 설정 (정중앙 90도)
    current_pan = 90
    current_tilt = 90    
    set_angle(PAN_CHANNEL, current_pan)
    set_angle(TILT_CHANNEL, current_tilt)
    time.sleep(1)

    # 2. 동작 테스트 (좌우/상하 스캔)
    print("스캔 동작 테스트 중...")
    
    # Pan (좌우) 이동
    for a in range(30, 151, 30):
        current_pan = set_angle(PAN_CHANNEL, a)
        time.sleep(0.3)
    set_angle(PAN_CHANNEL, 90)
    current_pan = 90

    # Tilt (상하) 이동
    for a in range(30, 151, 30):
        current_tilt = set_angle(TILT_CHANNEL, a)
        time.sleep(0.3)
    set_angle(TILT_CHANNEL, 90)
    current_tilt = 90

    print("\n[수동 제어 모드]")
    print("a: 왼쪽 | d: 오른쪽 | w: 위로 | s: 아래로 | c: 중앙 복귀 | q: 종료")
    
    # 3. 간단한 키보드 입력 인터랙션 Loop
    step = 5  # 한 번 입력할 때 움직일 각도 크기

    try:
        while True:
            cmd = input("명령 입력 (a/d/w/s/c/q): ").strip().lower()
            
            if cmd == 'q':
                print("제어를 종료합니다.")
                break
            elif cmd == 'a':  # Left
                current_pan = set_angle(PAN_CHANNEL, current_pan + step)
            elif cmd == 'd':  # Right
                current_pan = set_angle(PAN_CHANNEL, current_pan - step)
            elif cmd == 'w':  # Up
                current_tilt = set_angle(TILT_CHANNEL, current_tilt - step)
            elif cmd == 's':  # Down
                current_tilt = set_angle(TILT_CHANNEL, current_tilt + step)
            elif cmd == 'c':  # Center
                current_pan = set_angle(PAN_CHANNEL, 90)
                current_tilt = set_angle(TILT_CHANNEL, 90)
            
            print(f"현재 각도 -> Pan(좌우): {current_pan}°, Tilt(상하): {current_tilt}°")
    except KeyboardInterrupt:
        print("\n강제 종료되었습니다.")    
    finally:
        # 종료 시 중앙 정렬
        set_angle(PAN_CHANNEL, 90)
        set_angle(TILT_CHANNEL, 90)
if __name__ == "__main__":
    main()