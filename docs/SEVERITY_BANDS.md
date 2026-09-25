# Severity bands: the USGS dNBR table

## The table

survey-burn classifies dNBR with the standard USGS severity bands from
Key & Benson (2006), *"Landscape Assessment: Sampling and Analysis
Methods"* (USDA Forest Service, General Technical Report RMRS-GTR-164-CD)
— the same break points used by USGS/NPS burn-severity products including
MTBS (Monitoring Trends in Burn Severity).

| class id | name | dNBR range | meaning |
|---|---|---|---|
| 5 | enhanced regrowth | < −0.10 | post-fire green-up exceeding the pre-fire signal |
| 0 | unburned | −0.10 – 0.10 | no detectable change (phenology + noise live here) |
| 1 | low severity | 0.10 – 0.27 | surface fire, most canopy intact |
| 2 | moderate-low severity | 0.27 – 0.44 | mixed surface/crown effects |
| 3 | moderate-high severity | 0.44 – 0.66 | extensive crown consumption |
| 4 | high severity | ≥ 0.66 | stand-replacing, near-complete consumption |

Exact break points belong to the **higher** class (0.10 is low, 0.27 is
moderate-low, 0.44 is moderate-high, 0.66 is high). Class ids are stable
across releases — survey-change transition matrices and the QML palette
depend on them.

## When to recalibrate

These bands were calibrated on **western-US conifer forests**. The same
dNBR means different things elsewhere:

- **Grasslands / shrublands:** pre-fire NBR is low, so even stand-
  replacing fire produces modest dNBR. Consider RdNBR (relative dNBR,
  `burn.dnbr.rdnbr`) and lower thresholds.
- **Tropical forests:** very high pre-fire NBR; small dNBR can still mean
  real canopy damage.
- **Croplands:** harvest produces dNBR in the low–moderate bands with no
  fire at all — the disturbance heuristic's documented false positive.

Recalibration is one constant: edit `SEVERITY_CLASSES` in
`src/burn/severity.py` (and note the change in your own docs, since class
ids feed downstream products).

## References

- Key, C.H. & Benson, N.C. (2006). *Landscape Assessment (LA): Sampling
  and Analysis Methods.* USDA Forest Service, RMRS-GTR-164-CD.
- Miller, J.D. & Thode, A.E. (2007). *Quantifying burn severity in a
  heterogeneous landscape with a relative version of the delta Normalized
  Burn Ratio (dNBR).* Remote Sensing of Environment, 109(1).
