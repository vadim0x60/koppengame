import urllib.request
import json
import re

# Let's test the public Street View tile or streetview metadata or the exact iframe URL
# The iframe URL is: https://maps.google.com/maps?q={lat},{lng}&layer=c&cbll={lat},{lng}&cbp=11,0,0,0,0&output=svembed

def check_embed(lat, lng):
    url = f"https://maps.google.com/maps?q={lat},{lng}&layer=c&cbll={lat},{lng}&cbp=11,0,0,0,0&output=svembed"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Check for error or pano ID in response
            # Let's see what content contains
            has_no_streetview = "Street View isn't available here" in content or "no-streetview" in content or "No street view available" in content
            return len(content), has_no_streetview, content[:300]
    except Exception as e:
        return 0, False, str(e)

with open("locations.json") as f:
    locs = json.load(f)

for loc in locs[:5]:
    sz, has_err, snippet = check_embed(loc['lat'], loc['lng'])
    print(f"{loc['id']}: size={sz}, has_err={has_err}")
