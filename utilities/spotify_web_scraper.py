import requests
import json
from typing import List, Dict, Optional, Tuple
import urllib.parse
import time


class SpotifyWebScraper:
    """
    Spotify track search using web scraping methods (no API credentials required).
    
    Note: This uses Spotify's public web endpoints and GraphQL queries.
    This is for educational purposes and may break if Spotify changes their frontend.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://open.spotify.com',
            'Referer': 'https://open.spotify.com/',
        })
        self.graphql_url = "https://api-partner.spotify.com/pathfinder/v1/query"
    
    def search_track(self, search_term: str, limit: int = 10) -> List[Dict]:
        """
        Search for tracks using Spotify's GraphQL endpoint.
        
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
                
                # Extract tracks from search results
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
            print(f"Error searching for '{search_term}': {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return []
    
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
                
                # Extract cover art
                if 'coverArt' in album and 'sources' in album['coverArt']:
                    images = album['coverArt']['sources']
                    if images:
                        track_info['album']['images'] = images
                        track_info['album']['cover_url'] = images[0].get('url', '')
            
            return track_info
            
        except Exception as e:
            print(f"Error extracting track info: {e}")
            return None
    
    def search_tracks_batch(self, songs_and_artists: List[Tuple[str, str]]) -> List[Dict]:
        """
        Search for multiple tracks.
        
        Args:
            songs_and_artists: List of (song, artist) tuples
            
        Returns:
            List of track information dictionaries
        """
        all_tracks = []
        
        print(f"Searching for {len(songs_and_artists)} tracks...")
        
        for i, (song, artist) in enumerate(songs_and_artists):
            search_term = f"{artist} {song}"
            print(f"Searching [{i+1}/{len(songs_and_artists)}]: {search_term}")
            
            tracks = self.search_track(search_term, limit=3)
            
            if tracks:
                # Try to find the best match
                best_match = self._find_best_match(song, artist, tracks)
                if best_match:
                    all_tracks.append(best_match)
                    print(f"✓ Found: {best_match['artist_names'][0]} - {best_match['name']}")
                else:
                    print(f"✗ No good match found for: {artist} - {song}")
            else:
                print(f"✗ No results for: {artist} - {song}")
            
            # Be respectful with requests
            time.sleep(0.5)
        
        print(f"\nFound {len(all_tracks)} out of {len(songs_and_artists)} tracks")
        return all_tracks
    
    def _find_best_match(self, target_song: str, target_artist: str, tracks: List[Dict]) -> Optional[Dict]:
        """Find the best matching track from search results."""
        target_song_lower = target_song.lower()
        target_artist_lower = target_artist.lower()
        
        # Score each track based on similarity
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
        
        # Only return if we have a reasonable match
        return best_track if best_score >= 2 else None
    
    def get_track_info(self, spotify_uri_or_url: str) -> Optional[Dict]:
        """
        Get detailed information about a specific track.
        
        Args:
            spotify_uri_or_url: Spotify URI (spotify:track:xxx) or URL
            
        Returns:
            Track information dictionary
        """
        # Extract track ID from URI or URL
        track_id = self._extract_track_id(spotify_uri_or_url)
        if not track_id:
            return None
        
        # Search for the track specifically
        # This is a simplified approach - you might need to implement
        # a specific track lookup if available
        return None
    
    def _extract_track_id(self, uri_or_url: str) -> Optional[str]:
        """Extract Spotify track ID from URI or URL."""
        if uri_or_url.startswith('spotify:track:'):
            return uri_or_url.split(':')[-1]
        elif 'open.spotify.com/track/' in uri_or_url:
            return uri_or_url.split('/track/')[-1].split('?')[0]
        return None
    
    def format_track_list(self, tracks: List[Dict]) -> str:
        """Format track list for display."""
        output = []
        for i, track in enumerate(tracks, 1):
            artists = ", ".join(track['artist_names'])
            duration = self._format_duration(track['duration_ms'])
            output.append(f"{i:2d}. {artists} - {track['name']} ({duration})")
        return "\n".join(output)
    
    def _format_duration(self, duration_ms: int) -> str:
        """Format duration from milliseconds to MM:SS."""
        if not duration_ms:
            return "0:00"
        
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"
    
    def export_to_text(self, tracks: List[Dict], filename: str = "spotify_tracks.txt"):
        """Export track list to a text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Spotify Track List\n")
            f.write("=" * 50 + "\n\n")
            
            for track in tracks:
                artists = ", ".join(track['artist_names'])
                f.write(f"Track: {track['name']}\n")
                f.write(f"Artist(s): {artists}\n")
                f.write(f"Album: {track.get('album', {}).get('name', 'Unknown')}\n")
                f.write(f"Duration: {self._format_duration(track['duration_ms'])}\n")
                
                if track.get('external_urls', {}).get('spotify'):
                    f.write(f"Spotify URL: {track['external_urls']['spotify']}\n")
                
                f.write("-" * 30 + "\n")
        
        print(f"Exported {len(tracks)} tracks to {filename}")
    
    def export_to_csv(self, tracks: List[Dict], filename: str = "spotify_tracks.csv"):
        """Export track list to CSV format."""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Track Name', 'Artist(s)', 'Album', 'Duration', 'Spotify URL', 'Popularity'])
            
            for track in tracks:
                artists = ", ".join(track['artist_names'])
                duration = self._format_duration(track['duration_ms'])
                spotify_url = track.get('external_urls', {}).get('spotify', '')
                album_name = track.get('album', {}).get('name', 'Unknown')
                
                writer.writerow([
                    track['name'],
                    artists,
                    album_name,
                    duration,
                    spotify_url,
                    track.get('popularity', 0)
                ])
        
        print(f"Exported {len(tracks)} tracks to {filename}")