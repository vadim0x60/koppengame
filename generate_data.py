import json

locations = [
    # --- GROUP A: TROPICAL ---
    {
        "id": "singapore",
        "name": "Singapore",
        "country": "Singapore",
        "lat": 1.290270,
        "lng": 103.851959,
        "koppen_code": "Af",
        "koppen_group": "A",
        "koppen_name": "Tropical Rainforest climate",
        "hints": ["Near equatorial latitude (1°N)", "Lush, dense tropical foliage year-round", "Consistent high humidity and afternoon downpours with no dry season"],
        "explanation": "Af climates experience high temperatures all year with monthly precipitation exceeding 60mm in all 12 months. Dense broadleaf evergreen vegetation and equatorial sun are key signatures."
    },
    {
        "id": "iquitos_peru",
        "name": "Iquitos",
        "country": "Peru",
        "lat": -3.743673,
        "lng": -73.251633,
        "koppen_code": "Af",
        "koppen_group": "A",
        "koppen_name": "Tropical Rainforest climate",
        "hints": ["Amazon Basin interior", "Equatorial wet climate surrounded by rainforest", "Very uniform high temperature and heavy rainfall throughout the year"],
        "explanation": "Deep in the Amazon rainforest, Iquitos is the largest city in the world unreachable by road and exhibits textbook tropical rainforest (Af) conditions."
    },
    {
        "id": "miami_fl",
        "name": "Miami, Florida",
        "country": "United States",
        "lat": 25.778135,
        "lng": -80.131324,
        "koppen_code": "Am",
        "koppen_group": "A",
        "koppen_name": "Tropical Monsoon climate",
        "hints": ["Subtropical/tropical peninsula with palm trees", "Pronounced rainy season in summer/fall, brief drier winter", "Warm coastal breezes"],
        "explanation": "Miami has a tropical monsoon climate (Am), featuring a short drier winter but heavy monsoon-like rains in summer that easily sustain tropical vegetation."
    },
    {
        "id": "ko_samui",
        "name": "Koh Samui",
        "country": "Thailand",
        "lat": 9.535671,
        "lng": 100.063467,
        "koppen_code": "Am",
        "koppen_group": "A",
        "koppen_name": "Tropical Monsoon climate",
        "hints": ["Southeast Asian island", "Intense monsoon season between October and December", "Lush tropical coastal flora"],
        "explanation": "Koh Samui experiences a tropical monsoon climate where monsoon winds bring torrential rains during part of the year, with a short dry period."
    },
    {
        "id": "darwin_australia",
        "name": "Darwin",
        "country": "Australia",
        "lat": -12.463440,
        "lng": 130.845642,
        "koppen_code": "Aw",
        "koppen_group": "A",
        "koppen_name": "Tropical Savanna climate (Wet/Dry)",
        "hints": ["Top End of Northern Australia", "Dramatic contrast between monsoon 'Wet' and bone-dry 'Dry' seasons", "Tropical grasslands and eucalyptus woodland"],
        "explanation": "Darwin has a tropical savanna (Aw) climate with distinct dry winters and torrential wet summers dictated by the Australian monsoon."
    },
    {
        "id": "brasilia_brazil",
        "name": "Brasília",
        "country": "Brazil",
        "lat": -15.797515,
        "lng": -47.891888,
        "koppen_code": "Aw",
        "koppen_group": "A",
        "koppen_name": "Tropical Savanna climate (Wet/Dry)",
        "hints": ["Central Brazilian plateau (Cerrado)", "Months of nearly zero winter rainfall followed by summer storms", "Stunted savanna trees and grassland"],
        "explanation": "Brasília's high plateau location exhibits an Aw (tropical savanna) regime with severe winter drought (May-September) and humid summer downpours."
    },

    # --- GROUP B: ARID & SEMI-ARID ---
    {
        "id": "las_vegas_nv",
        "name": "Las Vegas, Nevada",
        "country": "United States",
        "lat": 36.169941,
        "lng": -115.139830,
        "koppen_code": "BWh",
        "koppen_group": "B",
        "koppen_name": "Hot Desert climate",
        "hints": ["Mojave Desert basin", "Creosote bush, desert landscaping, intense summer heat >40°C", "Extremely low annual precipitation (<110mm)"],
        "explanation": "BWh indicates a hot arid desert where potential evapotranspiration heavily exceeds precipitation and mean annual temperature is >18°C."
    },
    {
        "id": "dubai_uae",
        "name": "Dubai",
        "country": "United Arab Emirates",
        "lat": 25.197197,
        "lng": 55.274376,
        "koppen_code": "BWh",
        "koppen_group": "B",
        "koppen_name": "Hot Desert climate",
        "hints": ["Arabian Peninsula coastal desert", "Blistering summer heat and sandy expanse", "Scant winter rains only"],
        "explanation": "Dubai sits in the Arabian desert with extreme heat and very low annual rainfall, typical of subtropical high-pressure deserts (BWh)."
    },
    {
        "id": "swakopmund_namibia",
        "name": "Swakopmund",
        "country": "Namibia",
        "lat": -22.679124,
        "lng": 14.526848,
        "koppen_code": "BWk",
        "koppen_group": "B",
        "koppen_name": "Cold Desert climate",
        "hints": ["Namib coast with coastal fog", "Cool sea breezes from the Benguela current despite barren dunes", "Annual precipitation under 20mm"],
        "explanation": "BWk denotes a cold desert (mean annual temperature <18°C). Cold ocean currents suppress precipitation, creating a cool, hyper-arid fog desert."
    },
    {
        "id": "turpan_china",
        "name": "Turpan",
        "country": "China",
        "lat": 42.951301,
        "lng": 89.189500,
        "koppen_code": "BWk",
        "koppen_group": "B",
        "koppen_name": "Cold Desert climate",
        "hints": ["Deep inland depression in Central Asia (Taklamakan basin)", "Frigid continental winters and scorching summers", "Extremely dry desert basin with ancient irrigation"],
        "explanation": "Turpan has a cold desert (BWk) climate due to extreme distance from oceans and mountain rain shadows, bringing freezing winter temperatures and negligible rainfall."
    },
    {
        "id": "zaragoza_spain",
        "name": "Zaragoza",
        "country": "Spain",
        "lat": 41.648823,
        "lng": -0.889085,
        "koppen_code": "BSk",
        "koppen_group": "B",
        "koppen_name": "Cold Semi-Arid (Steppe) climate",
        "hints": ["Ebro River basin surrounded by mountain ranges", "Steppe vegetation, dry continental plateau", "Cold winter spells with hot, dry summers"],
        "explanation": "The interior Ebro basin is rain-shadowed by the Pyrenees and Iberian system, creating a cold semi-arid steppe (BSk) climate."
    },
    {
        "id": "denver_co",
        "name": "Denver, Colorado",
        "country": "United States",
        "lat": 39.739236,
        "lng": -104.990251,
        "koppen_code": "BSk",
        "koppen_group": "B",
        "koppen_name": "Cold Semi-Arid (Steppe) climate",
        "hints": ["High Plains just east of the Rocky Mountains", "Shortgrass prairie, sunny skies, dramatic temperature swings", "Low annual rainfall with winter snow"],
        "explanation": "Denver sits in the rain shadow of the Rockies on the semi-arid high plains, receiving about 380mm of precipitation annually."
    },
    {
        "id": "marrakech_morocco",
        "name": "Marrakech",
        "country": "Morocco",
        "lat": 31.629472,
        "lng": -7.981084,
        "koppen_code": "BSh",
        "koppen_group": "B",
        "koppen_name": "Hot Semi-Arid (Steppe) climate",
        "hints": ["North of the High Atlas mountains", "Semi-desert shrubs, olive and date palm groves", "Warm winters and very hot, dry summers"],
        "explanation": "Marrakech falls into BSh: semi-arid transitional steppe between Mediterranean coastal areas and the Sahara Desert, with average annual temperatures >18°C."
    },

    # --- GROUP C: TEMPERATE ---
    {
        "id": "athens_greece",
        "name": "Athens",
        "country": "Greece",
        "lat": 37.983810,
        "lng": 23.727539,
        "koppen_code": "Csa",
        "koppen_group": "C",
        "koppen_name": "Hot-summer Mediterranean climate",
        "hints": ["Southern European Aegean coast", "Olive trees, dry rocky hills, whitewashed terracotta architecture", "Long, bone-dry hot summers and mild rainy winters"],
        "explanation": "Csa is the classic Mediterranean climate: hot, dry summers controlled by subtropical high pressure, and wet, mild winters."
    },
    {
        "id": "san_francisco_ca",
        "name": "San Francisco, California",
        "country": "United States",
        "lat": 37.774929,
        "lng": -122.419416,
        "koppen_code": "Csb",
        "koppen_group": "C",
        "koppen_name": "Warm-summer Mediterranean climate",
        "hints": ["Pacific coastal peninsula with cool summer fog", "Mediterranean dry summer pattern but rarely hot due to marine upwelling", "Eucalyptus, coastal pines, mild year-round"],
        "explanation": "San Francisco is a classic cool/warm-summer Mediterranean (Csb) climate where cold Pacific currents keep summer temperatures remarkably cool despite clear dry months."
    },
    {
        "id": "cape_town_south_africa",
        "name": "Cape Town",
        "country": "South Africa",
        "lat": -33.924869,
        "lng": 18.424055,
        "koppen_code": "Csb",
        "koppen_group": "C",
        "koppen_name": "Warm-summer Mediterranean climate",
        "hints": ["Southern tip of African continent under Table Mountain", "Fynbos shrubland, prominent winter rain, dry sunny summer", "Oceanic influence moderates peak heat"],
        "explanation": "Cape Town features a warm-summer Mediterranean (Csb) climate with winter storm fronts and dry summer southerly winds ('Cape Doctor')."
    },
    {
        "id": "london_uk",
        "name": "London",
        "country": "United Kingdom",
        "lat": 51.507351,
        "lng": -0.127758,
        "koppen_code": "Cfb",
        "koppen_group": "C",
        "koppen_name": "Temperate Oceanic (Marine West Coast) climate",
        "hints": ["Northwestern Europe maritime zone", "Deciduous parklands, frequent overcast skies, drizzle spread across all seasons", "Mild winters and moderate, rarely hot summers"],
        "explanation": "Cfb climates are maritime with no dry season and warm (not hot) summers, heavily moderated by the North Atlantic Current."
    },
    {
        "id": "auckland_nz",
        "name": "Auckland",
        "country": "New Zealand",
        "lat": -36.848460,
        "lng": 174.763332,
        "koppen_code": "Cfb",
        "koppen_group": "C",
        "koppen_name": "Temperate Oceanic climate",
        "hints": ["Southern Hemisphere island isthmus", "Lush rolling green hills, tree ferns, maritime breezes", "Rainfall well-distributed across all months with mild temperatures"],
        "explanation": "Auckland has an oceanic (Cfb) climate with high humidity, frequent showers, and mild oceanic winters and summers."
    },
    {
        "id": "tokyo_japan",
        "name": "Tokyo",
        "country": "Japan",
        "lat": 35.689487,
        "lng": 139.691706,
        "koppen_code": "Cfa",
        "koppen_group": "C",
        "koppen_name": "Humid Subtropical climate",
        "hints": ["East Asian Pacific coast", "Hot, muggy rainy summers with typhoon activity, cool sunny winters", "Broadleaf evergreen and deciduous mixed forests"],
        "explanation": "Tokyo has a humid subtropical (Cfa) climate characterized by warm-to-hot humid summers, abundant precipitation, and relatively mild winters."
    },
    {
        "id": "atlanta_ga",
        "name": "Atlanta, Georgia",
        "country": "United States",
        "lat": 33.748995,
        "lng": -84.387982,
        "koppen_code": "Cfa",
        "koppen_group": "C",
        "koppen_name": "Humid Subtropical climate",
        "hints": ["Southeastern US Piedmont region", "Dense canopy of oak, pine, and magnolia", "Hot muggy summers with frequent thunderstorms, mild winters"],
        "explanation": "The American Southeast represents classic Cfa: no dry season, gulf moisture fueling warm humid summers, and temperate winters."
    },
    {
        "id": "addis_ababa_ethiopia",
        "name": "Addis Ababa",
        "country": "Ethiopia",
        "lat": 9.032000,
        "lng": 38.748000,
        "koppen_code": "Cwb",
        "koppen_group": "C",
        "koppen_name": "Subtropical Highland climate (Dry Winter)",
        "hints": ["East African high plateau (>2,300m elevation)", "Eucalyptus groves, pleasant spring-like temperatures year-round", "Heavy summer monsoon rain and very dry winters"],
        "explanation": "Despite being near the equator, high elevation keeps temperatures temperate (Cwb), with a stark monsoon dry-winter pattern."
    },

    # --- GROUP D: CONTINENTAL ---
    {
        "id": "stockholm_sweden",
        "name": "Stockholm",
        "country": "Sweden",
        "lat": 59.329323,
        "lng": 18.068581,
        "koppen_code": "Dfb",
        "koppen_group": "D",
        "koppen_name": "Warm-summer Humid Continental climate",
        "hints": ["Baltic Sea Nordic archipelago (59°N)", "Birch and pine woodlands, distinct snowy winters", "Warm, pleasant summers with long daylight hours"],
        "explanation": "Stockholm has a warm-summer humid continental (Dfb) climate: coldest month averages below 0°C (or -3°C), four distinct seasons, and no dry season."
    },
    {
        "id": "chicago_il",
        "name": "Chicago, Illinois",
        "country": "United States",
        "lat": 41.878114,
        "lng": -87.629798,
        "koppen_code": "Dfa",
        "koppen_group": "D",
        "koppen_name": "Hot-summer Humid Continental climate",
        "hints": ["Lake Michigan shoreline in the Midwest interior", "Freezing snowy winters with polar vortex snaps, hot humid summers", "Deciduous hardwood forest and prairie transition"],
        "explanation": "Chicago has a hot-summer humid continental (Dfa) climate, with warm/hot summer months exceeding 22°C on average and freezing winter temperatures."
    },
    {
        "id": "sapporo_japan",
        "name": "Sapporo, Hokkaido",
        "country": "Japan",
        "lat": 43.061771,
        "lng": 141.354451,
        "koppen_code": "Dfb",
        "koppen_group": "D",
        "koppen_name": "Warm-summer Humid Continental climate",
        "hints": ["Northern Japanese island of Hokkaido", "World-renowned heavy winter snowfall from Siberian sea-effect winds", "Cool to warm summers with lush conifers and deciduous trees"],
        "explanation": "Sapporo is one of the snowiest major cities in the world, fitting Dfb with cold snowy winters and warm, non-monsoonal summers."
    },
    {
        "id": "anchorage_ak",
        "name": "Anchorage, Alaska",
        "country": "United States",
        "lat": 61.218056,
        "lng": -149.900278,
        "koppen_code": "Dsc",
        "koppen_group": "D",
        "koppen_name": "Dry-summer Subarctic climate",
        "hints": ["Southcentral Alaska coastal inlet flanked by Chugach Mountains", "Spruce and birch taiga, long cold winters, short cool summers", "Drier spring and early summer followed by autumn showers"],
        "explanation": "Anchorage borders subarctic climates (Dfc/Dsc) with fewer than four months averaging above 10°C, cold winters, and dry early summer characteristics."
    },
    {
        "id": "rovaniemi_finland",
        "name": "Rovaniemi (Lapland)",
        "country": "Finland",
        "lat": 66.503948,
        "lng": 25.729391,
        "koppen_code": "Dfc",
        "koppen_group": "D",
        "koppen_name": "Subarctic (Taiga) climate",
        "hints": ["Directly on the Arctic Circle (66.5°N)", "Extensive boreal forest (taiga), pine and spruce, snow cover for 6+ months", "Short, cool summers and prolonged sub-zero winters"],
        "explanation": "Dfc is the classic subarctic boreal climate: 1 to 3 months with mean temperature above 10°C, and severe sub-zero winters."
    },
    {
        "id": "harbin_china",
        "name": "Harbin",
        "country": "China",
        "lat": 45.803775,
        "lng": 126.534967,
        "koppen_code": "Dwa",
        "koppen_group": "D",
        "koppen_name": "Monsoon-influenced Hot-summer Humid Continental climate",
        "hints": ["Northeast China (Manchuria)", "Famous Ice and Snow Festival with brutal dry sub-zero Siberian winters", "Warm, rainy monsoon-driven summers"],
        "explanation": "Dwa climates have extreme Siberian high-pressure winter dry conditions followed by East Asian summer monsoon rains and warm temperatures."
    },

    # --- GROUP E: POLAR & ALPINE ---
    {
        "id": "longyearbyen_svalbard",
        "name": "Longyearbyen, Svalbard",
        "country": "Norway",
        "lat": 78.223172,
        "lng": 15.646897,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Tundra climate",
        "hints": ["High Arctic archipelago (78°N)", "No trees, permafrost ground, Arctic moss and lichens, snowy fjords", "Warmest month averages below 10°C but above 0°C"],
        "explanation": "ET (Tundra) occurs when at least one month averages above freezing (0°C) to melt snow, but the warmest month remains below 10°C, preventing tree growth."
    },
    {
        "id": "ushuaia_argentina",
        "name": "Ushuaia, Tierra del Fuego",
        "country": "Argentina",
        "lat": -54.801912,
        "lng": -68.302951,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Tundra / Subpolar Oceanic climate",
        "hints": ["Southernmost tip of South America (Tierra del Fuego)", "Stunted Antarctic beech (Nothofagus) and tundra mosses", "Chilly, windy maritime weather year-round with warmest month barely reaching 10°C"],
        "explanation": "Ushuaia sits on the boundary of subpolar oceanic (Cfc) and tundra (ET), with polar winds from Drake Passage keeping summer temperatures exceptionally cool."
    },
    {
        "id": "nuuk_greenland",
        "name": "Nuuk",
        "country": "Greenland",
        "lat": 64.181410,
        "lng": -51.694138,
        "koppen_code": "ET",
        "koppen_group": "E",
        "koppen_name": "Tundra climate",
        "hints": ["Southwest coast of Greenland", "Rocky fjord landscape devoid of natural trees, coastal tundra", "Short chilly summers under 10°C and long freezing maritime winters"],
        "explanation": "Nuuk has a maritime tundra climate (ET) where cold Labrador currents prevent summer warming, keeping monthly averages under 10°C."
    },
    {
        "id": "jungfraujoch_swiss",
        "name": "Jungfraujoch (Bernese Alps)",
        "country": "Switzerland",
        "lat": 46.547500,
        "lng": 7.985278,
        "koppen_code": "EF",
        "koppen_group": "E",
        "koppen_name": "Ice Cap (Alpine Frost) climate",
        "hints": ["Glaciated Alpine pass at 3,454m elevation", "Perpetual snow and glacial ice (Aletsch Glacier)", "Every single month has an average temperature below 0°C"],
        "explanation": "EF (Ice Cap / Perpetual Frost) applies where all 12 months average below 0°C, preventing any permanent melting and sustaining year-round ice."
    },
    {
        "id": "reykjavik_iceland",
        "name": "Reykjavík",
        "country": "Iceland",
        "lat": 64.146582,
        "lng": -21.942635,
        "koppen_code": "Cfc",
        "koppen_group": "C",
        "koppen_name": "Subpolar Oceanic climate",
        "hints": ["North Atlantic volcanic island near Arctic Circle", "Lupines, moss-covered lava fields, cool breezy weather", "Mild winters due to Gulf Stream, but cool summers under 15°C"],
        "explanation": "Reykjavík has a subpolar oceanic climate (Cfc): 1 to 3 months above 10°C, oceanic moderation keeping winter averages near 0°C, and damp weather throughout the year."
    }
]

with open("locations.json", "w") as f:
    json.dump(locations, f, indent=2)

print(f"Successfully generated locations.json with {len(locations)} locations.")
