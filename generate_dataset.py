import json
import collections
import random
import pycountry
import kgcpy

# 1. Setup Köppen lookup
num_to_zone = dict(zip(kgcpy.kg_zoneNum_df['zoneNum'], kgcpy.kg_zoneNum_df['kg_zone']))
img = kgcpy.img
w, h = img.size

# Detailed climate names and botanical descriptions
CLIMATE_DETAILS = {
    'Af': {
        'group': 'A',
        'name': 'Tropical Rainforest climate',
        'summary': 'Constant high temps, precipitation >60mm each month, multi-tiered evergreen canopy.',
        'hints': [
            'Dense multi-tiered evergreen jungle canopy and lush epiphytes',
            'Deep reddish laterite / oxisol tropical soil',
            'High atmospheric humidity with no distinct dry month'
        ],
        'explanation_template': "Located near equatorial latitudes, this area experiences consistent high temperatures (all months >= 18°C) and abundant year-round convective rainfall without a dry season."
    },
    'Am': {
        'group': 'A',
        'name': 'Tropical Monsoon climate',
        'summary': 'Intense rainy season with a short dry interval, high annual totals.',
        'hints': [
            'Dense semi-evergreen forest and bamboo thickets',
            'Strong wet/dry contrast with brief drier winter and monsoon downpours',
            'Tropical warmth year-round with massive annual rainfall totals'
        ],
        'explanation_template': "Marked by a brief dry interval followed by an intense rainy season driven by seasonal wind shifts and ITCZ migration, sustaining tropical rainforest flora."
    },
    'Aw': {
        'group': 'A',
        'name': 'Tropical Savanna (Wet/Dry) climate',
        'summary': 'Pronounced wet summer and bone-dry winter, drought-adapted trees and grassland.',
        'hints': [
            'Open savanna grassland dotted with drought-adapted, corky-bark trees or acacias',
            'Marked seasonal drying with severe winter drought followed by summer rains',
            'Tropical temperatures throughout the year'
        ],
        'explanation_template': "Characterized by pronounced seasonality with a dry winter season (driest month < 60mm) and high tropical warmth all year round."
    },
    'As': {
        'group': 'A',
        'name': 'Tropical Savanna (Dry Summer) climate',
        'summary': 'Tropical climate with a dry season during high-sun months.',
        'hints': [
            'Tropical deciduous woodland or dry scrub savanna',
            'Unusual dry summer season contrasting with rainy winter/equinoctial months',
            'Consistently high tropical temperatures without freeze'
        ],
        'explanation_template': "A rare tropical savanna regime where rain occurs primarily during the low-sun season while the high-sun summer experiences drought."
    },
    'BWh': {
        'group': 'B',
        'name': 'Hot Desert climate',
        'summary': 'Extremely arid, mean annual temp >= 18°C, sparse succulents/gravel plains.',
        'hints': [
            'Hyper-arid landscape with gravel plains, sand dunes, or desert pavement',
            'Extremely sparse xerophytic scrub, saltbush, or succulents',
            'Searing summer temperatures under persistent subtropical high pressure'
        ],
        'explanation_template': "Subtropical high-pressure subsiding air keeps precipitation extremely low while mean annual temperatures exceed 18°C."
    },
    'BWk': {
        'group': 'B',
        'name': 'Cold Desert climate',
        'summary': 'Arid, mean annual temp < 18°C, freezing continental winters or cool fog upwelling.',
        'hints': [
            'Barren arid plains or gravel basins with sparse sagebrush or halophytes',
            'Cold or freezing winter conditions despite scarce precipitation',
            'Strong diurnal temperature swings and high solar radiation'
        ],
        'explanation_template': "Arid conditions where mean annual temperature is below 18°C, often located in continental interiors or high-altitude rain shadows."
    },
    'BSh': {
        'group': 'B',
        'name': 'Hot Semi-Arid (Steppe) climate',
        'summary': 'Transitional dry scrub/grassland, mean annual temp >= 18°C.',
        'hints': [
            'Short grasses, thorny acacia or mesquite scrub, and dry wash beds',
            'Mean annual temperature >= 18°C with prolonged dry season',
            'Transitional landscape between savanna and true desert'
        ],
        'explanation_template': "A transitional steppe climate with high mean temperatures (>= 18°C) where potential evapotranspiration exceeds rainfall but supports hardy grassland and shrubs."
    },
    'BSk': {
        'group': 'B',
        'name': 'Cold Semi-Arid (Steppe) climate',
        'summary': 'Steppe with cold snowy winters and dry, warm to hot summers.',
        'hints': [
            'Expansive windswept bunchgrass steppe and low sagebrush',
            'Cold snowy winters paired with dry, warm-to-hot summers',
            'Continental interior or rain-shadowed plateau topography'
        ],
        'explanation_template': "Mid-latitude steppe with freezing winter temperatures and mean annual temperature under 18°C, typical of continental interiors and leeward basins."
    },
    'Csa': {
        'group': 'C',
        'name': 'Hot-summer Mediterranean climate',
        'summary': 'Hot, dry summers and mild, wet winters; sclerophyllous maquis/olive trees.',
        'hints': [
            'Sclerophyllous evergreen scrub (maquis/chaparral), olive trees, or stone pines',
            'Sun-parched golden grasses in summer under cloudless skies',
            'Hot summer (warmest month > 22°C) and mild rainy winter'
        ],
        'explanation_template': "Classic dry-summer subtropical climate with hot, drought-stressed summers (>22°C) and mild cyclonic winter rainfall."
    },
    'Csb': {
        'group': 'C',
        'name': 'Warm-summer Mediterranean climate',
        'summary': 'Dry summers tempered by cool coastal marine fog/currents.',
        'hints': [
            'Dry summer Mediterranean vegetation tempered by cool oceanic breezes or fog',
            'Warm mild summer (warmest month < 22°C) without extreme heat',
            'Sclerophyllous shrubs, coastal conifers, or eucalyptus groves'
        ],
        'explanation_template': "Coastal or highland Mediterranean regime where cool ocean currents moderate summer warmth (warmest month < 22°C) while maintaining dry summers."
    },
    'Csc': {
        'group': 'C',
        'name': 'Cold-summer Mediterranean climate',
        'summary': 'High-altitude dry-summer climate with short, cool summers.',
        'hints': [
            'High elevation subalpine woodland or alpine meadows',
            'Dry summer conditions with short, cool summers (fewer than 4 months > 10°C)',
            'Cold snowy winters'
        ],
        'explanation_template': "A rare highland variant of the Mediterranean climate where high elevation results in short, cool summers and dry high-sun months."
    },
    'Cfa': {
        'group': 'C',
        'name': 'Humid Subtropical climate',
        'summary': 'Hot humid summers with frequent storms, mild winters without a dry season.',
        'hints': [
            'Lush broadleaf and mixed pine forests, humid understory',
            'Abundant year-round rainfall with no dry season',
            'Hot muggy summers (warmest month > 22°C) and mild winters'
        ],
        'explanation_template': "Located primarily on eastern continental margins, receiving warm moist maritime air in summer and consistent precipitation year-round."
    },
    'Cfb': {
        'group': 'C',
        'name': 'Temperate Oceanic climate',
        'summary': 'Mild winters and cool-to-warm summers, frequent cloud/drizzle year-round.',
        'hints': [
            'Lush green pastures, deciduous oak/beech woodland, or fern gullies',
            'Mild winters, cool-to-warm summers (warmest month < 22°C)',
            'Frequent cloud cover, drizzle, and absence of a dry season'
        ],
        'explanation_template': "Dominated by prevailing westerlies and ocean currents that moderate seasonal temperature swings, keeping all months temperate with steady precipitation."
    },
    'Cfc': {
        'group': 'C',
        'name': 'Subpolar Oceanic climate',
        'summary': 'Maritime subpolar with cool short summers (1-3 months >10°C) and mild wet winters.',
        'hints': [
            'Windswept maritime heathland, dwarf birch, mossy moorlands, and craggy sea fjords',
            'Cool, short summer with only 1 to 3 months averaging above 10°C',
            'Mild winter for the high latitude due to ocean moderating effect'
        ],
        'explanation_template': "High-latitude coastal margins where maritime influence keeps winters relatively mild, but cool summers restrict tree growth to hardy scrub and heath."
    },
    'Cwa': {
        'group': 'C',
        'name': 'Monsoon Humid Subtropical climate',
        'summary': 'Hot wet summers driven by monsoon winds, paired with mild dry winters.',
        'hints': [
            'Subtropical mixed forest, bamboo, and terrace agriculture',
            'Hot rainy summer monsoon contrasted with sunny dry winter',
            'Warmest month > 22°C, coldest month between -3°C and 18°C'
        ],
        'explanation_template': "Summer monsoonal downpours deliver over 90% of annual rain, while winter is sunny and dry under continental high pressure."
    },
    'Cwb': {
        'group': 'C',
        'name': 'Subtropical Highland (Dry Winter) climate',
        'summary': 'Highland temperate climate with wet summers and cool, dry sunny winters.',
        'hints': [
            'High plateau or mountain valleys with pine, cypress, or highland savanna',
            'Comfortably mild year-round temperatures due to high elevation',
            'Rainy summer paired with crisp, dry sunny winters'
        ],
        'explanation_template': "Tropical/subtropical latitudes at high elevations (1,500m - 2,800m) resulting in spring-like temperatures year-round with summer rains and dry winters."
    },
    'Cwc': {
        'group': 'C',
        'name': 'Cold Subtropical Highland climate',
        'summary': 'High elevation tropical highlands with short, cool summers.',
        'hints': [
            'High Andean or Himalayan páramo / puna plateau shrubs and bunchgrass',
            'Fewer than 4 months with mean temperature above 10°C',
            'Cold dry winters and brief cool wet summer season'
        ],
        'explanation_template': "High-altitude tropical mountain slopes with cool short summers and dry winter seasons near the alpine tree line."
    },
    'Dfa': {
        'group': 'D',
        'name': 'Hot-summer Humid Continental climate',
        'summary': 'Snowy cold winters, hot humid summers (>22°C warmest month).',
        'hints': [
            'Deciduous oak-hickory woodland, corn belts, or tallgrass prairie',
            'Freezing snowy winters (coldest month < -3°C)',
            'Hot humid summers with mean temperature exceeding 22°C'
        ],
        'explanation_template': "Severe continental freeze in winter combined with hot, convective summer weather with mean temperatures above 22°C."
    },
    'Dfb': {
        'group': 'D',
        'name': 'Warm-summer Humid Continental climate',
        'summary': 'Snowy cold winters, warm mild summers (warmest month <22°C).',
        'hints': [
            'Mixed forest of birch, maple, pine, and spruce',
            'Prolonged snowy winter freeze and pleasant mild summers (< 22°C warmest month)',
            'Reliable precipitation year-round without drought'
        ],
        'explanation_template': "Classic boreal margin / northern continental climate with long cold winters and warm, pleasant summers supporting mixed woodlands."
    },
    'Dfc': {
        'group': 'D',
        'name': 'Subarctic (Taiga) climate',
        'summary': 'Very long cold winters, 1-3 short cool summer months; boreal spruce/pine.',
        'hints': [
            'Endless needleleaf boreal forest (taiga) of spruce, larch, and fir',
            'Only 1 to 3 months with mean temperature above 10°C',
            'Long bitter winters with deep snowpack lasting 6+ months'
        ],
        'explanation_template': "Vast high-latitude boreal zone with severe sub-zero winter freezes and short, cool summer growing seasons."
    },
    'Dfd': {
        'group': 'D',
        'name': 'Extremely Cold Subarctic climate',
        'summary': 'Extreme subarctic climate with coldest month below -38°C.',
        'hints': [
            'Stunted dahurian larch forest growing on continuous permafrost',
            'Extreme continental temperature swings exceeding 60°C annually',
            'Coldest month mean below -38°C with bone-chilling Siberian air'
        ],
        'explanation_template': "Hyper-continental eastern Siberia where winter temperatures drop below -50°C (coldest month < -38°C) over deep permafrost."
    },
    'Dsa': {
        'group': 'D',
        'name': 'Hot-summer Mediterranean Continental climate',
        'summary': 'Continental freezing winters paired with hot dry Mediterranean summers.',
        'hints': [
            'Dry interior mountain plateau with scrub oaks, junipers, and dry grasslands',
            'Freezing continental snowy winter paired with hot, bone-dry summer',
            'Warmest month > 22°C'
        ],
        'explanation_template': "Interior highland basins that experience continental freezing winters alongside Mediterranean summer droughts."
    },
    'Dsb': {
        'group': 'D',
        'name': 'Warm-summer Mediterranean Continental climate',
        'summary': 'Freezing continental winters paired with dry Mediterranean summers in rain shadow.',
        'hints': [
            'Open stands of ponderosa pine, bitterbrush, and dry volcanic plateaus',
            'Rain-shadowed leeward slopes with freezing snowy winters and dry summers',
            'Warm mild summer (warmest month < 22°C)'
        ],
        'explanation_template': "Rain-shadowed interior mountain plateaus featuring cold freezing winters and warm, dry summer drought."
    },
    'Dsc': {
        'group': 'D',
        'name': 'Dry-summer Subarctic climate',
        'summary': 'High-latitude or alpine subarctic with brief dry summer.',
        'hints': [
            'Subalpine conifers and dwarf shrubs near tree line',
            'Short cool dry summer with 1 to 3 months above 10°C',
            'Long, cold snowy winters'
        ],
        'explanation_template': "High-elevation or subarctic regions combining short, cool, dry summers with cold snowy winters."
    },
    'Dsd': {
        'group': 'D',
        'name': 'Extremely Cold Dry-summer Subarctic climate',
        'summary': 'Extreme winter cold paired with dry summer drought.',
        'hints': [
            'Siberian interior taiga on permafrost',
            'Coldest month below -38°C',
            'Dry summer season'
        ],
        'explanation_template': "Rare hyper-continental climate in Siberian mountains with extreme winter lows and dry summers."
    },
    'Dwa': {
        'group': 'D',
        'name': 'Monsoon Hot Continental climate',
        'summary': 'Monsoon rainy summers and dry, intensely cold Siberian-influenced winters.',
        'hints': [
            'Deciduous oak-pine mixed forest and river plains',
            'Heavy summer monsoon deluge paired with bone-dry, sub-zero winter winds',
            'Hot summer (warmest month > 22°C)'
        ],
        'explanation_template': "East Asian continental regime where the Siberian high brings bitterly cold, dry winters while summer brings hot monsoon downpours."
    },
    'Dwb': {
        'group': 'D',
        'name': 'Monsoon Warm Continental climate',
        'summary': 'Warm rainy summer monsoon and dry, freezing continental winters.',
        'hints': [
            'Larch, birch, and mixed temperate/boreal woodlands',
            'Summer monsoon rain contrasted with dry, clear, freezing winter air',
            'Warmest month < 22°C, coldest month < -3°C'
        ],
        'explanation_template': "Northern East Asian continental climate with cold, dry winter anticyclones and pleasant, rainy monsoonal summers."
    },
    'Dwc': {
        'group': 'D',
        'name': 'Monsoon Subarctic climate',
        'summary': 'Subarctic taiga with dry freezing winters and short monsoonal summers.',
        'hints': [
            'Larch taiga and boggy permafrost terrain',
            'Only 1 to 3 months with mean temperature above 10°C',
            'Very dry, intensely cold winter season'
        ],
        'explanation_template': "High-latitude East Asia where the winter Siberian high creates extreme dry cold, while a brief summer brings monsoonal moisture."
    },
    'Dwd': {
        'group': 'D',
        'name': 'Extremely Cold Monsoon Subarctic climate',
        'summary': 'Extreme Siberian winter cold (coldest month <-38°C) and dry winters.',
        'hints': [
            'Dahurian larch taiga on deep permafrost',
            'World-record winter cold with coldest month below -38°C',
            'Dry winter anticyclone with clear, freezing skies'
        ],
        'explanation_template': "The pole of cold in northeastern Siberia, where winter temps plunge below -50°C under the Siberian high."
    },
    'ET': {
        'group': 'E',
        'name': 'Tundra (Polar/Alpine) climate',
        'summary': 'Treeless moss/lichen/scree terrain; warmest month between 0°C and 10°C.',
        'hints': [
            'Treeless landscape of dwarf willow, moss, lichen, or rocky scree',
            'Warmest month mean temperature remains between 0°C and 10°C',
            'Permafrost ground, glacial valleys, or alpine high-altitude pass'
        ],
        'explanation_template': "Polar or high-altitude alpine conditions where temperatures are too low for tree growth (warmest month between 0°C and 10°C)."
    },
    'EF': {
        'group': 'E',
        'name': 'Ice Cap climate',
        'summary': 'Perpetual frost; all 12 months average below 0°C with perpetual ice/snow.',
        'hints': [
            'Perpetual ice sheet, glacier, or perennial snowpack',
            'No month has an average temperature above 0°C',
            'No soil or vascular plant life; pure ice, snow, and rock'
        ],
        'explanation_template': "High alpine crests or polar ice caps where all 12 months average below 0°C, sustaining perpetual ice and snow."
    }
}

