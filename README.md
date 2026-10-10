> [!IMPORTANT]
> **Consolidated into [EarthWatch-Suite](https://github.com/crieck2010/earthwatch-suite)**  
> This engine has been consolidated into the unified [EarthWatch-Suite monorepo](https://github.com/crieck2010/earthwatch-suite). Active development, bug fixes, releases, and unified testing now live in earthwatch-suite. This repository is preserved as an archive.

# survey-burn

> **Part of [earthwatch-suite](https://github.com/crieck2010/earthwatch-suite)** —
> the remote-sensing project (satellite imagery, change detection, site
> monitoring). Terrestrial surveying lives in
> [survey-suite](https://github.com/crieck2010/survey-suite); the two stay
> compatible through the
> [cross-suite contracts](https://github.com/crieck2010/earthwatch-suite/blob/main/docs/CONTRACTS.md).

The **burn-scar / disturbance mapping engine** for earthwatch-suite: dNBR
fire-severity classification, per-zone burned-area time series, a
clearing/logging disturbance heuristic, and disturbance polygons. Built for
the construction / land-use compliance niche — did that clearing happen
inside the permitted footprint? — and for post-fire assessment, and feeds
survey-monitor as a first-class metric source.

It does **not** reimplement spectral indices. NBR comes from
survey-imagery's index registry (lazy import, reused); this package adds
the burn-specific analytics on top: dNBR/RdNBR, USGS severity bands,
severity-area series, the disturbance heuristic, and polygon vectorisation.

## Quickstart (no network — synthetic demo)

```bash
pip install survey-burn
survey-burn demo --out-dir ./burn-demo
```

That runs the full pipeline on seeded synthetic data: a planted 12.57 ha
burn with known severity rings, dNBR + severity rasters, QML styles, and a
disturbance polygon GeoJSON. The demo prints planted-vs-measured areas —
they match exactly.

```bash
# dNBR from two NBR rasters, then USGS severity classification
survey-burn dnbr --pre pre_nbr.npy --post post_nbr.npy --out dnbr.npy
survey-burn severity --dnbr dnbr.npy --out severity.npy --qml severity.qml

# per-zone burned-area time series (incremental CSV)
survey-burn timeseries --zones zones.geojson --out timeseries.csv --synthetic

# clearing/logging disturbance heuristic on a pass series
survey-burn disturbance --synthetic --out events.json

# burn polygons to GeoJSON
survey-burn polygons --synthetic --out burn_polygons.geojson
```

## What it produces

| Product | Format | Notes |
|---|---|---|
| dNBR raster | `.npy` / GeoTIFF via acquire path | pre-fire NBR − post-fire NBR |
| Severity raster | uint8 GeoTIFF + `.qml` | 6 USGS classes, stable ids |
| Burned-area time series | CSV (incremental) | `burned_ha`, `burned_fraction`, per-class ha |
| Disturbance events | JSON | patch polygons' worth of clearing/logging flags |
| Disturbance polygons | GeoJSON | pixel-exact, per-feature area + dominant severity |

## The maths

**NBR** (Normalised Burn Ratio) is `(NIR − SWIR2) / (NIR + SWIR2)`.
Healthy green vegetation reflects strongly in the near-infrared and
absorbs in short-wave infrared, so NBR is high (~0.5–0.8). Fire destroys
chlorophyll and leaves char/ash: NIR collapses, SWIR2 rises, and NBR
drops to near zero or negative.

**dNBR** is simply `NBR_pre − NBR_post`. Where nothing changed the two
scenes cancel to ~0; over a scar the difference is large and positive.
**RdNBR** (relative dNBR) divides by `√|NBR_pre|`, so the same absolute
drop counts more in sparse vegetation — important in grasslands where
there wasn't much green to lose.

**Severity bands** are the USGS standard (Key & Benson, 2006; used by
MTBS): unburned < 0.10, low 0.10–0.27, moderate-low 0.27–0.44,
moderate-high 0.44–0.66, high ≥ 0.66, enhanced regrowth < −0.10. Exact
break points belong to the higher class. See `docs/SEVERITY_BANDS.md`.

**The disturbance heuristic** flags pixels where NDVI *and* NBR both fall
sharply between consecutive passes. Requiring both rejects most seasonal
senescence (which moves NDVI more than NBR) while catching mechanical
removal, which strips NIR in both. It's a heuristic — harvest, drought
browning, and cloud leakage are documented false-positive modes
(`docs/` has the full list).

## Integration

**survey-monitor:** the time-series CSV columns `burned_ha` and
`burned_fraction` are the documented monitor contract — a site config per
zone thresholds them exactly like the vegetation/flood engines' columns:

```yaml
# site config snippet
indices: [dnbr]
thresholds:
  dnbr:
    metric: burned_ha
    warning: 5.0
    critical: 20.0
```

**survey-change:** severity rasters carry stable class ids, so they feed
`survey-change` transition matrices directly (e.g. high-severity →
regrowth over two seasons).

**survey-qgis:** drop the severity raster + `.qml` sidecar into QGIS, or
drag the disturbance GeoJSON straight onto the canvas.

**survey-imagery:** NBR and the STAC acquisition path are reused, not
reimplemented (`pip install "survey-burn[acquire]"` for real data).

## Limitations (honest)

- dNBR needs a **true pre-fire image** — a pre scene from after green-up
  started, or phenology contaminates the difference.
- The USGS bands were calibrated on western-US conifer forests; in
  grasslands, shrublands, or tropical forest the same dNBR means something
  different. Recalibrate per ecosystem (the band table is one constant in
  `burn/severity.py`).
- The disturbance heuristic is not a classifier: harvest, drought
  browning, and cloud/shadow leakage all fire it. Use the confidence
  score and spatial pattern, not the flag alone.
- Optical only — smoke and clouds hide the scar until the sky clears.
- Screening and compliance-support tool, **not** an incident-response or
  fire-perimeter system.

## Docs

- `docs/TIMESERIES_SCHEMA.md` — the burned-area CSV, column by column
- `docs/SEVERITY_BANDS.md` — the USGS band table, its source, and when to recalibrate
- `docs/MATHS.md` — NBR/dNBR/RdNBR and the heuristic, worked through
- `examples/` — end-to-end scripts

## Install

Requires Python 3.9+, numpy.

```bash
pip install survey-burn                    # core (numpy only)
pip install "survey-burn[acquire]"         # + survey-imagery for real STAC data
pip install "survey-burn[raster]"          # + rasterio for GeoTIFF/polygon zones
pip install "survey-burn[full]"            # everything
```
