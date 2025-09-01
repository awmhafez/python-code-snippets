#!/usr/bin/env python3
"""
Create a 90s/2000s Eurodance playlist using provided Bearer token.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utilities.spotify_token_scraper import SpotifyTokenScraper


def main():
    """Create the eurodance playlist."""
    
    # Your awesome 90s/2000s eurodance tracks!
    eurodance_songs = [
        ("Pump Up the Jam", "Technotronic"),
        ("Seven Days and One Week", "Def Dames Dope"),
        ("Bailando", "Paradisio"),
        ("You're a Superstar", "Love Inc."),
        ("Saturday Night", "Whigfield"),
        ("Barbie Girl", "Aqua"),
        ("Sandstorm", "Darude"),
        ("Around the World", "Daft Punk"),
        ("Music Sounds Better with You", "Stardust"),
        ("Rhythm Is a Dancer", "Snap!"),
        ("Mr. Vain", "Culture Beat"),
        ("What Is Love", "Haddaway"),
        ("Another Night", "Real McCoy"),
        ("Get-A-Way", "Maxx"),
        ("Eins, Zwei, Polizei", "Mo-Do"),
        ("Be My Lover", "La Bouche"),
        ("Coco Jambo", "Mr. President"),
        ("Bellissima", "DJ Quicksilver"),
        ("Ecuador", "Sash!"),
        ("Meet Her at the Love Parade", "Da Hool"),
        ("9PM (Till I Come)", "ATB"),
        ("Kernkraft 400", "Zombie Nation"),
        ("Around the World (La La La La La)", "ATC"),
        ("Rhythm of the Night", "Corona"),
        ("U Got 2 Let the Music", "Cappella"),
        ("Children", "Robert Miles"),
        ("Freed from Desire", "Gala"),
        ("Blue (Da Ba Dee)", "Eiffel 65"),
        ("L'Amour Toujours", "Gigi d'Agostino"),
        ("Get Ready for This", "2 Unlimited"),
        ("No Limit", "2 Unlimited"),
        ("This Is Your Night", "Amber"),
        ("We Like to Party!", "Vengaboys"),
        ("Boom, Boom, Boom, Boom!!", "Vengaboys"),
        ("We're Going to Ibiza", "Vengaboys"),
        ("Better Off Alone", "Alice Deejay"),
        ("Macarena", "Los Del Rio"),
        ("Cotton Eye Joe", "Rednex"),
        ("Beautiful Life", "Ace of Base"),
        ("Push the Feeling On", "Nightcrawlers"),
        ("Insomnia", "Faithless"),
        ("Gypsy Woman", "Crystal Waters"),
        ("Show Me Love", "Robin S."),
        ("Scatman", "Scatman John"),
        ("Real Love", "TTF")
    ]
    
    print("=== 90s/2000s EURODANCE PLAYLIST CREATOR ===")
    print("=" * 50)
    print(f"Ready to create playlist with {len(eurodance_songs)} classic tracks!")
    
    # You need to provide a fresh Bearer token here
    print("\nNOTE: You need to provide a fresh Bearer token.")
    print("1. Go to https://open.spotify.com in your browser")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Network tab")  
    print("4. Search for something on Spotify")
    print("5. Look for requests with 'Authorization: Bearer ...'")
    print("6. Copy the token and update this script")
    print()
    
    # YOU NEED TO PUT YOUR BEARER TOKEN HERE
    bearer_token = "PUT_YOUR_FRESH_BEARER_TOKEN_HERE"
    
    if bearer_token == "PUT_YOUR_FRESH_BEARER_TOKEN_HERE":
        print("ERROR: Please update the script with your Bearer token!")
        return
    
    try:
        # Create scraper instance
        print("Initializing Spotify connection...")
        scraper = SpotifyTokenScraper(bearer_token)
        
        # Test the token by getting user info
        user = scraper.get_current_user()
        if not user:
            print("ERROR: Invalid or expired Bearer token")
            print("Please get a fresh token and update the script")
            return
        
        print(f"Hello {user.get('display_name', 'User')}!")
        
        # Create the playlist
        playlist_name = "90s 2000s Eurodance Classics"
        playlist_description = "The ultimate collection of 90s and early 2000s eurodance hits! Featuring Technotronic, Paradisio, Darude, Daft Punk, Snap!, and many more. Perfect for parties, workouts, or nostalgic dance sessions! Created with Python"
        
        print(f"\nCreating playlist: {playlist_name}")
        print("This may take a few minutes to search for all tracks...")
        
        result = scraper.create_playlist_from_songs(
            songs_and_artists=eurodance_songs,
            playlist_name=playlist_name,
            playlist_description=playlist_description,
            public=True
        )
        
        if result['success']:
            print("\n" + "="*60)
            print("SUCCESS! Your eurodance playlist is ready!")
            print("="*60)
            print(f"Playlist URL: {result['playlist_url']}")
            print(f"Tracks added: {result['tracks_found']}/{result['tracks_requested']}")
            
            # Show some stats
            success_rate = (result['tracks_found'] / result['tracks_requested']) * 100
            print(f"Success rate: {success_rate:.1f}%")
            
            if result['tracks_found'] != result['tracks_requested']:
                print(f"\nNote: {result['tracks_requested'] - result['tracks_found']} tracks couldn't be found.")
                print("This might be due to:")
                print("  - Different song titles/artist names on Spotify")
                print("  - Tracks not available in your region")
                print("  - Alternate versions or remixes")
                
            print("\nEnjoy your throwback playlist!")
        else:
            print("ERROR: Failed to create playlist")
            if 'error' in result:
                print(f"Error: {result['error']}")
                
    except Exception as e:
        print(f"ERROR: {e}")
        print("\nTroubleshooting tips:")
        print("- Make sure your Bearer token is valid and not expired")
        print("- Get a fresh token from your browser's Network tab")
        print("- Update the script with your fresh token")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPlaylist creation cancelled")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()