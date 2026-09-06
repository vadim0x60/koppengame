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

# Candidate rural/scenic spots across all climate categories
candidates = [
    # --- GROUP A: TROPICAL ---
    # Af: Tropical Rainforest
    {
        "id": "borneo_semenggoh_rural",
        "name": "Borneo Rainforest Reserve Road",
        "country": "Malaysia (Sarawak)",
        "lat": 1.4012, "lng": 110.3185,
        "koppen_code": "Af", "koppen_group": "A", "koppen_name": "Tropical Rainforest climate",
        "hints": ["Equatorial rainforest corridor with dense broadleaf canopy and epiphytes", "Heavy red clay tropical soil", "Consistent year-round warmth and precipitation with no dry month under 60mm"],
        "explanation": "Af: Deep in Malaysian Borneo, rainfall exceeds 60mm every single month, sustaining lush multi-storied tropical rainforest."
    },
    {
        "id": "costa_rica_sarapiqui",
        "name": "Sarapiquí Lowland Rainforest Corridor",
        "country": "Costa Rica",
        "lat": 10.4532, "lng": -84.0156,
        "koppen_code": "Af", "koppen_group": "A", "koppen_name": "Tropical Rainforest climate",
        "hints": ["Lowland Caribbean slope with dense evergreen jungle", "Bromeliads, heliconias, and palms lining the road", "High atmospheric humidity and over 4,000mm annual precipitation"],
        "explanation": "Af: Costa Rica's Caribbean lowlands receive moisture-laden trade winds year-round without any true dry season."
    },
    {
        "id": "daintree_cape_tribulation",
        "name": "Cape Tribulation Rainforest Road",
        "country": "Australia",
        "lat": -16.0825, "lng": 145.4498,
        "koppen_code": "Af", "koppen_group": "A", "koppen_name": "Tropical Rainforest climate",
        "hints": ["Ancient tropical rainforest running directly down to the coast", "Dense canopy of fan palms, cycads, and strangler figs", "Tropical warmth with high monthly rain throughout the year"],
        "explanation": "Af: The Daintree is Australia's oldest tropical rainforest, receiving massive orographic rainfall from Pacific trade winds."
    },

    # Am: Tropical Monsoon
    {
        "id": "phuket_interior_hills",
        "name": "Khao Phra Thaeo Foothills",
        "country": "Thailand",
        "lat": 8.0315, "lng": 98.3725,
        "koppen_code": "Am", "koppen_group": "A", "koppen_name": "Tropical Monsoon climate",
        "hints": ["Lush tropical rubber and bamboo thickets", "Brief drier winter spell followed by relentless southwest monsoon deluges", "Undulating coastal hills covered in dense green growth"],
        "explanation": "Am: Tropical monsoon climate with intense seasonal deluge alternating with a short, distinct dry season."
    },
    {
        "id": "western_ghats_munnar_rural",
        "name": "Western Ghats Gap Road, Idukki",
        "country": "India",
        "lat": 10.0154, "lng": 77.0621,
        "koppen_code": "Am", "koppen_group": "A", "koppen_name": "Tropical Monsoon climate",
        "hints": ["Steep mist-shrouded mountain flanks with shola-grassland mosaic and tea hills", "Deluging southwest monsoon rains from June to September", "Deep green tropical mountain vegetation"],
        "explanation": "Am: The Western Ghats capture moisture from the Arabian Sea, creating some of the world's most intense tropical monsoons."
    },

    # Aw: Tropical Savanna
    {
        "id": "kakadu_jabiru_bush",
        "name": "Arnhem Highway, Kakadu Savannah Basin",
        "country": "Australia",
        "lat": -12.6712, "lng": 132.8341,
        "koppen_code": "Aw", "koppen_group": "A", "koppen_name": "Tropical Savanna (Wet/Dry)",
        "hints": ["Open eucalyptus savanna woodland and tall dry spear grass", "Flat tropical plain with magnetic termite mounds", "Severe winter drought followed by monsoonal summer floods"],
        "explanation": "Aw: Northern Australia's tropical savannas have an extreme wet/dry cycle: months of total drought followed by torrential monsoonal rains."
    },
    {
        "id": "cerrado_chapada_dos_veadeiros",
        "name": "GO-118 Highway, Chapada Plateau",
        "country": "Brazil",
        "lat": -14.1352, "lng": -47.5182,
        "koppen_code": "Aw", "koppen_group": "A", "koppen_name": "Tropical Savanna (Wet/Dry)",
        "hints": ["Twisted trees with thick, corky bark and tough sclerophyllous leaves", "Expansive savanna grassland plateau under vast sky", "Extreme parching during dry southern winter (June-August)"],
        "explanation": "Aw: Brazil's Cerrado plateau experiences high tropical heat and a severe winter dry period followed by summer downpours."
    },
    {
        "id": "kenya_rift_valley_rural",
        "name": "Mai Mahiu Escarpment Route, Great Rift Valley",
        "country": "Kenya",
        "lat": -0.9852, "lng": 36.5812,
        "koppen_code": "Aw", "koppen_group": "A", "koppen_name": "Tropical Savanna climate",
        "hints": ["Yellow-barked acacia trees (fever tree) and dry scrub grassland", "Dramatic volcanic rift valley escarpment", "Equatorial bimodal wet and dry seasons"],
        "explanation": "Aw: Tropical savanna in the East African Rift with prolonged dry periods and open acacia-dotted grasslands."
    },

    # --- GROUP B: ARID & SEMI-ARID ---
    # BWh: Hot Desert
    {
        "id": "death_valley_artist_drive",
        "name": "Badwater Basin Flats, Death Valley",
        "country": "United States",
        "lat": 36.2425, "lng": -116.8251,
        "koppen_code": "BWh", "koppen_group": "B", "koppen_name": "Hot Desert climate",
        "hints": ["Bleached salt pan flats and hyper-arid alluvial gravel fans", "Virtually zero vegetation save for isolated saltbush and creosote", "Extreme summer temperatures frequently exceeding 45°C"],
        "explanation": "BWh: Death Valley is a textbook hot desert where potential evaporation exceeds precipitation by more than thirtyfold."
    },
    {
        "id": "stuart_hwy_central_aus",
        "name": "Stuart Highway, Marla Plains",
        "country": "Australia",
        "lat": -27.3015, "lng": 133.6215,
        "koppen_code": "BWh", "koppen_group": "B", "koppen_name": "Hot Desert climate",
        "hints": ["Bright crimson-red sand and ironstone gibber desert", "Sparse clumps of spinifex grass and mulga scrub", "Subtropical high-pressure belt with searing summer heat"],
        "explanation": "BWh: The Australian Red Centre is dominated by the subtropical ridge, producing hot, arid desert conditions."
    },
    {
        "id": "baja_desert_vizcaino",
        "name": "Carretera Transpeninsular, Vizcaíno Biosphere",
        "country": "Mexico",
        "lat": 27.6521, "lng": -113.4512,
        "koppen_code": "BWh", "koppen_group": "B", "koppen_name": "Hot Desert climate",
        "hints": ["Spectacular endemic cardón cacti and yucca-like cirio trees", "Rocky volcanic gravel under blinding desert sunshine", "Extremely low annual precipitation (<100mm)"],
        "explanation": "BWh: The Vizcaíno desert sits under persistent subtropical subsiding air, creating an arid, cactus-rich hot desert."
    },

    # BWk: Cold Desert
    {
        "id": "salardeatacama_chile",
        "name": "Ruta 23, San Pedro Altiplano Border",
        "country": "Chile",
        "lat": -23.1254, "lng": -68.0412,
        "koppen_code": "BWk", "koppen_group": "B", "koppen_name": "Cold Desert climate",
        "hints": ["Hyper-arid volcanic plateau with white crusty borax/salt deposits", "Bare reddish-brown volcanic cones under deep cobalt blue skies", "Crisp thin air with freezing night temperatures even in summer"],
        "explanation": "BWk: The high Atacama is a cold desert (mean temp <18°C), desiccated by the Humboldt Current and rain-shadowed by the Andes."
    },
    {
        "id": "mongolia_south_gobi_paved",
        "name": "Mandalgovi-Dalandzadgad Highway, Gobi Steppe",
        "country": "Mongolia",
        "lat": 44.5214, "lng": 105.7852,
        "koppen_code": "BWk", "koppen_group": "B", "koppen_name": "Cold Desert climate",
        "hints": ["Flat gravel plain with dwarf saxaul and allium clumps", "Vast empty horizons with distant flat-topped ridges", "Severe sub-zero winter freeze (-25°C) and hot arid summers"],
        "explanation": "BWk: The Gobi has a cold desert climate: extreme continentality far from oceans, severe winter freeze, and minimal precipitation."
    },

    # BSk: Cold Semi-Arid (Steppe)
    {
        "id": "ruta40_treslagos_patagonia",
        "name": "Ruta 40, Santa Cruz Gravel Steppe",
        "country": "Argentina",
        "lat": -49.6012, "lng": -71.4521,
        "koppen_code": "BSk", "koppen_group": "B", "koppen_name": "Cold Semi-Arid (Steppe) climate",
        "hints": ["Endless windswept coirón bunchgrass and thorny mata negra shrubs", "Flat basalt plateaus under relentless dry westerly gales", "Cold dry winters with Andean rain shadow blocking Pacific moisture"],
        "explanation": "BSk: The Patagonian steppe lies in the rain shadow of the Southern Andes, enduring cold dry winds and sparse rainfall."
    },
    {
        "id": "red_desert_wyoming_hwy",
        "name": "WYO 789, Continental Divide Basin",
        "country": "United States",
        "lat": 41.9852, "lng": -107.9521,
        "koppen_code": "BSk", "koppen_group": "B", "koppen_name": "Cold Semi-Arid (Steppe) climate",
        "hints": ["Endless expanse of silver-gray big sagebrush and greasewood", "High plateau elevation (~2,000m) with cold howling winter winds", "Dry steppe receiving 200-300mm annual precipitation with winter snow"],
        "explanation": "BSk: Wyoming's intermountain basins feature cold semi-arid steppe climates characterized by freezing winters and dry summers."
    },

    # BSh: Hot Semi-Arid (Steppe)
    {
        "id": "senegal_n2_sahel",
        "name": "N2 Highway, Podor Ferlo Transition",
        "country": "Senegal",
        "lat": 16.4812, "lng": -14.9214,
        "koppen_code": "BSh", "koppen_group": "B", "koppen_name": "Hot Semi-Arid (Steppe) climate",
        "hints": ["Sparse thorny acacia trees on pale sandy-clay soil", "Straw-colored dry annual grass during the 9-month dry period", "Mean annual temperature well above 25°C with a short summer rain spell"],
        "explanation": "BSh: The Sahelian transition zone between the Sahara and savanna experiences high year-round heat and brief semi-arid rainfall."
    },

    # --- GROUP C: TEMPERATE ---
    # Csa: Hot-summer Mediterranean
    {
        "id": "andalucia_montana_pass",
        "name": "A-369 Serranía de Ronda Route",
        "country": "Spain",
        "lat": 36.6214, "lng": -5.3012,
        "koppen_code": "Csa", "koppen_group": "C", "koppen_name": "Hot-summer Mediterranean climate",
        "hints": ["Limestone karst ridges, ancient olive groves, and cork oak woods", "Baked golden-brown summer grass under clear cloudless skies", "Long bone-dry hot summers and mild rainy winters"],
        "explanation": "Csa: Classic Mediterranean climate of southern Spain featuring hot, dry summers and wet, temperate winters."
    },
    {
        "id": "crete_white_mountains",
        "name": "Omalos Plateau Mountain Road, Crete",
        "country": "Greece",
        "lat": 35.3412, "lng": 23.9012,
        "koppen_code": "Csa", "koppen_group": "C", "koppen_name": "Hot-summer Mediterranean climate",
        "hints": ["Rough limestone crags with aromatic thyme, spiny phrygana, and cypress", "Deep Mediterranean sunlight with zero summer rainfall", "Mild winter frontal storms from the Mediterranean Sea"],
        "explanation": "Csa: Island Mediterranean climate with dry, scorching summer months and winter precipitation."
    },

    # Csb: Warm-summer Mediterranean
    {
        "id": "maule_sclerophyll_chile",
        "name": "Ruta 126, Coastal Range Sclerophyll Woodland",
        "country": "Chile",
        "lat": -35.8521, "lng": -72.3124,
        "koppen_code": "Csb", "koppen_group": "C", "koppen_name": "Warm-summer Mediterranean climate",
        "hints": ["Matorral scrub, quillay trees, and espino savanna on rolling hills", "Dry summer conditions tempered by cool Pacific marine winds", "Warmest month averages below 22°C due to coastal upwelling"],
        "explanation": "Csb: Central Chile's coastal range has dry Mediterranean summers moderated by cool Pacific sea breezes."
    },

    # Cfa: Humid Subtropical
    {
        "id": "ozark_mark_twain_forest",
        "name": "MO-19 Ozark Scenic Byway",
        "country": "United States",
        "lat": 37.3812, "lng": -91.3812,
        "koppen_code": "Cfa", "koppen_group": "C", "koppen_name": "Humid Subtropical climate",
        "hints": ["Dense hardwood forest of white oak, hickory, and shortleaf pine", "Humid, thunderstorm-prone summer days and temperate winters", "Abundant rainfall well-distributed across all four seasons"],
        "explanation": "Cfa: The southeastern United States interior features hot, humid summers fueled by Gulf moisture and mild-to-cool winters."
    },
    {
        "id": "uruguay_ruta8_pampa",
        "name": "Ruta 8, Lavalleja Rolling Pastures",
        "country": "Uruguay",
        "lat": -34.2512, "lng": -55.1214,
        "koppen_code": "Cfa", "koppen_group": "C", "koppen_name": "Humid Subtropical climate",
        "hints": ["Vast rolling green pampa grasslands dotted with cattle", "Rich perennial green turf without a dry season", "Warm humid summers and mild, frost-free winters"],
        "explanation": "Cfa: The Rio de la Plata grassland basin has warm humid summers and uniform precipitation year-round without drought."
    },

    # Cfb: Temperate Oceanic
    {
        "id": "snowy_mountains_subalpine",
        "name": "Snowy Mountains Highway, Kiandra Plain",
        "country": "Australia",
        "lat": -35.8521, "lng": 148.5124,
        "koppen_code": "Cfb", "koppen_group": "C", "koppen_name": "Temperate Oceanic climate",
        "hints": ["Rolling subalpine grasslands bordered by twisted snow gums (Eucalyptus pauciflora)", "Lush perennial grass with dependable year-round precipitation", "Cool pleasant summers and cold frosty winters with snow cover"],
        "explanation": "Cfb: The Australian Alps receive consistent maritime precipitation year-round with cool, mild summers."
    },
    {
        "id": "wales_elad_valley_moor",
        "name": "Elan Valley Mountain Road, Cambrian Hills",
        "country": "United Kingdom",
        "lat": 52.2812, "lng": -3.6521,
        "koppen_code": "Cfb", "koppen_group": "C", "koppen_name": "Temperate Oceanic climate",
        "hints": ["Heather moorland, bracken, and rolling sheep-grazed green fells", "Overcast skies, frequent Atlantic drizzle, and slate stone bridges", "Mild oceanic winters and cool damp summers rarely exceeding 20°C"],
        "explanation": "Cfb: Classic British oceanic climate: heavily moderated by the Atlantic Ocean, high cloudiness, no dry season."
    },

    # Cfc: Subpolar Oceanic
    {
        "id": "faroe_islands_streymoy",
        "name": "Route 10, Oyggjarvegur Mountain Route",
        "country": "Faroe Islands",
        "lat": 62.0812, "lng": -6.9124,
        "koppen_code": "Cfc", "koppen_group": "C", "koppen_name": "Subpolar Oceanic climate",
        "hints": ["Steep, totally treeless basalt mountains plunging into coastal fjords", "Emerald-green peat turf and roaring waterfalls under heavy Atlantic mist", "Cool summer temperatures where warmest month barely reaches 11°C"],
        "explanation": "Cfc: The Faroe Islands have a subpolar oceanic climate with very cool summers, mild wet winters, and relentless ocean winds."
    },

    # --- GROUP D: CONTINENTAL ---
    # Dfa: Hot-summer Humid Continental
    {
        "id": "badlands_sage_creek",
        "name": "Sage Creek Basin Road, Badlands",
        "country": "United States",
        "lat": 43.8821, "lng": -102.3812,
        "koppen_code": "Dfa", "koppen_group": "D", "koppen_name": "Hot-summer Humid Continental climate",
        "hints": ["Layered clay sedimentary badland buttes rising above mixed-grass prairie", "Huge seasonal extremes: -25°C winter blizzards to +38°C summer heatwaves", "Warmest summer month averages above 22°C"],
        "explanation": "Dfa: The Northern Great Plains have a hot-summer continental climate with vast temperature swings and freezing winters."
    },

    # Dfb: Warm-summer Humid Continental
    {
        "id": "karelia_finland_taiga",
        "name": "Route 88, Lake Oulujärvi Conifer Belt",
        "country": "Finland",
        "lat": 64.3821, "lng": 27.1824,
        "koppen_code": "Dfb", "koppen_group": "D", "koppen_name": "Warm-summer Humid Continental climate",
        "hints": ["Towering stands of Scots pine, Norway spruce, and silver birch", "Mossy forest floor with glacial granite boulders and dark lake water", "Four distinct seasons with snowy winters and pleasant mild summers"],
        "explanation": "Dfb: The central Finnish boreal transition zone has 4+ months above 10°C, snowy winters, and moderate summer warmth."
    },

    # Dfc: Subarctic (Taiga)
    {
        "id": "taylor_hwy_alaska",
        "name": "Taylor Highway, Interior Spruce Flats",
        "country": "United States",
        "lat": 64.0812, "lng": -142.1824,
        "koppen_code": "Dfc", "koppen_group": "D", "koppen_name": "Subarctic (Taiga) climate",
        "hints": ["Spindly black spruce muskeg on permafrost ground ('drunken forest')", "Caribou moss (lichen) and low dwarf birch understory", "Only 1 to 3 months with mean temperatures above 10°C; severe winter freeze"],
        "explanation": "Dfc: The interior Alaskan taiga endures prolonged sub-zero winters with a short, cool growing season."
    },
    {
        "id": "rovaniemi_rural_lapland",
        "name": "Route 79, Lapland Boreal Forest",
        "country": "Finland",
        "lat": 66.8521, "lng": 25.1214,
        "koppen_code": "Dfc", "koppen_group": "D", "koppen_name": "Subarctic (Taiga) climate",
        "hints": ["Spruce and pine taiga just south of the treeline", "Snow cover lasting from October through May", "Short, cool summer with only 1-2 months averaging above 10°C"],
        "explanation": "Dfc: Lapland's subarctic boreal forest has long, freezing winters and short, cool summer periods."
    },

    # Dsb: Dry-summer Continental
    {
        "id": "columbia_basin_simcoe",
        "name": "US-97, Simcoe Mountain Foothills",
        "country": "United States",
        "lat": 45.9812, "lng": -120.8812,
        "koppen_code": "Dsb", "koppen_group": "D", "koppen_name": "Dry-summer Continental climate",
        "hints": ["Open ponderosa pine savanna meeting dry basalt steppe", "Dry golden grass in summer under Cascade mountain rain shadow", "Cold snowy winter temperatures well below freezing"],
        "explanation": "Dsb: Rain-shadowed slopes of the Pacific Northwest mountains exhibit continental freezing winters combined with Mediterranean dry summers."
    },

    # --- GROUP E: POLAR & ALPINE ---
    # ET: Tundra
    {
        "id": "iceland_ringroad_jokulsarlon",
        "name": "Route 1, Vatnajökull Glacial Outwash Plain",
        "country": "Iceland",
        "lat": 64.0512, "lng": -16.1824,
        "koppen_code": "ET", "koppen_group": "E", "koppen_name": "Tundra climate",
        "hints": ["Black volcanic sand, glacial braided streams, and moss-covered moraines", "Massive ice cap and glaciers visible in background; completely treeless", "Warmest month temperature fails to reach 10°C"],
        "explanation": "ET: The coastal outwash plains below Vatnajökull have a tundra climate where maritime Arctic air keeps summer averages below 10°C."
    },
    {
        "id": "passo_dello_stelvio_italy",
        "name": "SS38 Stelvio Pass Alpine Scree (2,757m)",
        "country": "Italy",
        "lat": 46.5286, "lng": 10.4532,
        "koppen_code": "ET", "koppen_group": "E", "koppen_name": "Alpine Tundra climate",
        "hints": ["High alpine scree, bare limestone crags, and residual summer snowdrifts", "Far above the Alpine treeline with hardy cushion plants and lichen", "Severe sub-zero winter freeze and short, cold alpine summer (<10°C)"],
        "explanation": "ET: High elevation in the Italian Alps produces an alpine tundra climate matching polar tundra criteria."
    },
    {
        "id": "passo_garibaldi_tierra_del_fuego",
        "name": "Ruta 3, Paso Garibaldi, Fuegian Andes",
        "country": "Argentina",
        "lat": -54.6821, "lng": -67.8812,
        "koppen_code": "ET", "koppen_group": "E", "koppen_name": "Tundra / Alpine Subpolar climate",
        "hints": ["Wind-sheared krummholz (stunted southern beech) giving way to rocky scree", "Glacial mountain pass with subantarctic peat bogs and snow patches", "Relentless subantarctic winds; summer temperatures rarely exceed 9°C"],
        "explanation": "ET: High latitude and mountain pass elevation produce a tundra climate with no month averaging above 10°C."
    },
    {
        "id": "svalbard_longyearbyen_valley",
        "name": "Adventdalen Arctic Valley Track",
        "country": "Norway (Svalbard)",
        "lat": 78.2012, "lng": 15.8214,
        "koppen_code": "ET", "koppen_group": "E", "koppen_name": "Tundra climate",
        "hints": ["Barren high-Arctic permafrost valley framed by flat-topped snowy mountains", "Arctic dwarf willow and polar mosses hugging the gravel ground", "Midnight sun in summer with peak July averages around 5-7°C"],
        "explanation": "ET: High Arctic archipelago (78°N) where permafrost is continuous and warmest month averages remain between 0°C and 10°C."
    }
]

print(f"Testing {len(candidates)} candidate locations...")
verified = []

for c in candidates:
    ok, slat, slng, pano = verify_streetview(c["lat"], c["lng"])
    print(f"[{'PASS' if ok else 'FAIL'}] {c['id']} ({c['koppen_code']}) -> {slat}, {slng}, pano={pano}")
    if ok:
        c["lat"] = slat
        c["lng"] = slng
        c["pano_id"] = pano
        verified.append(c)
    time.sleep(0.1)

print(f"\nSuccessfully verified {len(verified)} out of {len(candidates)} locations.")
with open("verified_locations.json", "w") as f:
    json.dump(verified, f, indent=2)
