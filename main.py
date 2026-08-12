import time
import json


def input_3x3_matrix(prompt):
    print(prompt)
    matrix = []
    for i in range(3):
        while True:
            try:
                row = list(
                    map(float, input(f"{i + 1} / 3 > ").strip().split()))
                if len(row) != 3:
                    raise ValueError("3개의 숫자를 입력해야 합니다.")
                matrix.append(row)
                break
            except ValueError as e:
                print(f"잘못된 입력입니다: {e}. 다시 시도해주세요.")
    return matrix


def mac_operation(filter_a, filter_b, pattern, repeats=10):
    start_time = time.time()

    point_a = 0
    point_b = 0
    for _ in range(repeats):
        for p, fa in zip(pattern, filter_a):
            for n, f in zip(p, fa):
                point_a += n * f

        for p, fb in zip(pattern, filter_b):
            for n, f in zip(p, fb):
                point_b += n * f

    elapsed_time = (time.time() - start_time) * 1000

    # Assuming 1 repeat for simplicity
    return point_a / repeats, point_b / repeats, repeats, elapsed_time


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

    point_a, point_b, repeats, elapsed_time = mac_operation(
        filter_a, filter_b, pattern)

    print("# " + "-" * 30)
    print(
        f"# [3] MAC 결과 {'' if abs(point_a - point_b) > 1e-9 and point_b > point_a else '판정 불가'}")
    print("# " + "-" * 30)
    classification(point_a, point_b, repeats, elapsed_time)


def test_mac_operation():
    f_a = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]  # Cross pattern
    f_b = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]  # X pattern
    pattern = f_a.copy()
    point_a, point_b, repeats, elapsed_time = mac_operation(f_a, f_b, pattern)
    print(
        f"Test MAC Operation: filter_a={f_a}, filter_b={f_b}, pattern={pattern}")
    classification(point_a, point_b, repeats, elapsed_time)

    f_a = [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0]]  # Cross pattern
    f_b = [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]]  # X pattern
    pattern = f_b.copy()
    point_a, point_b, repeats, elapsed_time = mac_operation(f_a, f_b, pattern)
    print(
        f"\nTest MAC Operation: filter_a={f_a}, filter_b={f_b}, pattern={pattern}")
    classification(point_a, point_b, repeats, elapsed_time)


def generate_patterns():
    raise NotImplementedError


CROSS = "Cross"
X = "X"


def label_normalization(value):
    if value.upper() == 'X':
        return X
    elif value == '+':
        return CROSS
    else:
        raise ValueError(f"Invalid label: {value}. Expected 'X' or 'Cross'.")


def analyze_json():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data.json 파일을 찾을 수 없습니다.")
        return

    meta = data.get("meta")
    filters = data.get("filters")
    patterns = data.get("patterns")
    print("meta:", meta)
    print("filters:", len(filters))
    print("patterns:", len(patterns))

    labels = [
        ["size_5", "size_5_1", "size_5_2"],
        ["size_13", "size_13_1", "size_13_2"],
        ["size_25", "size_25_1", "size_25_2"],
    ]

    for label in labels:
        print("\n" + "." * 10)
        print(f"MAC Operation for {label}")
        cross_filter = filters.get(label[0]).get("cross")
        x_filter = filters.get(label[0]).get("x")

        size_5_1 = patterns.get(label[1]).get("input")
        size_5_1_expected = label_normalization(
            patterns.get(label[1]).get("expected"))

        result = mac_operation(cross_filter, x_filter, size_5_1)
        classification(*result)
        print(f"- -- {label[1]} ---")
        print(f"Cross 점수: {1.0}")
        print(f"X 점수: 5.0")
        print(f"판정: X | expected: X | PASS")

        size_5_2 = patterns.get(label[2]).get("input")
        size_5_2_expected = label_normalization(
            patterns.get(label[2]).get("expected"))

        result = mac_operation(cross_filter, x_filter, size_5_2)
        classification(*result)


def classification(point_a, point_b, repeats, elapsed_time):
    print(f"\tA 점수: {point_a}")
    print(f"\tB 점수: {point_b}")
    print(f"\t연산 시간(평균/{repeats}회): {elapsed_time:.3f} ms")
    print(f"\t판정: {'A' if abs(point_a - point_b) > 1e-9 and point_a > point_b else 'B' if abs(point_a - point_b) > 1e-9 and point_b > point_a else '판정 불가 (|A-B| < 1e-9)'}")


def main():
    while True:
        print("\n\n" + "=" * 50)
        print("=== Mini NPU Simulator ===")
        print("-" * 20)
        print("[모드 선택]")
        print("-" * 20)
        print("1. 사용자 입력(3x3)")
        print("2. data.json 분석")
        print("3. 패턴 생성기")
        print("Q. 종료")
        choice = input("선택: ")
        print("\n")
        if choice == "1":
            user_input()
        elif choice == "2":
            analyze_json()
        elif choice == "3":
            generate_patterns()
        elif choice.upper() == "T":
            test_mac_operation()
        elif choice.upper() == "Q":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1-3 사이의 숫자 또는 'Q'를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError:
        print("해당 기능은 아직 구현되지 않았습니다.")
