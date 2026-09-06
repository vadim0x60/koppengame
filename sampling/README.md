# Built-up-land downsampling pilot

Shared geographic metadata for the game and model development. This is **not an
image classifier**: low building coverage does not prove environmental visibility,
and rural scenes can still contain landmarks, signs, and other geographic cues.

## Current pilot

Annotated all 2,628 source sites using GHS-BUILT-S 2020, R2023A, 100 m Mollweide.
The original `game/locations.json` is unchanged. The game loads
`game/game-selection.json`, checks the source SHA-256, and shuffles the selected
sites without replacement. Missing/stale/invalid selections fall back to the full
pool with a console warning, rather than breaking the game.

| Geographic proxy | Source | Game selection |
| --- | ---: | ---: |
| Rural | 369 | 369 |
| Mixed | 797 | 463 |
| Urban | 1,462 | 267 |
| Total | 2,628 | 1,099 |

Every represented raw climate × country combination retains at least one site.
Urban share falls from 55.6% to 24.3%, **not** the aspirational 15%: sparse and
all-urban strata take precedence over that quota. Country is a coarse region proxy,
not a substitute for geographically separated sampling. Class/country proportions
can still change; the manifest reports every stratum's retention.

## Geographic annotation and policies

- Compute the mean built surface / 10,000 m² over 100 m raster cells touching
  geodesic circles of radius 100 m and 500 m. Boundary cells count in full, so these
  are approximate neighborhood fractions, not precise subpixel buffer statistics.
- Pilot labels use the larger fraction: `<0.05` rural, `0.05–<0.20` mixed,
  `>=0.20` urban. These are **not official GHSL settlement classes**.
- Require 90% valid cell coverage at both scales. Missing coverage and
  dateline-crossing buffers are unknown, not rural; unknown sites are retained.
- The supplied coordinates have **not been verified against actual capture
  coordinates**. Each manifest entry flags this. Re-annotate when coordinates are
  verified, and account for imagery dates differing from the raster's 2020 epoch.
- Game: retain rural/unknown sites, ceil(half) of mixed sites, then up to
  floor(nonurban × 0.15 / 0.85) urban sites, minimum one if urban candidates exist,
  within each climate × country stratum. Stable ID order and seed 42 fix selection.
- Model: rural/unknown : mixed : urban sampling weights are 1 : 0.5 : 0.25,
  normalized to mean one within climate × country. This preserves stratum weight
  totals, so an all-urban stratum is deliberately not downweighted relative to other
  strata. Weights apply to **training sites**, not independent views.
- Model evaluation: keep every site and weight one; report land-use slices.
  Split geographically first, then recompute training-weight normalization on the
  training partition. The pilot exports unsplit planning weights, not a ready-made
  benchmark or permission to train on Street View.

## Reproduce

Python 3.11+ for raster annotation; the model planner still needs only the standard
library. Install optional dependencies with `pip install -r sampling/requirements.txt`.
Download the approximately 2 GB [official GHSL archive](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A/GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100/V1-0/GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_V1_0.zip)
outside the repository and extract its `.tif` (overviews are unnecessary).
The TIFF checksum is in `pilot/manifest.json`; no raster is bundled.

From the repository root, using a new output directory:

```sh
python3 sampling/landuse.py --locations game/locations.json \
  --raster /path/to/GHS_BUILT_S_E2020_GLOBE_R2023A_54009_100_V1_0.tif \
  --output /tmp/landuse-pilot
# Review manifest summary and audit queue before replacing tracked pilot outputs.
cp /tmp/landuse-pilot/game-selection.json game/game-selection.json

python3 koppenmodel/prepare.py --game game \
  --land-use sampling/pilot/manifest.json \
  --output /tmp/model-audit.json --views-output /tmp/model-views.jsonl

python3 -m unittest discover -s sampling -p 'test_*.py' -v
PYTHONPATH=koppenmodel python3 -m unittest discover -s koppenmodel/tests -v
node --test game/test_sampling.cjs
```

When promoting a regenerated selection, also replace `pilot/manifest.json` and
`pilot/audit.csv` from the same run; don't overwrite completed human audit work.
Regenerate after any source-location change, including legacy generator runs.

## Manual scene audit — queued, not completed

`pilot/audit.csv` contains 300 unique sites sampled round-robin from shuffled
climate × country × proxy-land-use buckets, including retained and rejected sites.
This is a coverage-oriented audit, **not a prevalence estimate**. Inspect the
available panorama in multiple headings for game curation. Research-image review
must use imagery licensed for that purpose; this tool acquires no imagery and
does not resolve the rights requirements in `koppenmodel/README.md`.

Fill these columns rather than inferring labels from country or climate:

- `environment_visibility`: low / medium / high, considering vegetation,
  exposed ground, terrain, snow or ice; do not require greenery.
- `cultural_dominance`: low / medium / high, considering visible buildings,
  writing, distinctive landmarks, etc. Don't classify particular religions as
  climate cues or assume rural means culturally anonymous.
- `irrigated_or_ornamental`: yes / no / uncertain.
- `headings_reviewed`, `reviewer`, `notes`: record evidence and uncertainty,
  including unavailable panoramas or coordinate mismatches.

Audit both false rural and false urban assignments, including parks, deserts,
polar sites, suburbs, and rural landmarks. Threshold changes should use pilot/
training review only. These manual fields are not automatically consumed yet;
the current selection is explicitly a geographic-only baseline. Do not claim
the pool is 85% environment-dominant without completing scene review.

## Attribution

European Commission, Joint Research Centre (JRC). Pesaresi, M.; Politis, P. (2023),
**GHS-BUILT-S R2023A**, DOI: [10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA](https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA).
GHSL reuse is authorized with acknowledgement; see the
[official product description](https://human-settlement.emergency.copernicus.eu/ghs_buS2023.php).
The 2020 layer is interpolated/extrapolated, not a 2020 street-level observation.
