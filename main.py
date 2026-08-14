"""Mini NPU Simulator — Codyssey Mission 3.

입력 패턴과 필터를 위치별로 곱해 누적(MAC)한 점수로
Cross/X 패턴을 판정하고, 크기별 연산 시간을 측정한다.
표준 라이브러리(json, os, time)만 사용한다.
"""
import json
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data.json')

EPSILON = 1e-9
REPEATS = 10
MIN_SIZE = 3
MAX_SIZE = 25

CROSS = 'Cross'
X = 'X'
UNDECIDED = 'UNDECIDED'
TIE_MESSAGE = '판정 불가 (|A-B| < 1e-9)'
LABEL_MAP = {'+': CROSS, 'cross': CROSS, 'x': X}


def print_header(title):
    """구간 제목을 예시 형식(# --- / # 제목 / # ---)으로 출력한다."""
    print('# ' + '-' * 39)
    print(f'# {title}')
    print('# ' + '-' * 39)


def print_matrix(title, matrix):
    """행렬을 제목과 함께 행 단위로 출력한다(저장 확인용)."""
    print(f'{title}:')
    for row in matrix:
        print('  ' + ' '.join(f'{value:g}' for value in row))


def input_3x3_matrix(prompt):
    """3×3 행렬을 한 줄씩 입력받아 float 행렬로 반환한다.

    행 개수/숫자 파싱 오류 시 안내 후 해당 행을 재입력받는다.
    """
    print(prompt)
    matrix = []
    for i in range(3):
        while True:
            raw = input(f'{i + 1} / 3 > ').strip()
            try:
                row = [float(value) for value in raw.split()]
            except ValueError:
                print('입력 형식 오류: 숫자만 공백으로 구분해 입력하세요.')
                continue
            if len(row) != 3:
                print('입력 형식 오류: 각 줄에 3개의 숫자를 '
                      '공백으로 구분해 입력하세요.')
                continue
            matrix.append(row)
            break
    return matrix


def normalize_label(value):
    """원본 라벨('+', 'x', 'cross' 등)을 표준 라벨(Cross/X)로 변환한다."""
    key = str(value).strip().lower()
    if key not in LABEL_MAP:
        raise ValueError(f'알 수 없는 라벨: {value!r}')
    return LABEL_MAP[key]


def validate_size(matrix, size):
    """행렬이 size×size인지 검증한다. 불일치 시 ValueError."""
    if (not isinstance(matrix, list) or len(matrix) != size
            or any(not isinstance(row, list) or len(row) != size
                   for row in matrix)):
        raise ValueError(f'크기 불일치: {size}×{size} 행렬이 아닙니다')


def mac(pattern, filter_matrix):
    """위치별 곱을 누적(MAC)한 점수를 반환한다."""
    total = 0.0
    for row_p, row_f in zip(pattern, filter_matrix):
        for p_val, f_val in zip(row_p, row_f):
            total += p_val * f_val
    return total


def decide(score_a, score_b, label_a, label_b, tie_label=UNDECIDED):
    """허용오차(EPSILON) 정책으로 두 점수를 비교해 판정 라벨을 반환한다."""
    if abs(score_a - score_b) < EPSILON:
        return tie_label
    return label_a if score_a > score_b else label_b


def flatten(matrix):
    """2차원 행렬을 1차원 리스트로 펼친다(보너스: 메모리 접근 최적화)."""
    return [value for row in matrix for value in row]


def mac_flat(flat_pattern, flat_filter):
    """1차원으로 펼친 배열 기준 MAC 점수를 반환한다(보너스)."""
    total = 0.0
    for index in range(len(flat_pattern)):
        total += flat_pattern[index] * flat_filter[index]
    return total


def measure_mac_ms(pattern, filter_matrix, repeats=REPEATS):
    """2차원 MAC 1회 평균 시간(ms)을 repeats회 반복 측정으로 구한다."""
    start = time.perf_counter()
    for _ in range(repeats):
        mac(pattern, filter_matrix)
    return (time.perf_counter() - start) * 1000 / repeats


def measure_mac_flat_ms(pattern, filter_matrix, repeats=REPEATS):
    """1차원 MAC 1회 평균 시간(ms)을 측정한다. 변환은 측정에서 제외."""
    flat_pattern = flatten(pattern)
    flat_filter = flatten(filter_matrix)
    start = time.perf_counter()
    for _ in range(repeats):
        mac_flat(flat_pattern, flat_filter)
    return (time.perf_counter() - start) * 1000 / repeats


def create_cross(size):
    """가운데 행/열이 1인 size×size 십자가 패턴을 생성한다."""
    center = size // 2
    return [[1 if i == center or j == center else 0
             for j in range(size)]
            for i in range(size)]


def create_x(size):
    """두 대각선이 1인 size×size X 패턴을 생성한다."""
    return [[1 if i == j or i + j == size - 1 else 0
             for j in range(size)]
            for i in range(size)]


