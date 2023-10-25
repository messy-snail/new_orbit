import read_tle
import folium
from skyfield.api import load, Topos, EarthSatellite
from datetime import datetime, timedelta
from tqdm import tqdm

tle_data = read_tle.read_tle_file('tle_list.txt')


# TLE 데이터를 위성 객체로 변환
ts = load.timescale()
satellites = []

for name, tle_line1, tle_line2 in tle_data:
    satellite = EarthSatellite(tle_line1, tle_line2, name, ts)
    satellites.append((satellite, name))  # 위성 객체와 이름을 튜플로 저장

# 시작 날짜와 끝 날짜 설정 (예시로 1일치 궤도를 전파)
original_start_date = ts.utc(2022, 10, 21)
end_date = original_start_date + timedelta(days=1)
time_step = timedelta(minutes=1)

# 지도 초기화
m = folium.Map(location=[38.921389, -77.065556], zoom_start=5)

colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'purple', 'orange', 'brown']  # 원하는 색상 리스트를 추가
color_index = 0  # 색상 인덱스 초기화

# 궤도 계산 및 지도에 그리기
for i, (satellite, name) in enumerate(tqdm(satellites)):
    lats, lons = [], []
    line_color = colors[color_index]
    color_index = (color_index + 1) % len(colors)  # 다음 색상으로 순환
    
    start_date = original_start_date
    while start_date.tt < end_date.tt:        
        topocentric = satellite.at(start_date).subpoint()
        lat, lon = topocentric.latitude.degrees, topocentric.longitude.degrees  # degrees 속성 사용
        if lons and abs(lon - lons[-1]) > 180:
            # 경도가 180에서 -180으로 바뀌면 선이 이어지지 않도록 중단
            coordinates = list(zip(lats, lons))  
            folium.PolyLine(
                locations=coordinates,
                color=line_color,
                fill=True,
                ).add_to(m)
            lats, lons = [],[]

        lats.append(lat)
        lons.append(lon)    
        start_date += time_step
    coordinates = list(zip(lats, lons))  
    folium.PolyLine(
        locations=coordinates,
        color=line_color,
        fill=True,
    ).add_to(m)        

# 지도 저장
m.save('orbit_map.html')
