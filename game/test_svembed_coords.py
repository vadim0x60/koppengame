import urllib.request

test_coords = [
    (1.404355743497238, 110.3215053617324),   # Borneo
    (10.45243918559885, -84.01579635821369),  # Costa Rica
    (36.24538076237238, -116.8279266063727),  # Death valley
    (46.52862075451429, 10.45318592694539),   # Stelvio
    (-54.67730982797198, -67.88554676162855), # Tierra del Fuego
]

for lat, lng in test_coords:
    url = f"https://maps.google.com/maps?q={lat},{lng}&layer=c&cbll={lat},{lng}&cbp=11,0,0,0,0&output=svembed"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
    resp = urllib.request.urlopen(req)
    print(f"{lat}, {lng} -> svembed status: {resp.status}, length: {len(resp.read())}")
