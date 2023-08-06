import pyproj
from shapely.geometry import Point
from shapely.ops import transform

project = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:4326'), # source coordinate system
    pyproj.Proj(init='epsg:3301')) # destination coordinate system

def transformer(x,y):
    p = Point(x,y)
    transformed_point = transform(project.transform, p)
    return (transformed_point.x,transformed_point.y)