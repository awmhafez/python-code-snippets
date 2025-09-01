# Python Code Snippets

A collection of Python code snippets for various programming tasks and examples.

## 🎵 Spotify Playlist Tools

The main feature of this repository is a comprehensive set of Spotify tools that can create playlists without requiring a Spotify app!

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

- **`utilities/`** - Core Spotify tools and utilities
- **`examples/`** - Ready-to-run example scripts
- **`algorithms/`** - Algorithm implementations (empty - ready for your code)
- **`data_structures/`** - Data structure examples (empty - ready for your code)

## 🛠 Dependencies

- `requests` - HTTP requests for Spotify API calls
- `spotipy` - Official Spotify library (for reference examples)

## 🎯 Featured Success Story

Successfully created a **90s/2000s Eurodance Classics** playlist with 43 out of 45 tracks including:
- Technotronic - Pump Up the Jam
- Paradisio - Bailando  
- Darude - Sandstorm
- Daft Punk - Around the World
- And many more classics!

## 🤝 Contributing

Feel free to add your own code snippets and utilities to any folder. This repository is designed to grow with useful Python code examples.