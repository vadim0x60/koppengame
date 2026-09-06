import os
import urllib.request
import json
import time

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

def verify_streetview(lat, lng, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lng}&radius={radius}&key={API_KEY}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "OK":
                actual_loc = data.get("location", {})
                return True, actual_loc.get("lat", lat), actual_loc.get("lng", lng), data.get("pano_id")
    except Exception as e:
        print(f"Error checking {lat}, {lng}: {e}")
    return False, lat, lng, None

more_candidates = [
    # Uruguay Cfa
    {
        "id": "uruguay_ruta5_pasture",
        "name": "Ruta 5, Tacuarembó Rolling Pampas",
        "country": "Uruguay",
        "lat": -31.7312, "lng": -55.9812,
        "koppen_code": "Cfa", "koppen_group": "C", "koppen_name": "Humid Subtropical climate",
        "hints": ["Vast open green undulating pampas and grazing beef cattle", "Occasional eucalyptus windbreak rows along roadside pastures", "Warm humid summer months and mild winters without any dry season"],
        "explanation": "Cfa: The South American Pampas receive uniform rainfall all year round without drought, accompanied by warm, humid summers."
    },
    # Alaska Dfc
    {
        "id": "parks_hwy_alaska_taiga",
        "name": "Parks Highway, Denali Foothill Taiga",
        "country": "United States",
        "lat": 63.3812, "lng": -148.9512,
        "koppen_code": "Dfc", "koppen_group": "D", "koppen_name": "Subarctic (Taiga) climate",
        "hints": ["Expansive black and white spruce taiga, paper birch, and muskeg bogs", "Braided glacial streams and distant snow-capped Alaskan Range peaks", "Less than 4 months with mean temperature above 10°C; severe winter freeze down to -35°C"],
        "explanation": "Dfc: Interior Alaska's boreal forest endures long, bitter subarctic winters and short, cool summer growing seasons."
    },
    # Dsb (Dry summer continental, Oregon/Washington)
    {
        "id": "oregon_cascade_leeward_pines",
        "name": "US-97, Central Oregon Ponderosa Belt",
        "country": "United States",
        "lat": 43.6812, "lng": -121.5012,
        "koppen_code": "Dsb", "koppen_group": "D", "koppen_name": "Dry-summer Continental climate",
        "hints": ["Open stands of yellow-barked ponderosa pine with bitterbrush understory", "Volcanic pumice/ash soil, bone-dry summer grass in Cascade rain shadow", "Cold snowy winter temperatures with frequent sub-zero nights"],
        "explanation": "Dsb: Rain-shadowed volcanic plateaus east of the Cascades have continental freezing winters paired with Mediterranean bone-dry summer conditions."
    },
    # EF: Alpine Ice / Glacial
    {
        "id": "jungfraujoch_sphinx_pass",
        "name": "Jungfraujoch Sphinx Glacial Ridge",
        "country": "Switzerland",
        "lat": 46.5475, "lng": 7.9853,
        "koppen_code": "EF", "koppen_group": "E", "koppen_name": "Ice Cap / Perpetual Frost climate",
        "hints": ["Perpetual glacial ice (Aletsch Glacier) and year-round snowpack", "Severe alpine sub-zero freeze; warmest month mean fails to exceed 0°C", "No soil or vascular plant life; pure ice, snow, and bare horn crags"],
        "explanation": "EF (Ice Cap): High alpine glacial passes exceed 3,400m elevation where all 12 months average below 0°C, sustaining permanent ice."
    }
]

with open("verified_locations.json") as f:
    existing = json.load(f)

for c in more_candidates:
    ok, slat, slng, pano = verify_streetview(c["lat"], c["lng"])
    print(f"[{'PASS' if ok else 'FAIL'}] {c['id']} -> {slat}, {slng}, pano={pano}")
    if ok:
        c["lat"] = slat
        c["lng"] = slng
        c["pano_id"] = pano
        existing.append(c)

with open("locations.json", "w") as f:
    json.dump(existing, f, indent=2)

print(f"Total confirmed verified locations: {len(existing)}")
