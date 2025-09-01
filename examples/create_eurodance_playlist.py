#!/usr/bin/env python3
"""
Create a 90s/2000s Eurodance playlist from the provided song list.
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
        ("Get‑A‑Way", "Maxx"),
        ("Eins, Zwei, Polizei", "Mo‑Do"),
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
        ("Macarena", "Los Del Río"),
        ("Cotton Eye Joe", "Rednex"),
        ("Beautiful Life", "Ace of Base"),
        ("Push the Feeling On", "Nightcrawlers"),
        ("Insomnia", "Faithless"),
        ("Gypsy Woman", "Crystal Waters"),
        ("Show Me Love", "Robin S."),
        ("Scatman", "Scatman John"),
        ("Real Love", "TTF")
    ]
    
    print("🎵 90s/2000s EURODANCE PLAYLIST CREATOR")
    print("=" * 50)
    print(f"🎯 Ready to create playlist with {len(eurodance_songs)} classic tracks!")
    
    # Get Bearer token
    bearer_token = os.getenv('SPOTIFY_BEARER_TOKEN')
    
    if not bearer_token:
        print("📝 Enter your Spotify Bearer token:")
        print("(Get this from your browser's Network tab when logged into Spotify)")
        bearer_token = input("Bearer token: ").strip()
        
        if bearer_token.startswith('Bearer '):
            bearer_token = bearer_token[7:]  # Remove 'Bearer ' prefix if present
    
    if not bearer_token:
        print("❌ No Bearer token provided")
        return
    
    try:
        # Create scraper instance
        scraper = SpotifyTokenScraper(bearer_token)
        
        # Test the token by getting user info
        user = scraper.get_current_user()
        if not user:
            print("❌ Invalid or expired Bearer token")
            print("💡 Get a fresh token from your browser's Network tab")
            return
        
        print(f"👋 Hello {user.get('display_name', 'User')}!")
        
        # Create the playlist
        playlist_name = "🕺 90s/2000s Eurodance Classics"
        playlist_description = """
The ultimate collection of 90s and early 2000s eurodance hits! 
Featuring Technotronic, Paradisio, Darude, Daft Punk, Snap!, and many more. 
Perfect for parties, workouts, or nostalgic dance sessions! 
🎵 Created with Python 🐍
        """.strip()
        
        print(f"\n🎉 Creating playlist: {playlist_name}")
        
        result = scraper.create_playlist_from_songs(
            songs_and_artists=eurodance_songs,
            playlist_name=playlist_name,
            playlist_description=playlist_description,
            public=True
        )
        
        if result['success']:
            print(f"\n🎉 SUCCESS! Your eurodance playlist is ready!")
            print(f"🔗 {result['playlist_url']}")
            print(f"📊 Added {result['tracks_found']}/{result['tracks_requested']} tracks")
            
            # Show some stats
            success_rate = (result['tracks_found'] / result['tracks_requested']) * 100
            print(f"✨ Success rate: {success_rate:.1f}%")
            
            if result['tracks_found'] != result['tracks_requested']:
                print(f"\n💡 {result['tracks_requested'] - result['tracks_found']} tracks couldn't be found.")
                print("This might be due to:")
                print("  - Different song titles/artist names on Spotify")
                print("  - Tracks not available in your region")
                print("  - Alternate versions or remixes")
        else:
            print("❌ Failed to create playlist")
            if 'error' in result:
                print(f"Error: {result['error']}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("- Make sure your Bearer token is valid and not expired")
        print("- Get a fresh token from your browser's Network tab")
        print("- Check that you're logged into Spotify in your browser")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Playlist creation cancelled")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()