from math import atan2, cos, radians, sin, sqrt

_EARTH_RADIUS_METERS = 6371000

def calculate_distance(lat1, lon1, lat2, lon2):
  """ Calcula a distância entre as duas coordenadas
  (lat1, lon1) e (lat2, lon2) em metros usando a
  fórmula de Haversine. """

  dlat = radians(lat2 - lat1)
  dlon = radians(lon2 - lon1)

  a = sin(dlat / 2) ** 2 \
    + cos(radians(lat1)) \
    * cos(radians(lat2)) \
    * sin(dlon / 2) ** 2

  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  return _EARTH_RADIUS_METERS * c