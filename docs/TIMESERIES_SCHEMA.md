# Time-series schema: burned-area records

One row per **(zone, pass, index)** — the burn state of one zone on one
satellite pass. Written by `survey-burn timeseries`; read by anything that
wants the numbers, including survey-monitor threshold checks.

## Columns

The shared prefix mirrors survey-vegetation's and survey-flood's schemas
so the three engines' CSVs feel like one family:

| Column | Type | Meaning |
|---|---|---|
| zone_id | str | zone identifier (from the zones GeoJSON) |
| zone_name | str | human-readable zone name |
| pass_id | str | satellite pass identifier |
| date | str | ISO date `YYYY-MM-DD` |
| doy | int | day of year |
| year | int | calendar year |
| index | str | `dnbr` or `disturbance` |
| valid_pixels | int | pixels that entered the statistics |
| total_pixels | int | pixels in the zone footprint |
| burned_pixels | int | pixels with dNBR ≥ 0.10 |
| burned_fraction | float | burned / valid, 0–1 |
| burned_ha | float | burned area in hectares |
| unburned_ha | float | dNBR in [−0.10, 0.10) |
| low_severity_ha | float | dNBR in [0.10, 0.27) |
| moderate_low_severity_ha | float | dNBR in [0.27, 0.44) |
| moderate_high_severity_ha | float | dNBR in [0.44, 0.66) |
| high_severity_ha | float | dNBR ≥ 0.66 |
| enhanced_regrowth_ha | float | dNBR < −0.10 |
| pixel_size_m | float | ground sampling distance used |
| cloud_cover | float\|empty | scene cloud cover, percent 0–100 (suite convention) |

## Stability contract

- Columns are **append-only**: new columns go at the end; existing columns
  are never renamed or removed within a major version.
- `burned_ha` and `burned_fraction` are the **survey-monitor contract
  columns** — a monitor site config thresholds them.
- Appends are **incremental and deduped** on (zone_id, pass_id, index):
  re-running with new passes never recomputes old rows, and re-appending
  the same records is a no-op.
