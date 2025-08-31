#!/usr/bin/env python3
"""
Example usage of the Spotify Playlist Manager.

Before running this script:
1. Create a Spotify app at https://developer.spotify.com/dashboard/applications
2. Set environment variables:
   - SPOTIFY_CLIENT_ID
   - SPOTIFY_CLIENT_SECRET  
   - SPOTIFY_REDIRECT_URI (optional, defaults to http://localhost:8080)
3. Install required packages: pip install spotipy

Usage:
    python spotify_playlist_example.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utilities.spotify_playlist_manager import SpotifyPlaylistManager


def example_create_playlist():
    """Example of creating a playlist from a list of songs."""
    
    # Sample songs list - replace with your own
    songs_to_add = [
        ("Bohemian Rhapsody", "Queen"),
        ("Hotel California", "Eagles"),
        ("Stairway to Heaven", "Led Zeppelin"),
        ("Sweet Child O' Mine", "Guns N' Roses"),
        ("Smells Like Teen Spirit", "Nirvana"),
        ("Billie Jean", "Michael Jackson"),
        ("Like a Rolling Stone", "Bob Dylan"),
        ("Purple Haze", "Jimi Hendrix"),
        ("Hey Jude", "The Beatles"),
        ("Imagine", "John Lennon")
    ]
    
    try:
        # Initialize the Spotify manager
        spotify_manager = SpotifyPlaylistManager()
        
        # Create playlist with the songs
        result = spotify_manager.create_playlist_from_songs(
            songs_and_artists=songs_to_add,
            playlist_name="Classic Rock Hits",
            playlist_description="A collection of classic rock songs created with Python",
            public=True
        )
        
        if result["success"]:
            print(f"\n✅ Success! Playlist created:")
            print(f"   - Playlist ID: {result['playlist_id']}")
            print(f"   - URL: {result['playlist_url']}")
            print(f"   - Tracks added: {result['tracks_found']}/{result['tracks_requested']}")
        else:
            print("❌ Failed to create playlist")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nMake sure to set your Spotify API credentials:")
        print("   export SPOTIFY_CLIENT_ID='your_client_id'")
        print("   export SPOTIFY_CLIENT_SECRET='your_client_secret'")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_add_to_existing_playlist():
    """Example of adding songs to an existing playlist."""
    
    # Additional songs to add
    new_songs = [
        ("Don't Stop Believin'", "Journey"),
        ("Sweet Home Alabama", "Lynyrd Skynyrd"),
        ("Born to Run", "Bruce Springsteen")
    ]
    
    try:
        spotify_manager = SpotifyPlaylistManager()
        
        # You'll need to replace this with an actual playlist ID
        # You can get this from the playlist URL: https://open.spotify.com/playlist/PLAYLIST_ID
        playlist_id = "your_playlist_id_here"
        
        print(f"Searching for {len(new_songs)} new songs...")
        track_uris = spotify_manager.search_tracks_batch(new_songs)
        
        if track_uris:
            success = spotify_manager.add_tracks_to_playlist(playlist_id, track_uris)
            if success:
                print(f"✅ Added {len(track_uris)} songs to playlist!")
            else:
                print("❌ Failed to add songs to playlist")
        else:
            print("❌ No songs found to add")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_song_list():
    """Example with a custom function to read songs from user input."""
    
    def get_songs_from_user():
        """Get songs from user input."""
        songs = []
        print("Enter songs in the format 'Song Title - Artist Name' (empty line to finish):")
        
        while True:
            line = input(">> ").strip()
            if not line:
                break
            
            if ' - ' in line:
                song, artist = line.split(' - ', 1)
                songs.append((song.strip(), artist.strip()))
            else:
                print("Invalid format. Use: Song Title - Artist Name")
        
        return songs
    
    try:
        spotify_manager = SpotifyPlaylistManager()
        
        # Get songs from user
        songs = get_songs_from_user()
        
        if not songs:
            print("No songs entered.")
            return
        
        # Get playlist name
        playlist_name = input("Enter playlist name: ").strip()
        if not playlist_name:
            playlist_name = "My Custom Playlist"
        
        # Create playlist
        result = spotify_manager.create_playlist_from_songs(
            songs_and_artists=songs,
            playlist_name=playlist_name,
            playlist_description="Custom playlist created with Python"
        )
        
        if result["success"]:
            print(f"\n🎵 Playlist '{playlist_name}' created successfully!")
            print(f"URL: {result['playlist_url']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🎵 Spotify Playlist Manager Example")
    print("=" * 40)
    
    # Check if credentials are set
    if not os.getenv('SPOTIFY_CLIENT_ID') or not os.getenv('SPOTIFY_CLIENT_SECRET'):
        print("⚠️  Warning: Spotify API credentials not found in environment variables.")
        print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before running.")
        print("\nYou can get these from: https://developer.spotify.com/dashboard/applications")
        sys.exit(1)
    
    print("\nChoose an example:")
    print("1. Create playlist with predefined songs")
    print("2. Add songs to existing playlist")
    print("3. Create playlist with custom song list")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        example_create_playlist()
    elif choice == "2":
        example_add_to_existing_playlist()
    elif choice == "3":
        example_custom_song_list()
    else:
        print("Invalid choice. Running default example...")
        example_create_playlist()