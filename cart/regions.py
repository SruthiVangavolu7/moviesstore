"""Regions used by the local popularity map (user story 1 - anish) """
REGIONS = [
    {"key": "northeast", "name": "Northeast", "lat": 41.6, "lng": -73.9,
     "states": "New England, NY, NJ, PA"},
    {"key": "southeast", "name": "Southeast", "lat": 33.2, "lng": -84.2,
     "states": "GA, FL, the Carolinas, VA, TN, AL"},
    {"key": "midwest", "name": "Midwest", "lat": 41.9, "lng": -89.6,
     "states": "IL, OH, MI, IN, WI, MN, MO"},
    {"key": "southwest", "name": "Southwest", "lat": 32.8, "lng": -101.5,
     "states": "TX, OK, NM, AZ"},
    {"key": "west", "name": "West", "lat": 39.5, "lng": -119.5,
     "states": "CA, WA, OR, NV, CO, UT"},
]

REGION_CHOICES = [(r["key"], r["name"]) for r in REGIONS]
REGIONS_BY_KEY = {r["key"]: r for r in REGIONS}