def user_input():
    """모드 1: 3×3 필터/패턴 입력 → 저장 확인 → 판정 → 성능 분석."""
    print_header('[1] 필터 입력')
    filter_a = input_3x3_matrix('필터 A (3줄 입력, 공백 구분)')
    print_matrix('필터 A 저장 확인', filter_a)
    filter_b = input_3x3_matrix('필터 B (3줄 입력, 공백 구분)')
    print_matrix('필터 B 저장 확인', filter_b)

    print_header('[2] 패턴 입력')
    pattern = input_3x3_matrix('패턴 (3줄 입력, 공백 구분)')
    print_matrix('패턴 저장 확인', pattern)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    verdict = decide(score_a, score_b, 'A', 'B', TIE_MESSAGE)
    elapsed = (measure_mac_ms(pattern, filter_a)
               + measure_mac_ms(pattern, filter_b)) / 2

    suffix = ' (판정 불가)' if verdict == TIE_MESSAGE else ''
    print_header('[3] MAC 결과' + suffix)
    print(f'A 점수: {score_a}')
    print(f'B 점수: {score_b}')
    print(f'연산 시간(평균/{REPEATS}회): {elapsed:.3f} ms')
    print(f'판정: {verdict}')

    print_header(f'[4] 성능 분석 (3×3, 평균/{REPEATS}회)')
    time_2d = measure_mac_ms(pattern, filter_a)
    time_flat = measure_mac_flat_ms(pattern, filter_a)
    print(f'3×3 | 2차원: {time_2d:.3f} ms | 1차원: {time_flat:.3f} ms'
          f' | 연산 횟수: 9')


def parse_filter_key(key):
    """필터 키 'size_5' → 5. 형식이 다르면 ValueError."""
    parts = key.split('_')
    if len(parts) != 2 or parts[0] != 'size':
        raise ValueError(f'필터 키 형식 오류: {key}')
    return int(parts[1])


def parse_pattern_key(key):
    """패턴 키 'size_13_2' → (13, 2). 형식이 다르면 ValueError."""
    parts = key.split('_')
    if len(parts) != 3 or parts[0] != 'size':
        raise ValueError(f'패턴 키 형식 오류: {key}')
    return int(parts[1]), int(parts[2])


def filter_sort_key(key):
    """필터 키를 크기 숫자 기준으로 정렬하기 위한 키."""
    try:
        return (0, parse_filter_key(key), key)
    except ValueError:
        return (1, 0, key)


def pattern_sort_key(key):
    """패턴 키를 (크기, 번호) 기준으로 정렬하기 위한 키."""
    try:
        size, index = parse_pattern_key(key)
        return (0, size, index, key)
    except ValueError:
        return (1, 0, 0, key)


def load_data():
    """data.json을 읽어 dict로 반환한다. 실패 시 사유 출력 후 None."""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        print(f'데이터 파일을 찾을 수 없습니다: {DATA_PATH}')
    except json.JSONDecodeError as exc:
        print(f'data.json 형식 오류: {exc}')
    except OSError as exc:
        print(f'data.json 읽기 실패: {exc}')
    return None


def load_filters(filters):
    """필터 키를 정규화해 {크기: {Cross: 행렬, X: 행렬}}로 반환한다.

    항목별로 검증하며, 실패한 항목은 사유를 출력하고 건너뛴다.
    """
    loaded = {}
    for key in sorted(filters, key=filter_sort_key):
        try:
            size = parse_filter_key(key)
            filter_set = {}
            for label, matrix in filters[key].items():
                filter_set[normalize_label(label)] = matrix
            for label in (CROSS, X):
                if label not in filter_set:
                    raise ValueError(f'{label} 필터 누락')
                validate_size(filter_set[label], size)
            loaded[size] = filter_set
            print(f'✓ {key:<7} 필터 로드 완료 (Cross, X)')
        except Exception as exc:
            print(f'✗ {key:<7} 필터 로드 실패: {exc}')
    return loaded


def evaluate_case(key, case, loaded_filters):
    """패턴 케이스 1건을 판정한다. 오류는 케이스 단위 FAIL로 격리한다."""
    result = {'key': key, 'passed': False, 'reason': None,
              'cross': None, 'x': None, 'verdict': None, 'expected': None}
    try:
        size, _ = parse_pattern_key(key)
        filter_set = loaded_filters.get(size)
        if filter_set is None:
            raise ValueError(f'size_{size} 필터가 로드되지 않았습니다')
        expected = normalize_label(case.get('expected'))
        pattern = case.get('input')
        validate_size(pattern, size)
        cross_score = mac(pattern, filter_set[CROSS])
        x_score = mac(pattern, filter_set[X])
        verdict = decide(cross_score, x_score, CROSS, X)
        result.update(cross=cross_score, x=x_score,
                      verdict=verdict, expected=expected)
        if verdict == expected:
            result['passed'] = True
        elif verdict == UNDECIDED:
            result['reason'] = '동점(UNDECIDED) 처리 규칙에 따라 FAIL'
        else:
            result['reason'] = f'판정 {verdict} ≠ expected {expected}'
    except Exception as exc:
        result['reason'] = f'{type(exc).__name__}: {exc}'
    return result


