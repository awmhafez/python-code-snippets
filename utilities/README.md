# Spotify Playlist Manager

A Python utility for creating and managing Spotify playlists using the Spotify Web API.

## Setup

1. **Create a Spotify App:**
   - Go to https://developer.spotify.com/dashboard/applications
   - Click "Create an App"
   - Fill in the app name and description
   - Copy your Client ID and Client Secret

2. **Set Environment Variables:**
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id_here"
   export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
   export SPOTIFY_REDIRECT_URI="http://localhost:8080"  # Optional, this is the default
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```python
from utilities.spotify_playlist_manager import SpotifyPlaylistManager

# Initialize the manager
spotify = SpotifyPlaylistManager()

# Create a playlist with songs
songs = [
    ("Bohemian Rhapsody", "Queen"),
    ("Hotel California", "Eagles"),
    ("Stairway to Heaven", "Led Zeppelin")
]

result = spotify.create_playlist_from_songs(
    songs_and_artists=songs,
    playlist_name="My Awesome Playlist",
    playlist_description="Created with Python!"
)

print(f"Playlist URL: {result['playlist_url']}")
```

### Run the Example

```bash
python examples/spotify_playlist_example.py
```

## Features

- **Search for tracks** by song title and artist
- **Create new playlists** with custom names and descriptions
- **Add tracks to existing playlists**
- **Batch processing** of multiple songs
- **Error handling** for songs that can't be found
- **OAuth authentication** with automatic token management

## Methods

- `search_track(song, artist)` - Find a single track
- `search_tracks_batch(songs_list)` - Find multiple tracks
- `create_playlist(name, description, public)` - Create a new playlist
- `add_tracks_to_playlist(playlist_id, track_uris)` - Add tracks to existing playlist
- `create_playlist_from_songs(songs, name, description)` - Complete workflow
- `get_playlist_tracks(playlist_id)` - Get tracks from existing playlist