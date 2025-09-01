#!/usr/bin/env python3
"""
Example usage of the Spotify Web Scraper (no authentication required).

This example shows how to search for songs and get track information
without needing to create a Spotify app or API credentials.

Usage:
    python spotify_scraper_example.py

Note: This uses web scraping and may break if Spotify changes their frontend.
For production use, consider the official API approach.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utilities.spotify_web_scraper import SpotifyWebScraper


def example_single_search():
    """Example of searching for a single track."""
    print("🎵 Single Track Search Example")
    print("-" * 40)
    
    scraper = SpotifyWebScraper()
    
    # Search for a specific song
    search_term = "Paradisio Bailando"
    print(f"Searching for: {search_term}")
    
    tracks = scraper.search_track(search_term, limit=5)
    
    if tracks:
        print(f"\nFound {len(tracks)} results:")
        print(scraper.format_track_list(tracks))
        
        # Show detailed info for first result
        if tracks:
            track = tracks[0]
            print(f"\n📋 Details for top result:")
            print(f"   Name: {track['name']}")
            print(f"   Artist(s): {', '.join(track['artist_names'])}")
            if 'album' in track:
                print(f"   Album: {track['album']['name']}")
                print(f"   Release: {track['album'].get('release_date', 'Unknown')}")
            print(f"   Duration: {scraper._format_duration(track['duration_ms'])}")
            print(f"   Popularity: {track.get('popularity', 0)}/100")
            
            if track.get('external_urls', {}).get('spotify'):
                print(f"   Spotify URL: {track['external_urls']['spotify']}")
    else:
        print("No tracks found!")


def example_batch_search():
    """Example of searching for multiple tracks."""
    print("\n🎵 Batch Track Search Example")
    print("-" * 40)
    
    scraper = SpotifyWebScraper()
    
    # List of songs to search for
    songs_to_find = [
        ("Bailando", "Paradisio"),
        ("Macarena", "Los Del Rio"),
        ("Despacito", "Luis Fonsi"),
        ("Gangnam Style", "PSY"),
        ("Shape of You", "Ed Sheeran"),
        ("Blinding Lights", "The Weeknd")
    ]
    
    print(f"Searching for {len(songs_to_find)} tracks...")
    
    found_tracks = scraper.search_tracks_batch(songs_to_find)
    
    if found_tracks:
        print(f"\n📋 Summary of found tracks:")
        print(scraper.format_track_list(found_tracks))
        
        # Export options
        export_choice = input("\nWould you like to export these tracks? (txt/csv/n): ").lower()
        
        if export_choice == 'txt':
            scraper.export_to_text(found_tracks, "found_tracks.txt")
        elif export_choice == 'csv':
            scraper.export_to_csv(found_tracks, "found_tracks.csv")
        elif export_choice != 'n':
            print("Invalid choice, skipping export.")
    else:
        print("No tracks found!")


def example_interactive_search():
    """Interactive search where user enters songs."""
    print("\n🎵 Interactive Search Example")
    print("-" * 40)
    
    scraper = SpotifyWebScraper()
    
    print("Enter songs to search for (format: 'artist - song' or just search terms)")
    print("Press Enter on empty line to finish.")
    
    search_queries = []
    while True:
        query = input(">> ").strip()
        if not query:
            break
        search_queries.append(query)
    
    if not search_queries:
        print("No search queries entered.")
        return
    
    all_found_tracks = []
    
    for i, query in enumerate(search_queries, 1):
        print(f"\n[{i}/{len(search_queries)}] Searching: {query}")
        tracks = scraper.search_track(query, limit=3)
        
        if tracks:
            print("Results:")
            for j, track in enumerate(tracks, 1):
                artists = ", ".join(track['artist_names'])
                print(f"  {j}. {artists} - {track['name']}")
            
            # Ask user to pick one
            try:
                choice = input(f"Pick result (1-{len(tracks)}, or 0 to skip): ").strip()
                if choice and choice.isdigit():
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(tracks):
                        all_found_tracks.append(tracks[choice_idx])
                        print("✓ Added to collection")
                    elif int(choice) == 0:
                        print("○ Skipped")
                    else:
                        print("Invalid choice, skipping")
                else:
                    print("○ Skipped")
            except ValueError:
                print("Invalid input, skipping")
        else:
            print("✗ No results found")
    
    if all_found_tracks:
        print(f"\n📋 Final collection ({len(all_found_tracks)} tracks):")
        print(scraper.format_track_list(all_found_tracks))
        
        # Export options
        export = input("\nExport to file? (txt/csv/n): ").lower()
        if export == 'txt':
            scraper.export_to_text(all_found_tracks, "my_collection.txt")
        elif export == 'csv':
            scraper.export_to_csv(all_found_tracks, "my_collection.csv")
    else:
        print("No tracks in final collection.")


def example_playlist_recreation():
    """Example showing how to recreate a playlist based on song list."""
    print("\n🎵 Playlist Recreation Example")
    print("-" * 40)
    
    scraper = SpotifyWebScraper()
    
    # Example: Classic hits playlist
    classic_hits = [
        ("Bohemian Rhapsody", "Queen"),
        ("Hotel California", "Eagles"),
        ("Sweet Child O' Mine", "Guns N' Roses"),
        ("Smells Like Teen Spirit", "Nirvana"),
        ("Billie Jean", "Michael Jackson"),
        ("Like a Rolling Stone", "Bob Dylan"),
        ("Stairway to Heaven", "Led Zeppelin"),
        ("Hey Jude", "The Beatles"),
        ("Purple Haze", "Jimi Hendrix"),
        ("Imagine", "John Lennon")
    ]
    
    print(f"🎸 Recreating 'Classic Rock Hits' playlist with {len(classic_hits)} tracks...")
    
    found_tracks = scraper.search_tracks_batch(classic_hits)
    
    if found_tracks:
        print(f"\n✅ Successfully found {len(found_tracks)}/{len(classic_hits)} tracks!")
        print("\n📋 Playlist Contents:")
        print(scraper.format_track_list(found_tracks))
        
        # Calculate total duration
        total_ms = sum(track.get('duration_ms', 0) for track in found_tracks)
        total_duration = scraper._format_duration(total_ms)
        total_minutes = total_ms // 60000
        
        print(f"\n📊 Playlist Stats:")
        print(f"   Total tracks: {len(found_tracks)}")
        print(f"   Total duration: {total_duration} ({total_minutes} minutes)")
        
        avg_popularity = sum(track.get('popularity', 0) for track in found_tracks) / len(found_tracks)
        print(f"   Average popularity: {avg_popularity:.1f}/100")
        
        # Export full playlist
        scraper.export_to_text(found_tracks, "classic_rock_playlist.txt")
        scraper.export_to_csv(found_tracks, "classic_rock_playlist.csv")
        
        print(f"\n💾 Playlist exported to:")
        print(f"   - classic_rock_playlist.txt")
        print(f"   - classic_rock_playlist.csv")
    else:
        print("❌ No tracks found for playlist!")


if __name__ == "__main__":
    print("🎵 Spotify Web Scraper Examples")
    print("=" * 50)
    print("Choose an example to run:")
    print("1. Single track search")
    print("2. Batch search with predefined songs")
    print("3. Interactive search (enter your own songs)")
    print("4. Recreate a classic rock playlist")
    print("5. Run all examples")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    try:
        if choice == "1":
            example_single_search()
        elif choice == "2":
            example_batch_search()
        elif choice == "3":
            example_interactive_search()
        elif choice == "4":
            example_playlist_recreation()
        elif choice == "5":
            example_single_search()
            example_batch_search()
            example_playlist_recreation()
        else:
            print("Invalid choice. Running single search example...")
            example_single_search()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("This might happen if Spotify changes their web interface.")
        print("Try again later or consider using the official API approach.")