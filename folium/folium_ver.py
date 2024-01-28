import folium
from skyfield.api import load, Topos, EarthSatellite
from datetime import datetime, timedelta

#ARIRANG-3 (KOMPSAT-3)   
tle_line1 ='1 38338U 12025B   23297.62525709  .00000910  00000+0  19013-3 0  9990'
tle_line2 = '2 38338  98.2322 239.1614 0008989 258.8215 101.1975 14.62228630610087'

# TLE 데이터를 위성 객체로 변환
ts = load.timescale()
satellite = EarthSatellite(tle_line1, tle_line2, 'KOMPSAT-3A', ts)

# 시작 날짜와 끝 날짜 설정 (예시로 1일치 궤도를 전파)
start_date = ts.utc(2023, 10, 21)
end_date = start_date + timedelta(days=0.5)
time_step = timedelta(seconds=10)

# 지도 초기화
m = folium.Map(location=[38.921389, -77.065556], zoom_start=5)

# colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'purple', 'orange', 'brown']  # 원하는 색상 리스트를 추가
colors = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'brown']
color_index = 0  # 색상 인덱스 초기화

# 궤도 계산 및 지도에 그리기
while start_date.tt < end_date.tt:
    circle_color = colors[color_index]
    #color_index = (color_index + 1) % len(colors)  # 다음 색상으로 순환

    topocentric = satellite.at(start_date).subpoint()
    lat, lon = topocentric.latitude.degrees, topocentric.longitude.degrees  # degrees 속성 사용
    # lat, lon = topocentric.latitude().degrees, topocentric.longitude().degrees
    folium.Circle(
        location=[lat, lon],
        radius=15,
        color=circle_color,
        fill=True,
        fill_color=circle_color
    ).add_to(m)
    start_date += time_step

# 지도 저장
m.save('../folium_output/orbit_map1.html')
