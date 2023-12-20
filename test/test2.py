import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta
from sgp4.api import Satrec
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs84


import math

# ECEF 좌표를 위도와 경도로 변환하는 함수

def ecef_to_latlon(x, y, z):
    # WGS 84 지구 반경 및 탈락률 상수
    a = 6378.137  # 지구의 장반경 (킬로미터)
    f = 1 / 298.257223563  # 탈락률 (Reciprocal of flattening)

    # 탈락률 관련 계산
    e2 = 2 * f - f**2
    r = math.sqrt(x**2 + y**2)  # 두 점 사이의 거리 (수평 거리)

    # 위도 계산
    latitude = math.atan2(z, r * (1 - e2))

    # 경도 계산
    longitude = math.atan2(y, x)

    # 라디안 값을 도(degree)로 변환
    latitude = math.degrees(latitude)
    longitude = math.degrees(longitude)

    return latitude, longitude


# TLE 데이터

#ARIRANG-3 (KOMPSAT-3)   
line1 ='1 38338U 12025B   23297.62525709  .00000910  00000+0  19013-3 0  9990'
line2 = '2 38338  98.2322 239.1614 0008989 258.8215 101.1975 14.62228630610087'

# TLE 데이터를 파싱하여 위성 객체 생성
satellite = twoline2rv(line1, line2, wgs84)

# 시작 날짜와 끝 날짜 설정 (두 날짜 동안의 궤도 점을 찍기 위해)
start_date = datetime(2023, 10, 26, 00, 00, 00)
end_date = start_date + timedelta(days=1)
time_step = timedelta(seconds=1)  # 10분 간격으로 샘플링

# 지도 초기화
fig = plt.figure(figsize=(12, 8))
m = Basemap(projection='cyl', resolution='l', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
m.drawcoastlines()
m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0])
m.drawmeridians(range(-180, 181, 45), labels=[0,0,0,1])

# 궤도 점을 계산하고 지도에 찍기
lats, lons = [], []
iter =0;
while start_date < end_date:
    position, velocity = satellite.propagate(
        start_date.year, start_date.month, start_date.day,
        start_date.hour, start_date.minute, start_date.second
    )
    
    lat, lon = ecef_to_latlon(position[0], position[1], position[2])
    lats.append(lat)
    lons.append(lon)
    
    start_date += time_step
    iter+=1
    if iter >3600:
        break

# 지도에 궤도 점을 찍기
x, y = m(lons, lats)
m.plot(x, y, 'bo', markersize=2)  # 점으로 궤도를 표시

# 지도 표시
plt.title("KOMPSAT-3A 궤도")
plt.tight_layout()
plt.show()
