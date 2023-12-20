# Error List

아래와 같이 에러가 발생한 경우  
```commandline
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for basemap
Failed to build basemap
ERROR: Could not build wheels for basemap, which is required to install pyproject.toml-based projects
```
geos 설치 수행
```commandline
brew install geos
```


```commandline
#cmake 설치 안되어있으면
brew install cmake

brew install wget

wget http://download.osgeo.org/geos/geos-3.12.0.tar.bz2

tar -xvf geos-3.12.0.tar.bz2

cd geos-3.12.0.tar.bz2

./configure

make

sudo make install

```