# Spotify Utilities

Python utilities for creating and managing Spotify playlists **without requiring a Spotify app registration**.

## 🚀 SpotifyTokenScraper - Create Real Playlists!

The main utility that can actually create and modify playlists using your browser's Bearer token.

### Setup

1. **Get Bearer Token from Browser:**
   - Go to https://open.spotify.com in your browser and log in
   - Open Developer Tools (F12) → Network tab
   - Search for something on Spotify
   - Look for requests to `api-partner.spotify.com` or `api.spotify.com`
   - Find the `Authorization: Bearer ...` header and copy the token

2. **Install Dependencies:**
   ```bash
   pip install requests
   ```

### Usage

```python
from utilities.spotify_token_scraper import SpotifyTokenScraper

# Initialize with your Bearer token
scraper = SpotifyTokenScraper("your_bearer_token_here")

# Create a playlist with songs
songs = [
    ("Bailando", "Paradisio"),
    ("Sandstorm", "Darude"),
    ("Pump Up the Jam", "Technotronic")
]

result = scraper.create_playlist_from_songs(
    songs_and_artists=songs,
    playlist_name="My Dance Playlist",
    playlist_description="Created with Python!"
)

print(f"Playlist URL: {result['playlist_url']}")
```

### Features
- ✅ **Create playlists** - Actually creates playlists in your Spotify account
- ✅ **Add tracks** - Adds tracks to existing playlists  
- ✅ **Search tracks** - Finds tracks by song title and artist
- ✅ **Batch processing** - Handle multiple songs at once
- ✅ **User info** - Get current user information
- ✅ **List playlists** - View your existing playlists

---

## 🔍 SpotifyWebScraper - Search Without Authentication

Read-only search functionality that doesn't require any authentication.

### Usage

```python
from utilities.spotify_web_scraper import SpotifyWebScraper

# No authentication needed!
scraper = SpotifyWebScraper()

# Search for tracks
tracks = scraper.search_track("Paradisio Bailando", limit=5)

# Search multiple tracks
songs = [("Bailando", "Paradisio"), ("Sandstorm", "Darude")]
found_tracks = scraper.search_tracks_batch(songs)

# Export results
scraper.export_to_csv(found_tracks, "my_tracks.csv")
scraper.export_to_text(found_tracks, "my_tracks.txt")
```

### Features
- 🔍 **Search tracks** - Find songs by title and artist
- 📊 **Track info** - Get duration, popularity, album info
- 📁 **Export** - Save results to CSV or text files
- ⚡ **Fast** - No authentication delays
- 🔓 **Open** - Works without any tokens or credentials

---

## 📋 Methods Reference

### SpotifyTokenScraper Methods
- `search_track(song, artist)` - Find a single track
- `search_tracks_batch(songs_list)` - Find multiple tracks
- `create_playlist(user_id, name, description, public)` - Create new playlist
- `add_tracks_to_playlist(playlist_id, track_uris)` - Add tracks to playlist
- `create_playlist_from_songs(songs, name, description)` - Complete workflow
- `get_playlist_tracks(playlist_id)` - Get tracks from existing playlist
- `get_user_playlists(limit)` - List user's playlists
- `get_current_user()` - Get user information

### SpotifyWebScraper Methods
- `search_track(search_term, limit)` - Search for tracks
- `search_tracks_batch(songs_and_artists)` - Batch search
- `export_to_csv(tracks, filename)` - Export to CSV
- `export_to_text(tracks, filename)` - Export to text
- `format_track_list(tracks)` - Format for display

## ⚠️ Important Notes

- **Bearer tokens expire** (usually after ~1 hour) - get fresh tokens as needed
- **Token scraper** can create/modify playlists but tokens expire
- **Web scraper** is read-only but works indefinitely without auth
- Both tools respect Spotify's rate limits and include delays between requests

## 🎯 Example Files

- `../examples/run_eurodance_playlist.py` - Create a 90s/2000s playlist
- `../examples/spotify_token_example.py` - Interactive token examples
- `../examples/spotify_scraper_example.py` - No-auth search examples