"""End-to-end example: synthetic burn -> dNBR -> severity -> polygons -> CSV.

Run:  PYTHONPATH=src python3 examples/end_to_end.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from burn.dnbr import dnbr
from burn.polygons import vectorize, write_geojson
from burn.severity import burned_mask, class_areas, classify
from burn.synthetic import (
    DEMO_PIXEL_M,
    DEMO_TRANSFORM,
    expected_burn_areas,
    synthetic_post_nbr,
    synthetic_pre_nbr,
)
from burn.timeseries import ZonePassRecord, append_records
from burn.zones import Zone

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

# 1. dNBR + severity on the planted synthetic scar
pre = synthetic_pre_nbr()
post = synthetic_post_nbr()
d = dnbr(pre, post)
sev = classify(d)
areas = class_areas(sev, None, DEMO_PIXEL_M)
expected = expected_burn_areas()
print(f"burned: planted={expected['burned_ha']:.2f} ha  measured={areas['burned_ha']:.2f} ha")

# 2. One record for a whole-tile "zone", appended to the CSV
zone = Zone(id="demo-tile", name="Demo Tile", geometry={"type": "Polygon", "coordinates": []})
rec = ZonePassRecord.from_class_areas(
    zone_id=zone.id, zone_name=zone.name, pass_id="syn-post-20240801",
    date="2024-08-01", index="dnbr", areas=areas,
    total_pixels=int(sev.size), pixel_size_m=DEMO_PIXEL_M, cloud_cover=5.0,
)
csv_path = os.path.join(OUT, "timeseries.csv")
print(f"timeseries: appended {append_records(csv_path, [rec])} row(s) -> {csv_path}")

# 3. Polygons
features = vectorize(
    burned_mask(d), transform=DEMO_TRANSFORM, severity=sev,
    pixel_size_m=DEMO_PIXEL_M,
)
gpath = write_geojson(features, os.path.join(OUT, "burn_polygons.geojson"))
print(f"polygons: {len(features)} feature(s) -> {gpath}")
