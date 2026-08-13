import random
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


def mac(patt, filt):
    point = 0
    for i in range(len(patt)):
        row_p = patt[i]
        row_f = filt[i]
        for j in range(len(row_p)):
            point += float(row_p[j]) * float(row_f[j])
    return point


def mac_operation(filter_a, filter_b, pattern, repeats=1):
    start_time = time.perf_counter()

    point_a = 0
    point_b = 0
    for _ in range(repeats):
        # for p, fa in zip(pattern, filter_a):
        #     for n, f in zip(p, fa):
        #         point_a += n * f

        # for p, fb in zip(pattern, filter_b):
        #     for n, f in zip(p, fb):
        #         point_b += n * f
        point_a += mac(pattern, filter_a)
        point_b += mac(pattern, filter_b)

    elapsed_time = (time.perf_counter() - start_time) * 1000

    # Assuming 1 repeat for simplicity
    return point_a / repeats, point_b / repeats, repeats, elapsed_time


def mac_flat(patt, filt):
    point = 0
    for i in range(len(patt)):
        row_p = patt[i]
        row_f = filt[i]
        for j in range(len(row_p)):
            point += float(row_p[j]) * float(row_f[j])
    return point


def mac_operation_flat(filter_a, filter_b, pattern, repeats=1):
    filter_a_flat = map(filter_a)
    filter_b_flat = map(filter_b)
    pattern_flat = map(pattern)

    start_time = time.perf_counter()

    point_a = 0
    point_b = 0
    for _ in range(repeats):
        for k in len(pattern_flat):
            point_a += float(pattern_flat[k]) * float(filter_a_flat[k])
        for k in len(pattern_flat):
            point_b += float(pattern_flat[k]) * float(filter_b_flat[k])

    elapsed_time = (time.perf_counter() - start_time) * 1000

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
        f"# [3] MAC 결과 {'' if abs(point_a - point_b) > EPSILON and point_b > point_a else '판정 불가'}")
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
    print("# " + "-" * 30)
    print("# [보너스] 패턴 생성기")
    while True:
        raw = input("생성할 크기 N (홀수 권장, 3~25): ").strip()
        try:
            n = int(raw)
        except ValueError:
            print("입력 형식 오류: 정수를 입력하세요.")
            continue
        if n < 3:
            print("입력 형식 오류: 3 이상의 크기를 입력하세요.")
            continue
        break

    cross_pattern = create_cross()
    x_pattern = create_x()

    pattern = cross_pattern.copy()
    point_a, point_b, repeats, elapsed_time = mac_operation(
        cross_pattern, x_pattern, pattern)


def create_cross(size):
    center = size // 2
    cross = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if abs(i - center) == abs(j - center):
                cross[i][j] = 1
    return cross


def create_x(size):
    x_pattern = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if abs(i - j) == 1:
                x_pattern[i][j] = 1
    return x_pattern


CROSS = "Cross"
X = "X"


