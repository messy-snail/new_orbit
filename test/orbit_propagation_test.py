import numpy as np
from datetime import datetime, timedelta
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import folium

# KOMPSAT-3A의 TLE 데이터
line1 = "1 39084U 13009A   14295.08419791  .00002106  00000-0  11606-3 0  8652"
line2 = "2 39084  98.4658  99.7431 0009826  55.6672 304.5680 14.57121619115303"

# TLE 데이터로부터 위성 객체 생성
satellite = twoline2rv(line1, line2, wgs84)

# 초기 조건 설정
initial_time = datetime(2023, 10, 25, 0, 0, 0)
final_time = initial_time + timedelta(days=1)  # 원하는 시간 범위 설정
time_step = timedelta(minutes=10)  # 시간 간격 설정

# Folium 지도 생성
m = folium.Map(location=[0, 0], zoom_start=2)  # 초기 지도 설정

# 궤도 좌표 저장 리스트
orbit_coordinates = []

current_time = initial_time
while current_time <= final_time:
    # 궤도 전파
    position, _ = satellite.propagate(
        current_time.year, current_time.month, current_time.day,
        current_time.hour, current_time.minute, current_time.second
    )
    
    # 고도 계산
    altitude = np.linalg.norm(position) - 6371000  # 지구 반지름을 빼줌 (고도 계산)
    
    # ECI 좌표를 ECEF 좌표로 변환
    eci_to_ecef = np.array([[0, 1, 0],
                            [-1, 0, 0],
                            [0, 0, 1]])
    ecef_position = np.dot(eci_to_ecef, position)
    
    # ECEF 좌표를 위도와 경도로 변환
    phi = np.arctan2(ecef_position[2], np.sqrt(ecef_position[0]**2 + ecef_position[1]**2))
    lambda_ = np.arctan2(ecef_position[1], ecef_position[0])
    
    # 위도와 경도를 도 단위로 변환
    lat = np.degrees(phi)
    lon = np.degrees(lambda_)
    
    # 궤도 좌표를 저장
    orbit_coordinates.append([lat, lon])

    current_time += time_step

# 궤도를 선으로 그리기
folium.PolyLine(locations=orbit_coordinates, color='red').add_to(m)

# 지도를 HTML 파일로 저장
m.save('orbit_map.html')
