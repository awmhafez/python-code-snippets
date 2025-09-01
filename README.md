# Python Code Snippets

A collection of useful Python utilities, tools, and examples for various programming tasks.

## ✨ Featured Tools

This repository contains several practical Python utilities:

- **🎵 Spotify Tools** - Create and manage playlists without app registration
- **🕰️ Life Visualization** - Interactive life timeline showing weeks as dots
- **📊 Data Processing** - Algorithms and data structure examples

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a playlist with your favorite songs:**
   ```bash
   python examples/run_eurodance_playlist.py
   ```

3. **Get a Bearer token** (required):
   - Go to https://open.spotify.com in your browser
   - Open Developer Tools (F12) → Network tab
   - Search for something on Spotify
   - Look for requests with `Authorization: Bearer ...`
   - Copy the token

### Available Tools

#### 🚀 **SpotifyTokenScraper** - Create Real Playlists!
- **Creates and modifies playlists** using browser Bearer token
- **Search for tracks** by song title and artist
- **Batch processing** of multiple songs
- **No Spotify app registration needed**

```python
from utilities.spotify_token_scraper import SpotifyTokenScraper

scraper = SpotifyTokenScraper("your_bearer_token")
songs = [("Bailando", "Paradisio"), ("Sandstorm", "Darude")]
result = scraper.create_playlist_from_songs(songs, "My Playlist")
```

#### 🔍 **SpotifyWebScraper** - Search Without Authentication
- **Read-only search** functionality
- **No authentication required**
- **Export results** to CSV/TXT

```python
from utilities.spotify_web_scraper import SpotifyWebScraper

scraper = SpotifyWebScraper()
tracks = scraper.search_track("Paradisio Bailando")
scraper.export_to_csv(tracks, "results.csv")
```

### Example Scripts

- **`run_eurodance_playlist.py`** - Create a 90s/2000s eurodance playlist (45 classic tracks!)
- **`spotify_token_example.py`** - Interactive examples with Bearer token
- **`spotify_scraper_example.py`** - No-auth search examples

## 📁 Project Structure

- **`utilities/`** - Reusable Python utilities and tools
  - `spotify_token_scraper.py` - Create Spotify playlists without app registration
  - `spotify_web_scraper.py` - Search Spotify tracks without authentication
  - `life_weeks_visualizer.py` - Interactive life timeline visualization
- **`examples/`** - Ready-to-run example scripts and demos
- **`algorithms/`** - Algorithm implementations and examples
- **`data_structures/`** - Data structure examples and utilities

## 🛠 Dependencies

- `requests` - HTTP requests for Spotify API calls
- `spotipy` - Official Spotify library (for reference examples)
- `pygame` - Game development library for visualization tools

## 🚀 Quick Start Examples

### Life Weeks Visualizer
```python
from utilities.life_weeks_visualizer import LifeWeeksVisualizer

visualizer = LifeWeeksVisualizer(
    birth_year=1990, birth_month=1, birth_day=1,
    target_age=85, name="My Life in Weeks"
)
visualizer.run()
```

### Spotify Playlist Creation
```python
from utilities.spotify_token_scraper import SpotifyTokenScraper

scraper = SpotifyTokenScraper("your_bearer_token")
songs = [("Song Title", "Artist Name")]
result = scraper.create_playlist_from_songs(songs, "My Playlist")
```

## 🤝 Contributing

Contributions welcome! This repository is designed to be a growing collection of useful Python utilities and examples. Feel free to:

- Add new utilities to the `utilities/` folder
- Contribute algorithm implementations
- Share example scripts and demos
- Improve existing code and documentation