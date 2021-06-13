# heightmapper.py

https://github.com/u-onder/heightmapper

Heightmapper.py is an command line height map generation script, which can generate heightmaps for use in 3D applications. 
It will generate a height map image (grey scale png file) for a given bounding box. Minimum and maximum altitudes can also be supplied.

Uses [Mapzen's](http://mapzen.com/tangrams/tangram) global [elevation service](https://mapzen.com/blog/elevation).
<img width="900" alt="screen shot 2016-07-19 at 11 17 17 am" src="https://cloud.githubusercontent.com/assets/459970/16955404/6e9ec51e-4da2-11e6-97e1-d43d2682e07b.png">


### Usage
- python download.py -z <zoomlevel> -t <top Longitude> -b <bottom longitude> -l <left latitude> -r <right latitude> -o <outputfilename> -m <minimum threshold> -x <maximum trhreshold>

- the boundig box can be given with parameters -t -b -l -r
- bounding box top must be greater than bottom one.
- resulting image can be greater than the bounding box.
- resulting image will be normilized within minimum and maximum thresholds
