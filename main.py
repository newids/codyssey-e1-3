
def user_input():
    raise NotImplementedError

def generate_patterns():
    raise NotImplementedError

def analyze_json():
    raise NotImplementedError

def main(self):
    while True:
        print("=== Mini NPU Simulator ===")
        print("[모드 선택]")
        print("-"* 30)
        print("1. 사용자 입력(3x3)")
        print("2. data.json 분석")
        print("3. 패턴 생성기")
        print("Q. 종료")
        choice = input("선택: ")
        if choice == "1":
            user_input()
        elif choice == "2":
            analyze_json()
        elif choice == "3":
            generate_patterns()
        elif choice.upper() == "Q":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1-3 사이의 숫자 또는 'Q'를 입력해주세요.")
