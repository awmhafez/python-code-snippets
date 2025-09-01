#!/usr/bin/env python3
"""
Example usage of Spotify Token Scraper - CREATE ACTUAL PLAYLISTS!

This version can actually create playlists and add songs using a Bearer token
from your browser's Spotify session.

HOW TO GET BEARER TOKEN:
1. Go to https://open.spotify.com in your browser
2. Log in to your Spotify account
3. Open Developer Tools (F12)
4. Go to Network tab
5. Search for something or navigate around Spotify
6. Look for requests to "api-partner.spotify.com" or "api.spotify.com"
7. In the request headers, find "Authorization: Bearer ..."
8. Copy everything after "Bearer " (the long token)

Usage:
    python spotify_token_example.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utilities.spotify_token_scraper import SpotifyTokenScraper


def get_bearer_token():
    """Get Bearer token from user input or environment variable."""
    # Check if token is set as environment variable
    token = os.getenv('SPOTIFY_BEARER_TOKEN')
    
    if token:
        print("✅ Found Bearer token in environment variable")
        return token
    
    print("📝 Enter your Spotify Bearer token:")
    print("(Get this from your browser's Network tab when logged into Spotify)")
    token = input("Bearer token: ").strip()
    
    if token.startswith('Bearer '):
        token = token[7:]  # Remove 'Bearer ' prefix if present
    
    return token


def example_search_and_create_playlist():
    """Create an actual Spotify playlist with songs."""
    token = get_bearer_token()
    
    if not token:
        print("❌ No Bearer token provided")
        return
    
    try:
        scraper = SpotifyTokenScraper(token)
        
        # Test the token by getting user info
        user = scraper.get_current_user()
        if not user:
            print("❌ Invalid or expired token")
            return
        
        print(f"👋 Hello {user.get('display_name', 'User')}!")
        print(f"📊 Followers: {user.get('followers', {}).get('total', 0)}")
        
        # Songs to add to playlist
        party_songs = [
            ("Bailando", "Paradisio"),
            ("Macarena", "Los Del Rio"),
            ("Despacito", "Luis Fonsi"),
            ("Uptown Funk", "Mark Ronson ft. Bruno Mars"),
            ("Shape of You", "Ed Sheeran"),
            ("Blinding Lights", "The Weeknd"),
            ("Levitating", "Dua Lipa"),
            ("Don't Start Now", "Dua Lipa"),
            ("Watermelon Sugar", "Harry Styles"),
            ("Good 4 U", "Olivia Rodrigo")
        ]
        
        # Create the playlist
        result = scraper.create_playlist_from_songs(
            songs_and_artists=party_songs,
            playlist_name="🎉 Party Hits (Created with Python)",
            playlist_description="A fun party playlist created using Python and Spotify's API",
            public=True
        )
        
        if result['success']:
            print(f"\n🎉 SUCCESS! Your playlist is ready!")
            print(f"🔗 {result['playlist_url']}")
            print(f"📊 Added {result['tracks_found']}/{result['tracks_requested']} tracks")
        else:
            print("❌ Failed to create playlist")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_list_your_playlists():
    """List user's existing playlists."""
    token = get_bearer_token()
    
    if not token:
        print("❌ No Bearer token provided")
        return
    
    try:
        scraper = SpotifyTokenScraper(token)
        
        # Get user's playlists
        playlists = scraper.get_user_playlists(limit=20)
        
        if playlists:
            print(f"\n📂 Your Playlists ({len(playlists)} shown):")
            print("-" * 60)
            
            for i, playlist in enumerate(playlists, 1):
                owner = playlist['owner']
                track_count = playlist['tracks_total']
                visibility = "Public" if playlist['public'] else "Private"
                
                print(f"{i:2d}. {playlist['name']}")
                print(f"    👤 By: {owner} | 🎵 {track_count} tracks | 🔒 {visibility}")
                if playlist['description']:
                    print(f"    💬 {playlist['description'][:80]}...")
                print(f"    🔗 {playlist['url']}")
                print()
        else:
            print("No playlists found")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_add_to_existing_playlist():
    """Add songs to an existing playlist."""
    token = get_bearer_token()
    
    if not token:
        print("❌ No Bearer token provided")
        return
    
    try:
        scraper = SpotifyTokenScraper(token)
        
        # List user's playlists first
        playlists = scraper.get_user_playlists(limit=10)
        
        if not playlists:
            print("No playlists found")
            return
        
        print("\n📂 Your Playlists:")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i:2d}. {playlist['name']} ({playlist['tracks_total']} tracks)")
        
        # Ask user to pick a playlist
        try:
            choice = int(input("\nEnter playlist number to add songs to: ")) - 1
            if not (0 <= choice < len(playlists)):
                print("Invalid choice")
                return
        except ValueError:
            print("Invalid input")
            return
        
        selected_playlist = playlists[choice]
        print(f"\n🎯 Selected: {selected_playlist['name']}")
        
        # Songs to add
        new_songs = [
            ("As It Was", "Harry Styles"),
            ("Anti-Hero", "Taylor Swift"),
            ("Flowers", "Miley Cyrus"),
            ("Unholy", "Sam Smith ft. Kim Petras"),
            ("Calm Down", "Rema")
        ]
        
        print(f"🔍 Searching for {len(new_songs)} songs to add...")
        
        # Search for tracks
        found_tracks = scraper.search_tracks_batch(new_songs)
        
        if found_tracks:
            track_uris = [track['uri'] for track in found_tracks]
            success = scraper.add_tracks_to_playlist(selected_playlist['id'], track_uris)
            
            if success:
                print(f"✅ Added {len(found_tracks)} songs to '{selected_playlist['name']}'!")
                print(f"🔗 {selected_playlist['url']}")
            else:
                print("❌ Failed to add songs")
        else:
            print("No songs found to add")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_playlist_analyzer():
    """Analyze an existing playlist."""
    token = get_bearer_token()
    
    if not token:
        print("❌ No Bearer token provided")
        return
    
    try:
        scraper = SpotifyTokenScraper(token)
        
        # Get a playlist ID from user
        playlist_url = input("Enter Spotify playlist URL: ").strip()
        
        # Extract playlist ID from URL
        if 'playlist/' in playlist_url:
            playlist_id = playlist_url.split('playlist/')[-1].split('?')[0]
        else:
            playlist_id = playlist_url  # Assume it's already an ID
        
        print(f"📊 Analyzing playlist: {playlist_id}")
        
        # Get playlist tracks
        tracks = scraper.get_playlist_tracks(playlist_id)
        
        if tracks:
            print(f"\n🎵 Found {len(tracks)} tracks")
            
            # Calculate stats
            total_duration = sum(track['duration_ms'] for track in tracks)
            avg_popularity = sum(track['popularity'] for track in tracks) / len(tracks)
            explicit_count = sum(1 for track in tracks if track['explicit'])
            
            # Get unique artists
            all_artists = []
            for track in tracks:
                all_artists.extend(track['artist_names'])
            unique_artists = len(set(all_artists))
            
            print(f"\n📈 Playlist Statistics:")
            print(f"   🕒 Total duration: {total_duration // 60000} minutes")
            print(f"   ⭐ Average popularity: {avg_popularity:.1f}/100")
            print(f"   👥 Unique artists: {unique_artists}")
            print(f"   🔞 Explicit tracks: {explicit_count}")
            
            # Show top tracks by popularity
            top_tracks = sorted(tracks, key=lambda x: x['popularity'], reverse=True)[:5]
            print(f"\n🔥 Top 5 Most Popular Tracks:")
            for i, track in enumerate(top_tracks, 1):
                artists = ", ".join(track['artist_names'])
                print(f"   {i}. {artists} - {track['name']} ({track['popularity']}/100)")
            
            # Export option
            export = input("\n💾 Export playlist data? (csv/txt/n): ").lower()
            if export == 'csv':
                filename = f"playlist_analysis_{playlist_id}.csv"
                scraper.export_to_csv(tracks, filename)
            elif export == 'txt':
                filename = f"playlist_analysis_{playlist_id}.txt"
                scraper.export_to_text(tracks, filename)
        else:
            print("No tracks found in playlist")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🎵 Spotify Token Scraper - CREATE REAL PLAYLISTS!")
    print("=" * 55)
    
    print("\nChoose an option:")
    print("1. 🎉 Create a new party playlist")
    print("2. 📂 List your playlists")
    print("3. ➕ Add songs to existing playlist")
    print("4. 📊 Analyze a playlist")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    try:
        if choice == "1":
            example_search_and_create_playlist()
        elif choice == "2":
            example_list_your_playlists()
        elif choice == "3":
            example_add_to_existing_playlist()
        elif choice == "4":
            example_playlist_analyzer()
        else:
            print("Invalid choice. Creating party playlist...")
            example_search_and_create_playlist()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\nTips:")
        print("- Make sure your Bearer token is valid and not expired")
        print("- Get a fresh token from your browser's Network tab")
        print("- Check that you're logged into Spotify in your browser")