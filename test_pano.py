import urllib.request
import json
import re

# Test coordinates against Google's metadata endpoint
# Endpoint format: https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{lat}!4d{lng}!2d50!3m10!2m2!1sen!2sUS!9m1!1b1!10b1!11m1!2e10!12m1!2b1
# Or Street View Image Metadata API / embed check.

def check_pano_exists(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{lat}!4d{lng}!2d1000!3m10!2m2!1sen!2sUS!9m1!1b1!10b1!11m1!2e10!12m1!2b1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8', errors='ignore')
            # Extract pano_id
            match = re.search(r'\[\[null,null,(-?\d+\.\d+),(-?\d+\.\d+)\],\["([^"]+)"', data)
            if match:
                actual_lat, actual_lng, pano_id = match.group(1), match.group(2), match.group(3)
                return True, float(actual_lat), float(actual_lng), pano_id
            # Also check if pano string exists
            m2 = re.search(r'"([a-zA-Z0-9_-]{22,})"', data)
            if m2 and "apiv3" not in m2.group(1):
                return True, lat, lng, m2.group(1)
            return False, lat, lng, None
    except Exception as e:
        return False, lat, lng, str(e)

with open("locations.json") as f:
    locs = json.load(f)

for loc in locs[:5]:
    ok, slat, slng, pano = check_pano_exists(loc['lat'], loc['lng'])
    print(f"{loc['id']}: ok={ok}, pano={pano}")
