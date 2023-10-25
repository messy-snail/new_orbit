import read_tle
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
from tqdm import tqdm


# 위성 TLE 데이터

tle_data = read_tle.read_tle_file('tle_list.txt')
# 읽어온 TLE 정보 출력 (테스트용)
# tle_data = [
#     ('KOMPSAT-3A', '1 38338U 12025B   23297.62525709  .00000910  00000+0  19013-3 0  9990',
#      '2 38338  98.2322 239.1614 0008989 258.8215 101.1975 14.62228630610087'),
#     ('KOMPSAT-5', '1 39227U 13042A   23297.59983914  .00003163  00000+0  23031-3 0  9998',
#      '2 39227  97.6188 121.8189 0001654 136.7816 223.3540 15.04489647558524')
# ]

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
    while start_date.tt < end_date.tt:
        topocentric = satellite.at(start_date).subpoint()
        lat, lon = topocentric.latitude.degrees, topocentric.longitude.degrees

        if lons and abs(lon - lons[-1]) > 180:
            # 경도가 180에서 -180으로 바뀌면 선이 이어지지 않도록 중단
            m.plot(lons, lats, color=line_color, linestyle=linestyle, linewidth=1)  # 선의 색상을 설정
            lats, lons = [],[]

        lats.append(lat)
        lons.append(lon)
        start_date += time_step
        
    line, = m.plot(lons, lats, color=line_color, linestyle=linestyle, linewidth=1)  # 선의 색상과 스타일을 설정
    legend_lines.append(line)  # Line2D 객체를 레전드 리스트에 추가

# 레전드 추가 (레전드 라인과 위성 이름을 함께 표시)
legend_labels = [name for i, (_, name) in enumerate(satellites)]
plt.legend(legend_lines, legend_labels, loc='upper right', bbox_to_anchor=(1.0, 1.0))

# 지도 표시
plt.title("Satellite Orbits")
plt.tight_layout()
plt.show()
