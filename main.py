def input_3x3_matrix(prompt):
    print(prompt)
    matrix = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"{i+1} / 3> ").strip().split()))
                if len(row) != 3:
                    raise ValueError("3개의 숫자를 입력해야 합니다.")
                matrix.append(row)
                break
            except ValueError as e:
                print(f"잘못된 입력입니다: {e}. 다시 시도해주세요.")
    return matrix

def mac_operation(filter_a, pattern):
    raise NotImplementedError

def user_input():
    print("# " + "-" * 30)
    print("# [1] 필터 입력")
    print("# " + "-" * 30)
    filter_a = input_3x3_matrix("필터 A (3개씩의 숫자를 공백으로 구분하여 3줄 입력)")
    filter_b = input_3x3_matrix("필터 B (3개씩의 숫자를 공백으로 구분하여 3줄 입력)")

    print("# " + "-" * 30)
    print("# [2] 패턴 입력")
    print("# " + "-" * 30)
    pattern = input_3x3_matrix("패턴 (3개씩의 숫자를 공백으로 구분하여 3줄 입력)")

    point_a, point_b, repeats, elapsed_time = mac_operation(filter_a, pattern)
    print("# " + "-" * 30)
    print(f"# [3] MAC 결과 {"" if abs(point_a - point_b) > 1e-9 and point_b > point_a else '판정 불가'}")
    print("# " + "-" * 30)
    print(f"A 점수: {point_a}")
    print(f"B 점수: {point_b}")
    print(f"연산 시간(평균/{repeats}회): {elapsed_time:.3f} ms")
    print(f"판정: {'A' if abs(point_a - point_b) > 1e-9 and point_a > point_b else 'B' if abs(point_a - point_b) > 1e-9 and point_b > point_a else '판정 불가 (|A-B| < 1e-9)'}")

    print("# " + "-" * 30)

    print(f"# [3] MAC 결과 ")

    print("# " + "-" * 30)

    print(f"A 점수: {point_a}")
    print(f"B 점수: {point_b}")
    print(f"판정: {'A' if abs(point_a - point_b) > 1e-9 and point_a > point_b else 'B' if abs(point_a - point_b) > 1e-9 and point_b > point_a else '판정 불가 (|A-B| < 1e-9)'}")

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
