# 🌍 Köppen Climate Zone Guessr

A GeoGuessr-inspired geography and climatology game that drops you into a mystery Google Street View location anywhere on Earth and challenges you to deduce its **Köppen climate classification**.

🎮 **Play Online**: [https://vadim0x60.github.io/koppengame/](https://vadim0x60.github.io/koppengame/)

## ✨ Features

- **Interactive 360° Street View**: Look around, pan, zoom, and inspect flora, soil, topography, sunlight angle, and architecture.
- **50/50 Hints**: Use up to three botanical and geographic clues per round. Each hint also safely eliminates about half of the remaining wrong answers, narrowing the field from 31 choices to 16, then 8, then 4.
- **Full Educational Explanations**: Detailed breakdown after each guess showing why that region has that specific Köppen code (temperature thresholds, rainfall seasonality, ocean currents, rain shadows).
- **In-Game Reference Guide**: A built-in modal with quick summaries of the entire Köppen classification scheme.
- **Stats & Streaks**: Tracks rounds, current streak, high streak, and overall accuracy.
- **Zero Configuration Required**: Works out-of-the-box in any modern browser. Supports an optional custom Google Maps API key if you want to use the official Maps Embed API.
- **Massive Global Location Pool**: Over 2,600 verified global Street View panoramas sampled from the open-source GeoGuessr world pool and cross-referenced with high-resolution Köppen climatology rasters, balanced across all major climate groups and subtypes.

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
