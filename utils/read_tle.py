# 텍스트 파일에서 TLE 정보를 읽어오는 함수
def read_tle_file(file_path):
    tle_data = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 두 줄씩 읽어와서 TLE 정보를 추출하여 리스트에 추가
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        
        tle_data.append((name, line1, line2))
    
        # 읽어온 TLE 정보 출력 (테스트용)
    for name, line1, line2 in tle_data:
        print(f'Name: {name}')
        print(f'Line 1: {line1}')
        print(f'Line 2: {line2}')
        print()
        
    return tle_data

