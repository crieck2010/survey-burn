# Changelog

## v0.1.0 — 2026-09-25

Initial release.

- dNBR / RdNBR computation with NaN-honest arithmetic and pre/post pass
  selection around a fire date
- USGS dNBR severity classification (6 classes, stable ids, exact band
  edges tested) + paletted QML styles
- Per-zone burned-area time series (incremental CSV, deduped on
  zone_id+pass_id+index) with per-severity-class hectares
- Clearing/logging disturbance heuristic (dual NDVI+NBR drop, confidence
  scoring, speckle filtering) with documented false-positive modes
- Pixel-exact disturbance polygons (GeoJSON, per-feature area + dominant
  severity, interior holes preserved) via pure-numpy edge chaining
- NBR reused from survey-imagery's registry (lazy import); STAC
  acquisition path via `imagery.monitor.run_monitor`
- Seeded synthetic demo (planted 12.57 ha burn, planted clearing event)
  with planted-vs-measured verification
- 67 pytest tests, all passing
