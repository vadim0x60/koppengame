# 🌍 Köppen Climate Zone Guessr

A GeoGuessr-inspired geography and climatology game that drops you into a mystery Google Street View location anywhere on Earth and challenges you to deduce its **Köppen climate classification**.

🎮 **Play Online**: [https://vadim0x60.github.io/koppengame/](https://vadim0x60.github.io/koppengame/)

## ✨ Features

- **Interactive 360° Street View**: Look around, pan, zoom, and inspect flora, soil, topography, sunlight angle, and architecture.
- **Two Difficulty Modes**:
  - **5 Major Groups (A-E)**:
    - `A`: Tropical (Rainforest, Monsoon, Savanna)
    - `B`: Arid & Semi-Arid (Deserts, Steppes)
    - `C`: Temperate (Mediterranean, Oceanic, Humid Subtropical)
    - `D`: Continental (Humid Continental, Subarctic / Taiga)
    - `E`: Polar & Alpine (Tundra, Ice Cap)
  - **Subtypes**: Specific codes such as `Csa`, `Dfb`, `BWh`, `ET`, `Am`, etc.
- **Botanical & Geographic Hints**: Expandable hints pointing out biomes, indicator plants (e.g. eucalypts, creosote, spruce, olive groves, fynbos), and latitude cues without spoiling the answer.
- **Full Educational Explanations**: Detailed breakdown after each guess showing why that region has that specific Köppen code (temperature thresholds, rainfall seasonality, ocean currents, rain shadows).
- **In-Game Reference Guide**: A built-in modal with quick summaries of the entire Köppen classification scheme.
- **Stats & Streaks**: Tracks rounds, current streak, high streak, and overall accuracy.
- **Zero Configuration Required**: Works out-of-the-box in any modern browser. Supports an optional custom Google Maps API key if you want to use the official Maps Embed API.

## 🚀 How to Run

1. Start the local server:
   ```bash
   python3 server.py
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

Enjoy testing your geography and climate knowledge!