def label_normalization(value):
    if value.upper() == 'X':
        return X
    elif value == '+' or value.upper() == 'CROSS':
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
    print("✓ size_5  필터 로드 완료 (Cross, X)")
    print("✓ size_13 필터 로드 완료 (Cross, X)")
    print("✓ size_25 필터 로드 완료 (Cross, X)")

    LABELS = [5, 13, 25]

    for label in LABELS:
        print("\n" + "." * 10)
        print(f"MAC Operation for {f'size_{label}'}")
        cross_filter = filters.get(f'size_{label}').get("cross")
        x_filter = filters.get(f'size_{label}').get("x")

        pattern_1 = patterns.get(f'size_{label}_1').get("input")
        pattern_1_expected = label_normalization(
            patterns.get(f'size_{label}_1').get("expected"))

        result = mac_operation(cross_filter, x_filter, pattern_1)
        classification_x_cross(
            f'size_{label}_1', result[0], result[1], pattern_1_expected)
        e_time_1 = result[3]

        pattern_2 = patterns.get(f'size_{label}_2').get("input")
        pattern_2_expected = label_normalization(
            patterns.get(f'size_{label}_2').get("expected"))

        result = mac_operation(cross_filter, x_filter, pattern_2)
        classification_x_cross(
            f'size_{label}_2', result[0], result[1], pattern_2_expected)
        e_time_2 = result[3]

    # point_a / repeats, point_b / repeats, repeats, elapsed_time
    print(f"#---------------------------------------")
    print(f"# [3] 성능 분석 (평균/10회)")
    print(f"#---------------------------------------")
    print(f"\t크기\t평균 시간(ms)\t연산 횟수")
    print(f"-------------------------------------")

    REPEATS = 10
    average_times = []

    ## 3x3
    cross_filter = create_cross(3)
    x_filter = create_x(3)
    pattern_1 = cross_filter.copy()
    result = mac_operation(cross_filter, x_filter, pattern_1, REPEATS)
    e_time_1 = result[3]
    pattern_2 = x_filter.copy()
    result = mac_operation(cross_filter, x_filter, pattern_2)
    e_time_2 = result[3]

    average_times.append((e_time_1 + e_time_2) / 2)

    for label in LABELS:
        cross_filter = filters.get(f'size_{label}').get("cross")
        x_filter = filters.get(f'size_{label}').get("x")

        pattern_1 = patterns.get(f'size_{label}_1').get("input")
        pattern_1_expected = label_normalization(
            patterns.get(f'size_{label}_1').get("expected"))

        result = mac_operation(cross_filter, x_filter, pattern_1, REPEATS)
        e_time_1 = result[3]

        pattern_2 = patterns.get(f'size_{label}_2').get("input")
        pattern_2_expected = label_normalization(
            patterns.get(f'size_{label}_2').get("expected"))

        result = mac_operation(cross_filter, x_filter, pattern_2)
        e_time_2 = result[3]

        average_times.append((e_time_1 + e_time_2) / 2)

    for idx, n in zip(range(4), [3] + LABELS):
        print(f"\t{n}×{n}\t\t{average_times[idx]:.3f}\t\t{n ** 2}")

    # 3×3        0.010             9
    # 5×5        0.031            25
    # 13×13      0.187           169
    # 25×25      0.682           625

    ## flat_mac_operation
    ## 3x3
    cross_filter = create_cross(3)
    x_filter = create_x(3)
    pattern_1 = cross_filter.copy()
    result = mac_operation_flat(cross_filter, x_filter, pattern_1, REPEATS)
    e_time_1 = result[3]
    pattern_2 = x_filter.copy()
    result = mac_operation_flat(cross_filter, x_filter, pattern_2)
    e_time_2 = result[3]

    average_times.append((e_time_1 + e_time_2) / 2)

    for label in LABELS:
        cross_filter = filters.get(f'size_{label}').get("cross")
        x_filter = filters.get(f'size_{label}').get("x")

        pattern_1 = patterns.get(f'size_{label}_1').get("input")
        pattern_1_expected = label_normalization(
            patterns.get(f'size_{label}_1').get("expected"))

        result = mac_operation_flat(cross_filter, x_filter, pattern_1, REPEATS)
        e_time_1 = result[3]

        pattern_2 = patterns.get(f'size_{label}_2').get("input")
        pattern_2_expected = label_normalization(
            patterns.get(f'size_{label}_2').get("expected"))

        result = mac_operation_flat(cross_filter, x_filter, pattern_2)
        e_time_2 = result[3]

        average_times.append((e_time_1 + e_time_2) / 2)

    for idx, n in zip(range(4), [3] + LABELS):
        print(f"\t{n}×{n}\t\t{average_times[idx]:.3f}\t\t{n ** 2}")


EPSILON = 1e-9


def classification_x_cross(label, p0, p1, expected):
    print(f"- -- {label} ---")
    print(f"Cross 점수: {p0}")
    print(f"X 점수: {p1}")
    cross_or_x = CROSS if abs(p0 - p1) > EPSILON and p0 > p1 \
        else X if abs(p0 - p1) > EPSILON and p1 > p0 \
        else 'UNDECIDED'
    is_pass = "PASS" if expected == cross_or_x else "FAIL"
    print(f"판정: {cross_or_x} | expected : {expected} | {is_pass}")
    print("-" * 10)


def classification(point_a, point_b, repeats, elapsed_time):
    print(f"\tA 점수: {point_a}")
    print(f"\tB 점수: {point_b}")
    print(f"\t연산 시간(평균/{repeats}회): {elapsed_time:.3f} ms")
    print(f"\t판정: {'A' if abs(point_a - point_b) > EPSILON and point_a > point_b
                   else 'B' if abs(point_a - point_b) > EPSILON and point_b > point_a
                   else '판정 불가 (|A-B| < 1e-9)'}")


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
