import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from skyfield.api import load, Topos, EarthSatellite
from datetime import datetime, timedelta

#ARIRANG-3 (KOMPSAT-3)   
tle_line11 ='1 38338U 12025B   23297.62525709  .00000910  00000+0  19013-3 0  9990'
tle_line12 = '2 38338  98.2322 239.1614 0008989 258.8215 101.1975 14.62228630610087'

#ARIRANG-5 (KOMPSAT-5)   
tle_line21= '1 39227U 13042A   23297.59983914  .00003163  00000+0  23031-3 0  9998'
tle_line22= '2 39227  97.6188 121.8189 0001654 136.7816 223.3540 15.04489647558524'


# TLE 데이터를 위성 객체로 변환
ts = load.timescale()
satellite = EarthSatellite(tle_line11, tle_line12, 'KOMPSAT-5', ts)

# 시작 날짜와 끝 날짜 설정 (예시로 1일치 궤도를 전파)
start_date = ts.utc(2022, 10, 21)
end_date = start_date + timedelta(days=1)
time_step = timedelta(minutes=1)

# 지도 초기화
fig = plt.figure(figsize=(12, 8))
m = Basemap(projection='cyl', resolution='l', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
m.drawcoastlines()
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 45), labels=[0,0,0,1])
m.shadedrelief()
# 대륙 영역을 원하는 색상으로 채우기
# m.fillcontinents(color='gray', lake_color='blue')

# 궤도 계산 및 지도에 그리기
lats, lons = [], []

# while start_date.tt < end_date.tt:
#     topocentric = satellite.at(start_date).subpoint()
#     lat, lon = topocentric.latitude.degrees, topocentric.longitude.degrees  # degrees 속성 사용
#     lats.append(lat)
#     lons.append(lon)
    
#     start_date += time_step


# # 지도에 궤도 점을 찍기
# x, y = m(lons, lats)
# # m.plot(x, y, 'bo', markersize=2)  # 점으로 궤도를 표시
# m.plot(x, y, 'b-', linewidth=1)  # 선으로 궤도를 표시

while start_date.tt < end_date.tt:
    topocentric = satellite.at(start_date).subpoint()
    lat, lon = topocentric.latitude.degrees, topocentric.longitude.degrees  # degrees 속성 사용
    
    if lons and abs(lon - lons[-1]) > 180:
        # 경도가 180에서 -180으로 바뀌면 선이 이어지지 않도록 중단
        m.plot(lons, lats, 'b-', linewidth=1)
        lats, lons = [], []
    
    lats.append(lat)
    lons.append(lon)
    
    start_date += time_step

# 지도에 궤도 라인을 그리기
m.plot(lons, lats, 'b-', linewidth=1)  # 선으로 궤도를 표시

# 지도 표시
plt.title("KOMPSAT-3A")
plt.tight_layout()
plt.show()
