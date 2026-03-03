import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import Draw
from shapely.geometry import Point

CNPJ_PATH = "data/base_files/vets_geolocation.csv"
DISTRICTS_PATH = "data/base_files/sp_districts.geojson"
OUTPUT_MAP = "data/map/establishments_by_district_map.html"

df = pd.read_csv(CNPJ_PATH, sep=";", dtype=str)

df["latitude"] = df["lat"].astype(float)
df["longitude"] = df["lon"].astype(float)

geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]

gdf_establishments = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

districts = gpd.read_file(DISTRICTS_PATH).to_crs("EPSG:4326")

gdf_join = gpd.sjoin(
    gdf_establishments,
    districts,
    how="left",
    predicate="within"
)

agg = (
    gdf_join
    .groupby("cd_distrito_municipal")
    .size()
    .reset_index(name="establishments_count")
)

districts_full = districts.merge(
    agg,
    on="cd_distrito_municipal",
    how="left"
)

districts_full["establishments_count"] = (
    districts_full["establishments_count"]
    .fillna(0)
)

required_columns = [
    "cd_distrito_municipal",
    "nm_distrito_municipal",
    "establishments_count",
    "geometry"
]

districts_full = districts_full[required_columns]

map_obj = folium.Map(
    location=[-23.55, -46.63],
    zoom_start=11,
    tiles="cartodbpositron"
)

folium.Choropleth(
    geo_data=districts_full,
    data=districts_full,
    columns=["cd_distrito_municipal", "establishments_count"],
    key_on="feature.properties.cd_distrito_municipal",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Number of Establishments"
).add_to(map_obj)

folium.GeoJson(
    districts_full,
    tooltip=folium.GeoJsonTooltip(
        fields=["nm_distrito_municipal", "establishments_count"],
        aliases=["District:", "Count:"]
    ),
    style_function=lambda x: {
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0
    }
).add_to(map_obj)

districts_full["centroid"] = districts_full.geometry.representative_point()

for _, row in districts_full.iterrows():
    folium.Marker(
        location=[row["centroid"].y, row["centroid"].x],
        icon=folium.DivIcon(
            html=f"""
                <div style="
                    font-size:7pt;
                    font-weight:bold;
                    color:black;
                    text-align:center;
                ">
                    {int(row['establishments_count'])}
                </div>
            """
        )
    ).add_to(map_obj)

draw = Draw(
    export=True,
    filename='dados.geojson',
    draw_options={
        'polyline': True,
        'polygon': True,
        'circle': True,
        'rectangle': True,
        'marker': True,
        'circlemarker': False
    },
    edit_options={'edit': True}
).add_to(map_obj)

map_obj.save(OUTPUT_MAP)
