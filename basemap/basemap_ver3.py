from utils import read_tle
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from skyfield.api import load, EarthSatellite
from datetime import timedelta
from tqdm import tqdm

# 위성 TLE 데이터
# tle_data = read_tle.read_tle_file('../input_data/tle_list.txt')
tle_data = read_tle.read_tle_file('../input_data/k3a_tle.txt')

# TLE 데이터를 위성 객체로 변환
ts = load.timescale()
satellites = []

for name, tle_line1, tle_line2 in tle_data:
    satellite = EarthSatellite(tle_line1, tle_line2, name, ts)
    satellites.append((satellite, name))  # 위성 객체와 이름을 튜플로 저장

# 시작 날짜와 끝 날짜 설정 (예시로 1일치 궤도를 전파)
original_start_date = ts.utc(2023, 10, 21)
end_date = original_start_date + timedelta(days=0.3)
time_step = timedelta(minutes=1)

# 지도 초기화
fig = plt.figure(figsize=(24, 10))
m = Basemap(projection='cyl', resolution='l', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
m.drawcoastlines()
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 45), labels=[0,0,0,1])
m.shadedrelief()
# 각 위성의 궤도 계산 및 지도에 그리기
colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k', 'purple', 'orange', 'brown']  # 원하는 색상 리스트를 추가

linestyle_list = ['-', '--', '-.', ':']  # 선 스타일 리스트

color_index = 0  # 색상 인덱스 초기화
legend_lines = []  # 레전드에 추가할 Line2D 객체 리스트


for i, (satellite, name) in enumerate(tqdm(satellites)):
    lats, lons = [], []
    line_color = colors[color_index]
    color_index = (color_index + 1) % len(colors)  # 다음 색상으로 순환
    linestyle = linestyle_list[i % len(linestyle_list)]  # 선 스타일 순환

    start_date = original_start_date
    prev_lat = None  # 이전 위도 값 초기화

    while start_date.tt < end_date.tt:
        topocentric = satellite.at(start_date).subpoint()
        lat, lon = topocentric.latitude.degrees, topocentric.longitude.degrees

        # 승교점 감지 로직
        if prev_lat is not None and prev_lat > 0 and lat < 0:
            # 승교점을 지날 때마다 선의 색상을 변경
            m.plot(lons, lats, color=line_color, linestyle=linestyle, linewidth=2)  # 현재 색상의 선 그리기
            lats, lons = [], []
            line_color = colors[color_index]  # 다음 색상으로 변경
            color_index = (color_index + 1) % len(colors)  # 다음 색상으로 순환

        if lons and abs(lon - lons[-1]) > 180:
            m.plot(lons, lats, color=line_color, linestyle=linestyle, linewidth=2)
            lats, lons = [], []

        lats.append(lat)
        lons.append(lon)
        prev_lat = lat  # 이전 위도 업데이트
        start_date += time_step

    line, = m.plot(lons, lats, color=line_color, linestyle=linestyle, linewidth=2)
    legend_lines.append(line)

# 레전드 추가 (레전드 라인과 위성 이름을 함께 표시)
legend_labels = [name for i, (_, name) in enumerate(satellites)]
plt.legend(legend_lines, legend_labels, loc='upper right', bbox_to_anchor=(1.0, 1.0))

# 지도 표시
plt.title("Satellite Orbits")
plt.tight_layout()
plt.show()
