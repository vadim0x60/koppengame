import json

# Curated list of rural, non-obvious highways, backcountry roads, remote plateaus,
# and surprising climate zones where players MUST read the vegetation, soil, sky, and topography.
# Famous cities and obvious skylines are removed.

challenging_locations = [
    # --- GROUP A: TROPICAL (Af, Am, Aw) ---
    {
        "id": "borneo_sabah_rural",
        "name": "Sabah Interior Highway",
        "country": "Malaysia (Borneo)",
        "lat": 5.485123,
        "lng": 116.512340,
        "koppen_code": "Af",
        "koppen_group": "A",
        "koppen_name": "Tropical Rainforest climate",
        "hints": [
            "Dense multi-tiered dipterocarp jungle canopy and tree ferns",
            "Red laterite/oxisol clay soil exposed in road cuts",
            "Humid haze and high cloud build-up typical of the ITCZ"
        ],
        "explanation": "Af (Tropical Rainforest): Located deep in rural Borneo, rainfall exceeds 60mm every single month with heavy equatorial convection and no dry season."
    },
    {
        "id": "sumatra_trans_jungle",
        "name": "Trans-Sumatran Rural Route, Lampung",
        "country": "Indonesia",
        "lat": -5.102319,
        "lng": 105.152431,
        "koppen_code": "Af",
        "koppen_group": "A",
        "koppen_name": "Tropical Rainforest climate",
        "hints": [
            "Lush oil palm, wild banana, and broadleaf evergreen jungle margins",
            "Tropical cumulus towers; deep humidity visible on horizon",
            "Flat to undulating equatorial lowland terrain"
        ],
        "explanation": "Af: Equatorial Southeast Asia receives unrelenting warmth and heavy monthly rainfall sustaining perpetual evergreen broadleaf rainforests."
    },
    {
        "id": "western_ghats_monsoon_road",
        "name": "Western Ghats Escarpment Road, Kerala",
        "country": "India",
        "lat": 10.158420,
        "lng": 76.882140,
        "koppen_code": "Am",
        "koppen_group": "A",
        "koppen_name": "Tropical Monsoon climate",
        "hints": [
            "Dense semi-evergreen forest and bamboo thickets on dramatic steep slopes",
            "Orographic cloud banks and lush mossy cliffs",
            "Dry spell in winter followed by epic southwest monsoon deluge (>3,000mm/yr)"
        ],
        "explanation": "Am (Tropical Monsoon): Heavy seasonal precipitation driven by the summer Indian monsoon creates rainforest-level vegetation despite a short winter dry season."
    },
    {
        "id": "chiapas_mexico_rural",
        "name": "Lacandon Forest Edge, Chiapas",
        "country": "Mexico",
        "lat": 16.741250,
        "lng": -91.468210,
        "koppen_code": "Am",
        "koppen_group": "A",
        "koppen_name": "Tropical Monsoon climate",
        "hints": [
            "Karst limestone outcrops enveloped by tropical moist forest",
            "Foliage shows slight seasonal thinning unlike pure Af equatorial basins",
            "Heavy summer rainfall from Caribbean trade wind easterlies"
        ],
        "explanation": "Am: Southern Mexico's Caribbean slope receives intense tropical moisture, exceeding tropical savanna thresholds while retaining a brief dry spring."
    },
    {
        "id": "kakadu_highway_aus",
        "name": "Kakadu Highway, Arnhem Land Basin",
        "country": "Australia",
        "lat": -13.042100,
        "lng": 132.324500,
        "koppen_code": "Aw",
        "koppen_group": "A",
        "koppen_name": "Tropical Savanna (Wet/Dry)",
        "hints": [
            "Stunted eucalyptus (Darwin stringybark) and tall dry spear grass",
            "Termite mounds (magnetic/cathedral) dotted across flat plains",
            "Sun-bleached savanna indicating severe drought for half the year"
        ],
        "explanation": "Aw (Tropical Savanna): Extreme wet/dry alternation. Months of almost zero rainfall dry out the grassy understory until monsoonal rains flood the plains."
    },
    {
        "id": "cerrado_goias_brazil",
        "name": "Cerrado Biome Rural Highway, Goiás",
        "country": "Brazil",
        "lat": -14.283120,
        "lng": -49.381200,
        "koppen_code": "Aw",
        "koppen_group": "A",
        "koppen_name": "Tropical Savanna (Wet/Dry)",
        "hints": [
            "Gnarled, fire-adapted trees with thick corky bark and bent branches",
            "Coarse grassland between open scrub and scrubby woodlands",
            "Distinct seasonal parching typical of the Brazilian interior plateau"
        ],
        "explanation": "Aw: The Cerrado is one of the world's richest savannas, defined by intense summer downpours and several months of acute winter drought."
    },
    {
        "id": "rural_senegal_savanna",
        "name": "N1 Highway near Tambacounda",
        "country": "Senegal",
        "lat": 13.782410,
        "lng": -13.682100,
        "koppen_code": "Aw",
        "koppen_group": "A",
        "koppen_name": "Tropical Savanna (Sudanian)",
        "hints": [
            "Scattered baobab trees and thorny acacia bushes",
            "Bleached sandy-clay soil with dry straw-like annual grasses",
            "West African Sudanian savanna belt transition"
        ],
        "explanation": "Aw: The West African Sudanian zone has a short intense monsoonal wet season (July-September) followed by 8 months of parched dry tropical weather."
    },

    # --- GROUP B: ARID & SEMI-ARID (BWh, BWk, BSh, BSk) ---
    {
        "id": "atacama_route_5",
        "name": "Ruta 5, Antofagasta Region",
        "country": "Chile",
        "lat": -24.281900,
        "lng": -69.832100,
        "koppen_code": "BWk",
        "koppen_group": "B",
        "koppen_name": "Cold Desert climate",
        "hints": [
            "Virtually zero vegetation: completely barren gravel plains and salars",
            "Crisp thin high-altitude air with pale mountain ridges",
            "Cold Humboldt Current offshore blocks atmospheric moisture entirely"
        ],
        "explanation": "BWk (Cold Desert): The Atacama is the driest non-polar desert on Earth. Its mean annual temperature stays under 18°C due to Pacific coastal upwelling and altitude."
    },
    {
        "id": "namib_c14_desert",
        "name": "C14 Gravel Road, Kuiseb Canyon margin",
        "country": "Namibia",
        "lat": -23.321450,
        "lng": 15.772100,
        "koppen_code": "BWk",
        "koppen_group": "B",
        "koppen_name": "Cold Desert climate",
        "hints": [
            "Endless desert plains with rocky inselbergs and dry riverbed washes",
            "Extremely sparse scrub, Euphorbia, and Welwitschia adaptations",
            "Cool maritime marine layer (fog) penetrating inland from the Atlantic"
        ],
        "explanation": "BWk: The Namib is cooled by the Benguela current. Despite tropical latitudes, mean temperatures are cool (<18°C) and rain is virtually nonexistent."
    },
    {
        "id": "gobi_desert_mongolia",
        "name": "South Gobi Track near Tsogt-Ovoo",
        "country": "Mongolia",
        "lat": 44.421900,
        "lng": 105.312800,
        "koppen_code": "BWk",
        "koppen_group": "B",
        "koppen_name": "Cold Desert climate",
        "hints": [
            "Endless stony desert pavement (reg) with dwarf saxaul shrubs",
            "Expansive, treeless horizon under vast continental skies",
            "Severe sub-zero winter freeze (-20°C) alternating with hot dry summers"
        ],
        "explanation": "BWk: The Gobi sits deep in the rain shadow of the Himalayas and Tibetan plateau, enduring frigid Siberian anticyclone winters and arid summers."
    },
    {
        "id": "baja_california_desierto",
        "name": "Highway 1, Cataviña Boulder Desert",
        "country": "Mexico",
        "lat": 29.734120,
        "lng": -114.718900,
        "koppen_code": "BWh",
        "koppen_group": "B",
        "koppen_name": "Hot Desert climate",
        "hints": [
            "Cirio (boojum) trees, giant cardón cacti, and elephant trees",
            "Granite boulder fields under relentless arid sunshine",
            "Annual rainfall under 120mm with scorching summer heat"
        ],
        "explanation": "BWh (Hot Desert): Subtropical high pressure keeps Baja's Central Desert hot and arid with average annual temperature exceeding 18°C."
    },
    {
        "id": "outback_coober_pedy",
        "name": "Stuart Highway, Outback Range",
        "country": "Australia",
        "lat": -28.981200,
        "lng": 134.582100,
        "koppen_code": "BWh",
        "koppen_group": "B",
        "koppen_name": "Hot Desert climate",
        "hints": [
            "Vivid deep-red ironstone gravel and gibber plains",
            "Stunted saltbush and bluebush clumps with zero tree canopy",
            "Extreme heatwaves and prolonged multi-year droughts"
        ],
        "explanation": "BWh: Central Australia's gibber plains experience scorching desert summers and very low sporadic rainfall, classic for continental hot deserts."
    },
    {
        "id": "patagonia_ruta40_steppe",
        "name": "Ruta 40, Santa Cruz Plateau",
        "country": "Argentina",
        "lat": -48.214500,
        "lng": -70.521300,
        "koppen_code": "BSk",
        "koppen_group": "B",
        "koppen_name": "Cold Semi-Arid (Steppe) climate",
        "hints": [
            "Endless windswept coirón bunchgrass and low cushion shrubs",
            "Distant snow-dusted Andean ridges on the western horizon",
            "Relentless westerlies; cold, dry continental plateau"
        ],
        "explanation": "BSk (Cold Semi-Arid): The Andes block moisture from the Pacific, leaving the Patagonian steppe in a cold, windy rain shadow."
    },
    {
        "id": "wyoming_great_divide_basin",
        "name": "Red Desert / Continental Divide Basin",
        "country": "United States",
        "lat": 41.782100,
        "lng": -108.312400,
        "koppen_code": "BSk",
        "koppen_group": "B",
        "koppen_name": "Cold Semi-Arid (Steppe) climate",
        "hints": [
            "Vast sagebrush steppe and greasewood flats",
            "Broad high-altitude basins (2,000m+) framed by distant tablelands",
            "Frigid, windy winter snowstorms and dry summer afternoons"
        ],
        "explanation": "BSk: Wyoming's intermountain basins receive only 200-300mm of precipitation, with cold continental winters keeping the annual mean well below 18°C."
    },
    {
        "id": "sahel_mopti_route",
        "name": "RN16 Sahel Route, Douentza Corridor",
        "country": "Mali",
        "lat": 15.012400,
        "lng": -1.682100,
        "koppen_code": "BSh",
        "koppen_group": "B",
        "koppen_name": "Hot Semi-Arid (Steppe) climate",
        "hints": [
            "Open thorny acacia scrub on sandy soil",
            "Sparse drought-resistant annual grasses and grazing camels",
            "Year-round hot conditions with a fleeting 2-month summer rain pulse"
        ],
        "explanation": "BSh (Hot Semi-Arid): The Sahelian transitional belt between the Sahara and savanna experiences high heat year-round (>28°C mean) and semi-arid rainfall."
    },

    # --- GROUP C: TEMPERATE (Csa, Csb, Cfa, Cfb, Cfc, Cwb) ---
    {
        "id": "peloponnese_olive_hills",
        "name": "Rural Mountain Pass, Peloponnese",
        "country": "Greece",
        "lat": 37.182400,
        "lng": 22.381200,
        "koppen_code": "Csa",
        "koppen_group": "C",
        "koppen_name": "Hot-summer Mediterranean climate",
        "hints": [
            "Terraced olive groves, maquis shrubland, and cypress spires",
            "Limestone karst ridges and dry rocky soil baked under summer sun",
            "Zero summer rain; winter rain supplies groundwater for sclerophyll trees"
        ],
        "explanation": "Csa (Hot-summer Mediterranean): Classic Mediterranean pattern of hot dry summer months (>22°C warmest month) and wet mild winters."
    },
    {
        "id": "chile_maule_mediterranean",
        "name": "Ruta Los Conquistadores, Maule Valley",
        "country": "Chile",
        "lat": -35.582100,
        "lng": -72.182400,
        "koppen_code": "Csb",
        "koppen_group": "C",
        "koppen_name": "Warm-summer Mediterranean climate",
        "hints": [
            "Espino (Acacia caven) savanna and sclerophyllous matorral woodland",
            "Rolling coastal range hills with golden dry summer grass",
            "Cool Pacific breezes keeping warmest month temperatures below 22°C"
        ],
        "explanation": "Csb (Warm-summer Mediterranean): Central Chile's coastal range has dry Mediterranean summers moderated by cool Pacific sea breezes."
    },
    {
        "id": "southern_tablelands_aus",
        "name": "Monaro Highway, Snowy Foothills",
        "country": "Australia",
        "lat": -36.281200,
        "lng": 149.124500,
        "koppen_code": "Cfb",
        "koppen_group": "C",
        "koppen_name": "Temperate Oceanic climate",
        "hints": [
            "Rolling pastoral hills dotted with snow gums and weeping eucalyptus",
            "Green perennial grasslands with reliable year-round rainfall",
            "Mild, cool summers and crisp frosty winters with occasional light snow"
        ],
        "explanation": "Cfb (Oceanic): Temperate highlands of SE Australia receive rain throughout all 12 months with no dry season and mild summer temperatures under 22°C."
    },
    {
        "id": "galicia_rural_costa",
        "name": "Costa da Morte Country Lane, Galicia",
        "country": "Spain",
        "lat": 43.124500,
        "lng": -9.081200,
        "koppen_code": "Cfb",
        "koppen_group": "C",
        "koppen_name": "Temperate Oceanic climate",
        "hints": [
            "Granite stone walls, fern-covered sunken lanes, and eucalyptus/oak groves",
            "Atlantic drizzle and mist rolling in from ocean breakers",
            "Lush green meadows fed by over 1,500mm of annual precipitation"
        ],
        "explanation": "Cfb: Northwest Spain's Atlantic coast has an oceanic climate with abundant rain, moderate temperatures year-round, and cool overcast summers."
    },
    {
        "id": "ozark_interior_missouri",
        "name": "Ozark National Scenic Byway",
        "country": "United States",
        "lat": 37.142100,
        "lng": -91.284500,
        "koppen_code": "Cfa",
        "koppen_group": "C",
        "koppen_name": "Humid Subtropical climate",
        "hints": [
            "Dense mixed oak-hickory and shortleaf pine hardwood forest",
            "Limestone bluffs and crystal-clear spring-fed rivers",
            "Humid, muggy summer thunderstorms and moderately cold winters"
        ],
        "explanation": "Cfa (Humid Subtropical): The interior Ozark plateau features hot humid summers fueled by Gulf moisture and well-distributed precipitation all year."
    },
    {
        "id": "uruguay_pampa_rural",
        "name": "Ruta 8, Lavalleja Rolling Pastures",
        "country": "Uruguay",
        "lat": -34.124500,
        "lng": -55.081200,
        "koppen_code": "Cfa",
        "koppen_group": "C",
        "koppen_name": "Humid Subtropical climate",
        "hints": [
            "Endless rolling green pampas (cuchillas) with grazing cattle",
            "Occasional ombú and palm groves near creek gullies",
            "Abundant year-round rain without a dry season; hot humid summers"
        ],
        "explanation": "Cfa: The Rio de la Plata basin is a premier Southern Hemisphere example of Cfa: warm humid summers, mild winters, and rain in all seasons."
    },
    {
        "id": "faroe_islands_route",
        "name": "Oyggjarvegur Mountain Route, Streymoy",
        "country": "Faroe Islands",
        "lat": 62.081200,
        "lng": -6.912400,
        "koppen_code": "Cfc",
        "koppen_group": "C",
        "koppen_name": "Subpolar Oceanic climate",
        "hints": [
            "Dramatic basalt sea cliffs and totally treeless emerald hillsides",
            "Grazing sheep, peat bogs, and roaring waterfalls plunging to the sea",
            "High humidity, frequent gale winds, and cool summers rarely exceeding 13°C"
        ],
        "explanation": "Cfc (Subpolar Oceanic): The Gulf Stream prevents sub-zero winter extremes, but oceanic cloud cover keeps summer highs below 15°C (1-3 months >10°C)."
    },

    # --- GROUP D: CONTINENTAL (Dfa, Dfb, Dfc, Dwa, Dsc) ---
    {
        "id": "dakota_badlands_rim",
        "name": "Sage Creek Rim Road, Badlands Basin",
        "country": "United States",
        "lat": 43.882100,
        "lng": -102.381200,
        "koppen_code": "Dfa",
        "koppen_group": "D",
        "koppen_name": "Hot-summer Humid Continental climate",
        "hints": [
            "Eroded layered clay buttes rising above mixed-grass prairie",
            "Isolated cottonwood trees along seasonal dry creek beds",
            "Extreme continental swings: -30°C blizzards in winter to +40°C in summer"
        ],
        "explanation": "Dfa (Hot-summer Continental): Deep interior North America exhibits extreme temperature amplitude, with summer peaks exceeding 22°C and freezing winters."
    },
    {
        "id": "taiga_karelia_gravel",
        "name": "Route 88, Lake Oulujärvi Conifer Belt",
        "country": "Finland",
        "lat": 64.382100,
        "lng": 27.182400,
        "koppen_code": "Dfb",
        "koppen_group": "D",
        "koppen_name": "Warm-summer Humid Continental climate",
        "hints": [
            "Dense stands of Scots pine, Norway spruce, and silver birch",
            "Glacial granite erratics and dark peat bog water along the shoulder",
            "4 distinct seasons: snowy freeze from Nov-April and mild green summers"
        ],
        "explanation": "Dfb (Warm-summer Continental): Boreal transition zone where four or more months average above 10°C, but warmest month stays under 22°C."
    },
    {
        "id": "alaska_highway_interior",
        "name": "Taylor Highway, Interior Spruce Flats",
        "country": "United States",
        "lat": 64.081200,
        "lng": -142.182400,
        "koppen_code": "Dfc",
        "koppen_group": "D",
        "koppen_name": "Subarctic (Taiga) climate",
        "hints": [
            "Spindly black spruce muskeg on permafrost ground ('drunken trees')",
            "Reindeer moss (cladonia lichen) and wild blueberry shrubs",
            "Only 1 to 3 months with mean temperatures above 10°C; brutal winters"
        ],
        "explanation": "Dfc (Subarctic): Severe continental subarctic climate with 7+ months of snow and ice and very short, cool growing seasons."
    },
    {
        "id": "inner_mongolia_taiga_fringe",
        "name": "Greater Khingan Range Road",
        "country": "China",
        "lat": 50.182400,
        "lng": 121.381200,
        "koppen_code": "Dwa",
        "koppen_group": "D",
        "koppen_name": "Monsoon Continental climate (Dry Winter)",
        "hints": [
            "Dahurian larch and Mongolian oak on rolling granitic hills",
            "Bone-dry winter landscape under crisp Siberian high pressure skies",
            "Summer monsoon downpours turn the grasslands and forests vibrant green"
        ],
        "explanation": "Dwa: Extreme Northeast Asian monsoon regime: polar Siberian high brings bone-dry sub-zero winters, followed by hot, wet monsoonal summers."
    },
    {
        "id": "columbia_gorge_leeward",
        "name": "Simcoe Mountains Foothill Route",
        "country": "United States",
        "lat": 45.981200,
        "lng": -120.881200,
        "koppen_code": "Dsb",
        "koppen_group": "D",
        "koppen_name": "Dry-summer Continental climate",
        "hints": [
            "Ponderosa pine savanna meeting dry basalt steppe",
            "Bone-dry golden grass in mid-summer under Cascade rain shadow",
            "Freezing winter temperatures with substantial snowpack"
        ],
        "explanation": "Dsb (Dry-summer Continental): Rare climate subtype found on the leeward slopes of the Pacific Northwest cascades: freezing continental winters combined with dry Mediterranean summers."
    },

    # --- GROUP E: POLAR & ALPINE (ET, EF) ---
    {
        "id": "iceland_highlands_f208",
        "name": "Fjallabak Nature Reserve F-Road",
        "country": "Iceland",
        "lat": 63.981200,
        "lng": -19.081200,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Tundra climate",
        "hints": [
            "Black volcanic ash and rhyolite peaks covered in fluorescent green moss",
            "Braided glacial rivers and complete absence of trees or shrubs",
            "Warmest summer month mean remains below 10°C"
        ],
        "explanation": "ET (Tundra): Arctic and alpine tundra where permafrost or harsh cold prevents tree growth, and the warmest month averages between 0°C and 10°C."
    },
    {
        "id": "tierradelfuego_pass_garibaldi",
        "name": "Paso Garibaldi, Fuegian Andes",
        "country": "Argentina",
        "lat": -54.682100,
        "lng": -67.881200,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Tundra / Alpine Subpolar climate",
        "hints": [
            "Wind-sheared krummholz (stunted southern beech) giving way to alpine scree",
            "Glacial cirques, hanging snowfields, and subantarctic peat moss",
            "Relentless subantarctic westerlies and summer temperatures struggling to reach 9°C"
        ],
        "explanation": "ET: High latitude combined with the Fuegian mountain pass creates tundra conditions where the warmest month fails to reach 10°C."
    },
    {
        "id": "grimsel_pass_alps",
        "name": "Grimsel Pass Summit Route",
        "country": "Switzerland",
        "lat": 46.562100,
        "lng": 8.334500,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Alpine Tundra climate",
        "hints": [
            "Glaciated granite domes, alpine lakes, and rocky tundra turf (2,164m)",
            "Patches of residual summer snowpack clinging to north-facing gullies",
            "Tree line is far below; short chilly alpine summer under 10°C mean"
        ],
        "explanation": "ET (Alpine Tundra): High elevation in the Swiss Alps pushes temperatures below the tree line threshold, matching polar tundra criteria."
    },
    {
        "id": "stelvio_pass_glacier_view",
        "name": "Stelvio Pass Mountain Road (2,757m)",
        "country": "Italy",
        "lat": 46.528600,
        "lng": 10.453200,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Alpine Tundra / Subnival climate",
        "hints": [
            "High scree slopes, exposed bare rock, and alpine permafrost terrain",
            "Glacial tongues visible on surrounding 3,000m+ Ortler massif",
            "Bitterly cold winters and brief cool summers with frequent snow flurries"
        ],
        "explanation": "ET: Extreme altitude in the European Alps keeps warmest month temperatures below 10°C, producing barren alpine tundra."
    }
]

print(f"Generated {len(challenging_locations)} challenging locations.")
with open("locations.json", "w") as f:
    json.dump(challenging_locations, f, indent=2)
print("Saved challenging locations to locations.json!")
