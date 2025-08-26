import json
from keplergl import KeplerGl
import pandas as pd 
import numpy as np
import itertools

# preprocessing
df = pd.read_csv("2yr_traffic_geotagged.csv")
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

df.rename(columns={"Latitude": "lat", "Longitude": "lng"}, inplace=True)

# break into weekly increments
df['Date'] = pd.to_datetime(df['Date'])
df['week'] = (df['Date'] - pd.to_timedelta(df['Date'].dt.weekday, unit='D')).dt.date
df['week'] = pd.to_datetime(df['week']).dt.strftime('%Y-%m-%dT%H:%M:%S') # ensure week_start is datetime format

# regroup values into just coordinates, weeks, volume
df = df.groupby(['week', 'lat', 'lng'], as_index=False).agg({"Vol": "sum"})

# get all weeks and all coordinate pairs, so that we can have data for all coordinates and weeks 
all_weeks = df['week'].unique()
all_coordinates = df[['lat', 'lng']].drop_duplicates()
filled_grid = pd.DataFrame(list(itertools.product(all_weeks, all_coordinates['lat'], all_coordinates['lng'])), columns = ['week', 'lat', 'lng'])

valid_coords = df[['lat', 'lng']].drop_duplicates()
valid_filled_grid = filled_grid.merge(valid_coords, on=['lat', 'lng'], how='inner')

# merge with existing data
df = valid_filled_grid.merge(df, on=['week', 'lat', 'lng'], how='left')

df['Vol'] = df['Vol'].interpolate(method='linear')
df.to_csv('traffic_data_final.csv')

kepler_config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [
                {
                    "dataId": [
                        "-zf4o5h"
                    ],
                    "id": "oz17gxx5g",
                    "name": [
                        "week"
                    ],
                    "type": "timeRange",
                    "value": [
                        1654819344000,
                        1657521487000
                    ],
                    "plotType": {
                        "interval": "1-week",
                        "defaultTimeFormat": "L",
                        "type": "histogram",
                        "aggregation": "sum"
                    },
                    "animationWindow": "free",
                    "yAxis": None,
                    "view": "minified",
                    "speed": 1,
                    "syncTimelineMode": 1,
                    "enabled": True
                }
            ],
            "layers": [
                {
                    "id": "debwnj",
                    "type": "grid",
                    "config": {
                        "dataId": "-zf4o5h",
                        "label": "new layer",
                        "color": [
                            77,
                            193,
                            156
                        ],
                        "highlightColor": [
                            252,
                            242,
                            26,
                            255
                        ],
                        "columns": {
                            "lat": "lat",
                            "lng": "lng"
                        },
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "worldUnitSize": 1,
                            "colorRange": {
                                "colors": [
                                    "#FFF7EC",
                                    "#FDDCAF",
                                    "#FDB07A",
                                    "#F16C49",
                                    "#C81D13",
                                    "#7F0000"
                                ],
                                "name": "OrRd",
                                "type": "sequential",
                                "category": "ColorBrewer"
                            },
                            "coverage": 1,
                            "sizeRange": [
                                0,
                                500
                            ],
                            "percentile": [
                                0,
                                100
                            ],
                            "elevationPercentile": [
                                0,
                                100
                            ],
                            "elevationScale": 20,
                            "enableElevationZoomFactor": True,
                            "fixedHeight": False,
                            "colorAggregation": "average",
                            "sizeAggregation": "average",
                            "enable3d": True
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [
                                    255,
                                    255,
                                    255
                                ],
                                "size": 18,
                                "offset": [
                                    0,
                                    0
                                ],
                                "anchor": "start",
                                "alignment": "center",
                                "outlineWidth": 0,
                                "outlineColor": [
                                    255,
                                    0,
                                    0,
                                    255
                                ],
                                "background": False,
                                "backgroundColor": [
                                    0,
                                    0,
                                    200,
                                    255
                                ]
                            }
                        ]
                    },
                    "visualChannels": {
                        "colorField": {
                            "name": "Vol",
                            "type": "real"
                        },
                        "colorScale": "quantile",
                        "sizeField": {
                            "name": "Vol",
                            "type": "real"
                        },
                        "sizeScale": "linear"
                    }
                }
            ],
            "effects": [],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "-zf4o5h": [
                            {
                                "name": "Vol",
                                "format": ".3~s"
                            }
                        ]
                    },
                    "compareMode": True,
                    "compareType": "relative",
                    "enabled": True
                },
                "brush": {
                    "size": 0.5,
                    "enabled": False
                },
                "geocoder": {
                    "enabled": False
                },
                "coordinate": {
                    "enabled": False
                }
            },
            "layerBlending": "normal",
            "overlayBlending": "normal",
            "splitMaps": [],
            "animationConfig": {
                "currentTime": False,
                "speed": 1
            },
            "editor": {
                "features": [],
                "visible": True
            }
        },
        "mapState": {
            "bearing": 24,
            "dragRotate": True,
            "latitude": 40.69333013383505,
            "longitude": -73.99481322668227,
            "pitch": 50,
            "zoom": 9.548700360662087,
            "isSplit": False,
            "isViewportSynced": True,
            "isZoomLocked": False,
            "splitMapViewports": []
        },
        "mapStyle": {
            "styleType": "dark-matter",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False
            },
            "threeDBuildingColor": [
                15.035172933000911,
                15.035172933000911,
                15.035172933000911
            ],
            "backgroundColor": [
                0,
                0,
                0
            ],
            "mapStyles": {}
        },
        "uiState": {
            "mapControls": {
                "mapLegend": {
                    "active": False
                }
            }
        }
    }
}

# init kepler map
map = KeplerGl(height=800)

map.add_data(data=df, name="-zf4o5h")

# apply loaded config 
map.config = kepler_config

map.save_to_html(file_name="traffic_grid.html")
