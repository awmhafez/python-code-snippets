import requests
import json
from typing import List, Dict, Optional, Tuple
import time


class SpotifyTokenScraper:
    """
    Spotify scraper using Bearer token authentication.
    
    This uses a valid Bearer token from Spotify's web interface to make
    authenticated requests to their internal API endpoints.
    
    Note: Bearer tokens expire after some time (usually 1 hour).
    You'll need to get a fresh token from your browser's network tab.
    """
    
    def __init__(self, bearer_token: str):
        """
        Initialize with a Bearer token.
        
        Args:
            bearer_token: Valid Bearer token from Spotify web interface
        """
        self.bearer_token = bearer_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://open.spotify.com',
            'Referer': 'https://open.spotify.com/',
            'Content-Type': 'application/json',
        })
        self.graphql_url = "https://api-partner.spotify.com/pathfinder/v1/query"
        self.web_api_url = "https://api.spotify.com/v1"
    
    def search_track(self, search_term: str, limit: int = 10) -> List[Dict]:
        """
        Search for tracks using Spotify's GraphQL endpoint with authentication.
        
        Args:
            search_term: Search query (e.g., "Paradisio Bailando" or "artist - song")
            limit: Number of results to return
            
        Returns:
            List of track dictionaries with song info
        """
        variables = {
            "searchTerm": search_term,
            "offset": 0,
            "limit": limit,
            "numberOfTopResults": 5,
            "includeAudiobooks": True,
            "includeArtistHasConcertsField": False,
            "includePreReleases": True,
            "includeLocalConcertsField": False,
            "includeAuthors": True
        }
        
        payload = {
            "variables": variables,
            "operationName": "searchDesktop",
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "d9f785900f0710b31c07818d617f4f7600c1e21217e80f5b043d1e78d74e6026"
                }
            }
        }
        
        try:
            response = self.session.post(self.graphql_url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'searchV2' in data['data']:
                tracks = []
                
                search_results = data['data']['searchV2']
                
                if 'tracksV2' in search_results and search_results['tracksV2']['items']:
                    for item in search_results['tracksV2']['items']:
                        if 'item' in item:
                            track_data = item['item']
                            track_info = self._extract_track_info(track_data)
                            if track_info:
                                tracks.append(track_info)
                
                return tracks
            else:
                print(f"Unexpected response format: {data}")
                return []
                
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                print("❌ Bearer token expired or invalid. Please get a fresh token.")
            else:
                print(f"Error searching for '{search_term}': {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return []
    
    def get_user_playlists(self, limit: int = 50) -> List[Dict]:
        """
        Get current user's playlists using Web API.
        
        Args:
            limit: Number of playlists to return
            
        Returns:
            List of playlist dictionaries
        """
        try:
            response = self.session.get(f"{self.web_api_url}/me/playlists", params={'limit': limit})
            response.raise_for_status()
            
            data = response.json()
            playlists = []
            
            for item in data.get('items', []):
                playlist_info = {
                    'id': item.get('id'),
                    'name': item.get('name'),
                    'description': item.get('description', ''),
                    'public': item.get('public', False),
                    'collaborative': item.get('collaborative', False),
                    'tracks_total': item.get('tracks', {}).get('total', 0),
                    'owner': item.get('owner', {}).get('display_name', 'Unknown'),
                    'url': item.get('external_urls', {}).get('spotify', ''),
                    'images': item.get('images', [])
                }
                playlists.append(playlist_info)
            
            return playlists
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                print("❌ Bearer token expired or invalid. Please get a fresh token.")
            else:
                print(f"Error getting playlists: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id: str, limit: int = 100) -> List[Dict]:
        """
        Get tracks from a specific playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            limit: Number of tracks to return
            
        Returns:
            List of track dictionaries
        """
        try:
            response = self.session.get(f"{self.web_api_url}/playlists/{playlist_id}/tracks", 
                                      params={'limit': limit})
            response.raise_for_status()
            
            data = response.json()
            tracks = []
            
            for item in data.get('items', []):
                if item.get('track'):
                    track = item['track']
                    track_info = {
                        'id': track.get('id'),
                        'name': track.get('name'),
                        'uri': track.get('uri'),
                        'artists': [{'name': artist['name'], 'id': artist['id']} 
                                  for artist in track.get('artists', [])],
                        'artist_names': [artist['name'] for artist in track.get('artists', [])],
                        'album': {
                            'name': track.get('album', {}).get('name'),
                            'id': track.get('album', {}).get('id'),
                        },
                        'duration_ms': track.get('duration_ms', 0),
                        'popularity': track.get('popularity', 0),
                        'explicit': track.get('explicit', False),
                        'external_urls': track.get('external_urls', {}),
                        'preview_url': track.get('preview_url')
                    }
                    tracks.append(track_info)
            
            return tracks
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                print("❌ Bearer token expired or invalid. Please get a fresh token.")
            else:
                print(f"Error getting playlist tracks: {e}")
            return []
    
    def create_playlist(self, user_id: str, name: str, description: str = "", public: bool = True) -> Optional[str]:
        """
        Create a new playlist (requires write permissions).
        
        Args:
            user_id: Spotify user ID
            name: Playlist name
            description: Playlist description
            public: Whether playlist should be public
            
        Returns:
            Playlist ID if successful, None otherwise
        """
        playlist_data = {
            'name': name,
            'description': description,
            'public': public
        }
        
        try:
            response = self.session.post(f"{self.web_api_url}/users/{user_id}/playlists", 
                                       json=playlist_data)
            response.raise_for_status()
            
            data = response.json()
            playlist_id = data.get('id')
            
            if playlist_id:
                print(f"✅ Created playlist: {name} (ID: {playlist_id})")
                return playlist_id
            else:
                print("❌ Failed to create playlist")
                return None
                
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                print("❌ Bearer token expired or invalid. Please get a fresh token.")
            elif response.status_code == 403:
                print("❌ Insufficient permissions to create playlist.")
            else:
                print(f"Error creating playlist: {e}")
            return None
    
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
        
        try:
            # Spotify API allows max 100 tracks per request
            batch_size = 100
            for i in range(0, len(track_uris), batch_size):
                batch = track_uris[i:i + batch_size]
                
                response = self.session.post(
                    f"{self.web_api_url}/playlists/{playlist_id}/tracks",
                    json={'uris': batch}
                )
                response.raise_for_status()
            
            print(f"✅ Added {len(track_uris)} tracks to playlist")
            return True
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                print("❌ Bearer token expired or invalid. Please get a fresh token.")
            elif response.status_code == 403:
                print("❌ Insufficient permissions to modify playlist.")
            else:
                print(f"Error adding tracks to playlist: {e}")
            return False
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user information."""
        try:
            response = self.session.get(f"{self.web_api_url}/me")
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                print("❌ Bearer token expired or invalid. Please get a fresh token.")
            else:
                print(f"Error getting user info: {e}")
            return None
    
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
        
        # Get current user
        user = self.get_current_user()
        if not user:
            return {"success": False, "error": "Could not get user info"}
        
        user_id = user.get('id')
        if not user_id:
            return {"success": False, "error": "Could not get user ID"}
        
        # Search for tracks
        track_uris = self.search_tracks_batch(songs_and_artists)
        
        if not track_uris:
            print("No tracks found, cannot create playlist")
            return {"success": False, "tracks_added": 0}
        
        # Create playlist
        playlist_id = self.create_playlist(user_id, playlist_name, playlist_description, public)
        if not playlist_id:
            return {"success": False, "error": "Failed to create playlist"}
        
        # Add tracks to playlist
        success = self.add_tracks_to_playlist(playlist_id, [t['uri'] for t in track_uris])
        
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
    
    def search_tracks_batch(self, songs_and_artists: List[Tuple[str, str]]) -> List[Dict]:
        """
        Search for multiple tracks and return track info with URIs.
        
        Args:
            songs_and_artists: List of (song, artist) tuples
            
        Returns:
            List of track dictionaries with URIs
        """
        found_tracks = []
        
        print(f"Searching for {len(songs_and_artists)} tracks...")
        
        for i, (song, artist) in enumerate(songs_and_artists):
            search_term = f"{artist} {song}"
            print(f"Searching [{i+1}/{len(songs_and_artists)}]: {search_term}")
            
            tracks = self.search_track(search_term, limit=3)
            
            if tracks:
                # Find best match
                best_match = self._find_best_match(song, artist, tracks)
                if best_match:
                    found_tracks.append(best_match)
                    print(f"✓ Found: {best_match['artist_names'][0]} - {best_match['name']}")
                else:
                    print(f"✗ No good match for: {artist} - {song}")
            else:
                print(f"✗ No results for: {artist} - {song}")
            
            # Be respectful with requests
            time.sleep(0.3)
        
        print(f"\nFound {len(found_tracks)} out of {len(songs_and_artists)} tracks")
        return found_tracks
    
    def _find_best_match(self, target_song: str, target_artist: str, tracks: List[Dict]) -> Optional[Dict]:
        """Find the best matching track from search results."""
        target_song_lower = target_song.lower()
        target_artist_lower = target_artist.lower()
        
        best_track = None
        best_score = 0
        
        for track in tracks:
            score = 0
            
            # Check song name similarity
            if target_song_lower in track['name'].lower():
                score += 3
            elif any(word in track['name'].lower() for word in target_song_lower.split()):
                score += 1
            
            # Check artist name similarity
            for artist in track['artist_names']:
                if target_artist_lower in artist.lower():
                    score += 3
                    break
                elif any(word in artist.lower() for word in target_artist_lower.split()):
                    score += 1
                    break
            
            if score > best_score:
                best_score = score
                best_track = track
        
        return best_track if best_score >= 2 else None
    
    def _extract_track_info(self, track_data: Dict) -> Optional[Dict]:
        """Extract relevant track information from Spotify's response."""
        try:
            track_info = {
                'name': track_data.get('name', 'Unknown'),
                'uri': track_data.get('uri', ''),
                'external_urls': track_data.get('external_urls', {}),
                'preview_url': track_data.get('preview_url'),
                'duration_ms': track_data.get('duration_ms', 0),
                'explicit': track_data.get('explicit', False),
                'popularity': track_data.get('popularity', 0),
            }
            
            # Extract artist information
            artists = []
            if 'artists' in track_data and 'items' in track_data['artists']:
                for artist in track_data['artists']['items']:
                    artists.append({
                        'name': artist.get('profile', {}).get('name', 'Unknown Artist'),
                        'uri': artist.get('uri', ''),
                    })
            track_info['artists'] = artists
            track_info['artist_names'] = [a['name'] for a in artists]
            
            # Extract album information
            if 'albumOfTrack' in track_data:
                album = track_data['albumOfTrack']
                track_info['album'] = {
                    'name': album.get('name', 'Unknown Album'),
                    'uri': album.get('uri', ''),
                    'release_date': album.get('date', {}).get('year'),
                }
                
                if 'coverArt' in album and 'sources' in album['coverArt']:
                    images = album['coverArt']['sources']
                    if images:
                        track_info['album']['images'] = images
                        track_info['album']['cover_url'] = images[0].get('url', '')
            
            return track_info
            
        except Exception as e:
            print(f"Error extracting track info: {e}")
            return None