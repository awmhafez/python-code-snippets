import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from typing import List, Tuple, Optional, Dict


class SpotifyPlaylistManager:
    def __init__(self, client_id: str = None, client_secret: str = None, redirect_uri: str = None):
        """
        Initialize Spotify API client with OAuth authentication.
        
        Args:
            client_id: Spotify app client ID (or set SPOTIFY_CLIENT_ID env var)
            client_secret: Spotify app client secret (or set SPOTIFY_CLIENT_SECRET env var)
            redirect_uri: Redirect URI (or set SPOTIFY_REDIRECT_URI env var, default: http://localhost:8080)
        """
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = redirect_uri or os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8080')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify client ID and secret are required. Set them as environment variables or pass them directly.")
        
        scope = "playlist-modify-public playlist-modify-private"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scope
        ))
        
        self.user_id = self.sp.current_user()['id']
    
    def search_track(self, song: str, artist: str) -> Optional[str]:
        """
        Search for a track on Spotify and return its URI.
        
        Args:
            song: Song title
            artist: Artist name
            
        Returns:
            Track URI if found, None otherwise
        """
        query = f"track:{song} artist:{artist}"
        results = self.sp.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            print(f"✓ Found: {track['artists'][0]['name']} - {track['name']}")
            return track['uri']
        else:
            print(f"✗ Not found: {artist} - {song}")
            return None
    
    def search_tracks_batch(self, songs_and_artists: List[Tuple[str, str]]) -> List[str]:
        """
        Search for multiple tracks and return their URIs.
        
        Args:
            songs_and_artists: List of (song, artist) tuples
            
        Returns:
            List of track URIs for found songs
        """
        track_uris = []
        
        print(f"Searching for {len(songs_and_artists)} tracks...")
        for song, artist in songs_and_artists:
            uri = self.search_track(song, artist)
            if uri:
                track_uris.append(uri)
        
        print(f"\nFound {len(track_uris)} out of {len(songs_and_artists)} tracks")
        return track_uris
    
    def create_playlist(self, name: str, description: str = "", public: bool = True) -> str:
        """
        Create a new playlist.
        
        Args:
            name: Playlist name
            description: Playlist description
            public: Whether playlist should be public
            
        Returns:
            Playlist ID
        """
        playlist = self.sp.user_playlist_create(
            user=self.user_id,
            name=name,
            public=public,
            description=description
        )
        
        print(f"Created playlist: {name} (ID: {playlist['id']})")
        return playlist['id']
    
    def add_tracks_to_playlist(self, playlist_id: str, track_uris: List[str]) -> bool:
        """
        Add tracks to an existing playlist.
        
        Args:
            playlist_id: ID of the playlist
            track_uris: List of track URIs to add
            
        Returns:
            True if successful
        """
        if not track_uris:
            print("No tracks to add to playlist")
            return False
        
        # Spotify API allows max 100 tracks per request
        batch_size = 100
        for i in range(0, len(track_uris), batch_size):
            batch = track_uris[i:i + batch_size]
            self.sp.playlist_add_items(playlist_id, batch)
        
        print(f"Added {len(track_uris)} tracks to playlist")
        return True
    
    def create_playlist_from_songs(self, 
                                   songs_and_artists: List[Tuple[str, str]], 
                                   playlist_name: str,
                                   playlist_description: str = "",
                                   public: bool = True) -> Dict:
        """
        Create a new playlist and add songs to it.
        
        Args:
            songs_and_artists: List of (song, artist) tuples
            playlist_name: Name for the new playlist
            playlist_description: Description for the playlist
            public: Whether playlist should be public
            
        Returns:
            Dictionary with playlist info and results
        """
        print(f"Creating playlist '{playlist_name}'...")
        
        # Search for tracks
        track_uris = self.search_tracks_batch(songs_and_artists)
        
        if not track_uris:
            print("No tracks found, cannot create playlist")
            return {"success": False, "playlist_id": None, "tracks_added": 0}
        
        # Create playlist
        playlist_id = self.create_playlist(playlist_name, playlist_description, public)
        
        # Add tracks to playlist
        success = self.add_tracks_to_playlist(playlist_id, track_uris)
        
        result = {
            "success": success,
            "playlist_id": playlist_id,
            "tracks_found": len(track_uris),
            "tracks_requested": len(songs_and_artists),
            "playlist_url": f"https://open.spotify.com/playlist/{playlist_id}"
        }
        
        if success:
            print(f"\n🎵 Playlist created successfully!")
            print(f"URL: {result['playlist_url']}")
            print(f"Added {result['tracks_found']} out of {result['tracks_requested']} requested tracks")
        
        return result
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """
        Get all tracks from a playlist.
        
        Args:
            playlist_id: ID of the playlist
            
        Returns:
            List of track information
        """
        results = self.sp.playlist_tracks(playlist_id)
        tracks = []
        
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'uri': track['uri']
                })
        
        return tracks