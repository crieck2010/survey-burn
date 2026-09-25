# The maths: NBR, dNBR, RdNBR, and the disturbance heuristic

## NBR — why this ratio sees fire

A spectral index is a contrast knob: pick two bands that move in opposite
directions when the thing you care about happens, and their normalised
difference amplifies the signal while cancelling illumination differences.

For fire the two bands are **near-infrared (NIR)** and **short-wave
infrared 2 (SWIR2)**:

- Healthy leaves are NIR-bright (spongy mesophyll scatters it) and
  SWIR2-dark (leaf water absorbs it) → NBR high, typically 0.5–0.8.
- Fire removes the leaves and deposits char/ash: NIR collapses, SWIR2
  rises → NBR falls toward 0 or negative.

NBR = (NIR − SWIR2) / (NIR + SWIR2), in [−1, 1]. The division normalises
out brightness: a sunlit and a shaded healthy pixel get nearly the same
NBR, while their raw reflectances differ a lot.

## dNBR — the before/after difference

dNBR = NBR_pre − NBR_post. Where nothing changed, the two scenes cancel
to ~0 (plus phenology wobble, which is why "unburned" spans ±0.10). Over
a scar the difference is large and positive: a 0.6 → −0.2 swing reads as
dNBR = 0.8, deep in high severity.

The catch: dNBR needs a **true pre-fire image**. If the "pre" scene is
from after green-up began, phenology leaks into the difference and
unburned land reads as low severity.

## RdNBR — normalising for sparse vegetation

The same fire in sparse grassland produces a smaller absolute dNBR than
in dense forest, because there was less NBR to lose. RdNBR divides by the
pre-fire signal magnitude:

RdNBR = dNBR / √|NBR_pre|

A 0.3 dNBR over pre-fire NBR of 0.15 (sparse) gives RdNBR ≈ 0.77 — a loud
signal — while the same 0.3 over pre-fire 0.6 (dense) gives ≈ 0.39. Use
RdNBR when pre-fire cover is thin or heterogeneous.

## The disturbance heuristic — why two indices

Clearing and logging strip vegetation mechanically: both NDVI (greenness)
and NBR (structure/water) fall together, hard, in one pass interval.
Seasonal senescence usually moves NDVI more than NBR; drought browns both
but coherently over whole regions. So the rule:

disturbed ⟺ ΔNDVI ≤ −0.15 **and** ΔNBR ≤ −0.10

…catches mechanical removal while staying quieter than either index
alone. The `confidence` score (0–1) measures how far past both thresholds
the drops went: a patch at 2× the thresholds scores ~1.0, a patch barely
over the line scores near 0. Read low-confidence flags as "look here",
not "violation confirmed".

## Area from pixels

Every area in this engine is `pixel_count × pixel_size_m² / 10_000`
hectares. The polygon vectoriser builds pixel-exact boundaries, so a
polygon's `area_ha` equals its raster pixel count times the pixel area —
the raster and vector products always agree.
