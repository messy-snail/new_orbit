import requests

def download_tle(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_tle_data(tle_data, search_queries):
    tle_lines = tle_data.split('\n')
    selected_tle = []

    for search_query in search_queries:
        for i in range(0, len(tle_lines), 3):
            if search_query.isnumeric():
                # NORAD 번호로 검색
                if search_query.zfill(5) == tle_lines[i + 1][2:7]:
                    selected_tle.append(tle_lines[i] + '\n' + tle_lines[i + 1] + '\n' + tle_lines[i + 2])
                    break
            else:
                # 위성 이름으로 검색
                if search_query.upper() in tle_lines[i].upper():
                    selected_tle.append(tle_lines[i] + '\n' + tle_lines[i + 1] + '\n' + tle_lines[i + 2])
                    break

    return '\n'.join(selected_tle)

# 사용자로부터 위성 이름 또는 NORAD 카탈로그 번호 입력받기 (쉼표로 구분)
input_query = input("Enter the satellite names or NORAD catalog numbers, separated by commas: ")
search_queries = [query.strip() for query in input_query.split(',')]

# Celestrak의 TLE 데이터 URL
url = 'http://celestrak.com/NORAD/elements/active.txt'

# TLE 데이터 다운로드
all_tle_data = download_tle(url)

# 검색 질의에 따른 TLE 데이터 추출
selected_tle_data = extract_tle_data(all_tle_data, search_queries)

# 결과 출력 또는 파일로 저장
print(selected_tle_data)

# 필요한 경우 파일로 저장할 수 있습니다.
with open('../input_data/selected_satellites_tle.txt', 'w') as file:
    file.write(selected_tle_data)
