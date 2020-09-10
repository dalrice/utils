import h3
import googlemaps
from googlemaps import convert

lat, lng = 25.0774902, 55.1448226

lat1 = 25.066464
lng1 = 55.1351922

h3id = h3.geo_to_h3(lat, lng, 7)
h3id1 = h3.geo_to_h3(lat1, lng1, 7)
boundry = h3.h3_to_geo_boundary(h3id)

ZOOM_MAP = {
    6: 12,
    7: 14,
    8: 15,
    9: 16,
    10: 17
}


MAP_STATIC = "https://maps.googleapis.com/maps/api/staticmap?{}"
MAP_CONFIG = "size={size}&maptype=roadmap&zoom={zoom}"
MAP_PATH = "path=color:{color}|weight:{weight}|fillcolor:{fcolor}|enc:{poly_code}"


def get_path_from_h3(h3id, color="0xFF0000AA",
        weight=1, fillcolor="0xFFB6C1BB"):
    boundry = h3.h3_to_geo_boundary(h3id)
    poly_lines = list(boundry)
    poly_lines.append(boundry[0])
    polyline_code = convert.encode_polyline(poly_lines)
    return MAP_PATH.format(
        color=color,
        weight=weight,
        fcolor=fillcolor,
        poly_code=polyline_code
    )




def get_static_map(h3ids, res=7, size="500x500"):
    zoom = ZOOM_MAP.get(res, 14)
    map_config = MAP_CONFIG.format(size=size, zoom=zoom)
    params = [map_config, "key=AIzaSyDCce7ZDWT6OmSjx5m3TEVuqCBtquGIavw"]
    for h3id in h3ids:
        params.append(get_path_from_h3(h3id))
    map_param = "&".join(params)
    return MAP_STATIC.format(map_param)

h3ids = [h3id, h3id1]
get_static_path = get_static_map(h3ids, res=7, size="500x500")
print(get_static_path)