def print_case(result):
    """케이스 1건의 점수/판정/PASS-FAIL을 출력한다."""
    print(f"--- {result['key']} ---")
    if result['verdict'] is None:
        print(f"판정: FAIL | 사유: {result['reason']}")
        return
    print(f"Cross 점수: {result['cross']}")
    print(f"X 점수: {result['x']}")
    status = 'PASS' if result['passed'] else 'FAIL'
    print(f"판정: {result['verdict']} | "
          f"expected: {result['expected']} | {status}")


def print_performance(loaded_filters):
    """3×3(생성) + 로드된 크기별 MAC 시간을 2차원/1차원 표로 출력한다."""
    targets = [(3, create_cross(3))]
    targets += [(size, loaded_filters[size][CROSS])
                for size in sorted(loaded_filters) if size != 3]
    rows = [(size,
             measure_mac_ms(cross, cross),
             measure_mac_flat_ms(cross, cross))
            for size, cross in targets]

    for title, column in (('2차원 배열', 1), ('1차원 최적화 (보너스)', 2)):
        print(f'[{title}]')
        print(f"{'크기':>6}{'평균 시간(ms)':>13}{'연산 횟수':>9}")
        print('-' * 38)
        for row in rows:
            size = row[0]
            print(f"{f'{size}×{size}':>8}{row[column]:>16.3f}"
                  f"{size * size:>12}")
        print()


def print_summary(results):
    """총/통과/실패 건수와 실패 케이스 목록(사유 포함)을 출력한다."""
    total = len(results)
    passed = sum(1 for result in results if result['passed'])
    print(f'총 테스트: {total}개')
    print(f'통과: {passed}개')
    print(f'실패: {total - passed}개')
    failures = [result for result in results if not result['passed']]
    if failures:
        print()
        print('실패 케이스:')
        for result in failures:
            print(f"- {result['key']}: {result['reason']}")


def analyze_json():
    """모드 2: data.json 로드 → 케이스 판정 → 성능 분석 → 결과 요약."""
    data = load_data()
    if data is None:
        return

    print_header('[1] 필터 로드')
    loaded = load_filters(data.get('filters') or {})

    print_header('[2] 패턴 분석 (라벨 정규화 적용)')
    patterns = data.get('patterns') or {}
    if not patterns:
        print('분석할 패턴이 없습니다.')
    results = []
    for key in sorted(patterns, key=pattern_sort_key):
        result = evaluate_case(key, patterns[key], loaded)
        results.append(result)
        print_case(result)

    print_header(f'[3] 성능 분석 (평균/{REPEATS}회)')
    print_performance(loaded)

    print_header('[4] 결과 요약')
    print_summary(results)


def input_pattern_size():
    """패턴 생성 크기 N을 입력받는다. 범위 밖이면 재입력을 유도한다."""
    while True:
        raw = input(f'생성할 크기 N (홀수 권장, {MIN_SIZE}~{MAX_SIZE}): ')
        try:
            size = int(raw.strip())
        except ValueError:
            print('입력 형식 오류: 정수를 입력하세요.')
            continue
        if not MIN_SIZE <= size <= MAX_SIZE:
            print(f'입력 형식 오류: {MIN_SIZE}~{MAX_SIZE} 범위로 입력하세요.')
            continue
        return size


def generate_patterns():
    """모드 3(보너스): N×N Cross/X 패턴을 생성하고 자체 검증한다."""
    print_header('[보너스] 패턴 생성기')
    size = input_pattern_size()
    cross = create_cross(size)
    x_pattern = create_x(size)
    print_matrix(f'Cross 패턴 ({size}×{size})', cross)
    print_matrix(f'X 패턴 ({size}×{size})', x_pattern)

    for name, pattern in ((CROSS, cross), (X, x_pattern)):
        verdict = decide(mac(pattern, cross), mac(pattern, x_pattern),
                         CROSS, X)
        status = 'PASS' if verdict == name else 'FAIL'
        print(f'검증: {name} 패턴 → 판정: {verdict} | {status}')

    elapsed = measure_mac_ms(cross, cross)
    print(f'성능: {size}×{size} 평균 {elapsed:.3f} ms '
          f'(연산 횟수 {size * size}, {REPEATS}회 평균)')


def main():
    """모드 선택 메뉴를 반복 출력하고 각 모드를 실행한다."""
    while True:
        print('\n' + '=' * 50)
        print('=== Mini NPU Simulator ===')
        print('-' * 20)
        print('[모드 선택]')
        print('-' * 20)
        print('1. 사용자 입력(3x3)')
        print('2. data.json 분석')
        print('3. 패턴 생성기')
        print('Q. 종료')
        choice = input('선택: ').strip()
        print()
        if choice == '1':
            user_input()
        elif choice == '2':
            analyze_json()
        elif choice == '3':
            generate_patterns()
        elif choice.upper() == 'Q':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 선택입니다. 1~3 또는 Q를 입력해주세요.')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\n프로그램을 종료합니다.')
