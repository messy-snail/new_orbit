from tqdm import tqdm
import time

# 반복할 작업의 범위를 설정
total = 100

# tqdm으로 루프를 래핑
for i in tqdm(range(total)):
    # 작업 수행
    time.sleep(0.1)  # 예시로 작업 지연 시간을 추가