# 2. Load WorldGuessr pool
with open('/tmp/world-main.json') as f:
    world_locs = json.load(f)

print(f"Loaded {len(world_locs)} raw locations from world-main.")

# 3. Classify and group locations by verified Köppen code
by_zone = collections.defaultdict(list)
for loc in world_locs:
    lat, lng = loc['lat'], loc['lng']
    x = round((lng + 180) * w / 360 - 0.5)
    y = round(-(lat - 90) * h / 180 - 0.5)
    if 0 <= x < w and 0 <= y < h:
        pixel = img.getpixel((x, y))
        code = num_to_zone.get(pixel)
        if code and code != 'Ocean' and code in CLIMATE_DETAILS:
            by_zone[code].append(loc)

# 4. Load the existing curated 34 locations to preserve hand-tuned favorites
with open('locations.json') as f:
    existing_curated = json.load(f)

# Collect existing coordinates to avoid duplicates
existing_coords = set((round(l['lat'], 3), round(l['lng'], 3)) for l in existing_curated)

final_pool = list(existing_curated)
print(f"Starting with {len(final_pool)} hand-curated locations.")

# Target balance: up to 100 locations per common zone, and all available for rarer zones
random.seed(42)

for code in sorted(CLIMATE_DETAILS.keys()):
    locs = by_zone.get(code, [])
    random.shuffle(locs)
    current_count = sum(1 for l in final_pool if l['koppen_code'] == code)
    needed = max(0, min(len(locs), 100 - current_count))
    added = 0
    
    for loc in locs:
        if added >= needed:
            break
        key = (round(loc['lat'], 3), round(loc['lng'], 3))
        if key in existing_coords:
            continue
        
        country_code = loc.get('country', '')
        country_obj = pycountry.countries.get(alpha_2=country_code) if country_code else None
        country_name = country_obj.name if country_obj else country_code or 'Unknown'
        
        # Clean up country name if needed
        if ',' in country_name:
            country_name = country_name.split(',')[0]
            
        c_info = CLIMATE_DETAILS[code]
        pano = loc.get('panoId', '')
        item_id = f"loc_{code.lower()}_{pano[:8]}" if pano else f"loc_{code.lower()}_{added}"
        
        item = {
            "id": item_id,
            "name": f"Rural Route, {country_name}",
            "country": country_name,
            "lat": loc['lat'],
            "lng": loc['lng'],
            "koppen_code": code,
            "koppen_group": c_info['group'],
            "koppen_name": c_info['name'],
            "hints": c_info['hints'],
            "explanation": f"{code}: Located in {country_name}. {c_info['explanation_template']}",
            "pano_id": loc.get('panoId')
        }
        
        final_pool.append(item)
        existing_coords.add(key)
        added += 1

print(f"Total pool size after balancing: {len(final_pool)} locations.")

# Print distribution summary
counts = collections.Counter(l['koppen_code'] for l in final_pool)
print("Distribution by Köppen code:")
for code in sorted(counts.keys()):
    print(f"  {code:4s}: {counts[code]:4d}")

group_counts = collections.Counter(l['koppen_group'] for l in final_pool)
print("Distribution by Group:")
for g in sorted(group_counts.keys()):
    print(f"  Group {g}: {group_counts[g]:4d}")

with open('locations.json', 'w') as f:
    json.dump(final_pool, f, indent=2)

print("Saved updated pool to locations.json!")
