#!/usr/bin/env python3
"""
Test script to verify the updated response parsing works correctly.

This script loads the example JSON response and tests our track extraction logic.
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utilities.spotify_web_scraper import SpotifyWebScraper
from utilities.spotify_token_scraper import SpotifyTokenScraper


def test_response_parsing():
    """Test parsing with the actual response format."""
    print("🧪 Testing Response Parsing")
    print("-" * 40)
    
    # Load the example response
    try:
        with open('../utilities/example-response.json', 'r', encoding='utf-8') as f:
            response_data = json.load(f)
    except FileNotFoundError:
        print("❌ example-response.json not found")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return
    
    print("✅ Loaded example response successfully")
    
    # Create scraper instance (we'll test the parsing logic directly)
    scraper = SpotifyWebScraper()
    
    # Extract tracks from the response
    if 'data' in response_data and 'searchV2' in response_data['data']:
        search_results = response_data['data']['searchV2']
        
        if 'tracksV2' in search_results and search_results['tracksV2']['items']:
            tracks = []
            
            print(f"📋 Found {len(search_results['tracksV2']['items'])} track items in response")
            
            for i, item in enumerate(search_results['tracksV2']['items'][:3]):  # Test first 3
                if 'item' in item:
                    track_data = item['item']
                    track_info = scraper._extract_track_info(track_data)
                    if track_info:
                        tracks.append(track_info)
                        print(f"\n✅ Track {i+1} parsed successfully:")
                        print(f"   Name: {track_info['name']}")
                        print(f"   Artists: {', '.join(track_info['artist_names'])}")
                        print(f"   Album: {track_info.get('album', {}).get('name', 'Unknown')}")
                        print(f"   Duration: {scraper._format_duration(track_info['duration_ms'])}")
                        print(f"   URI: {track_info['uri']}")
                        print(f"   URL: {track_info.get('external_urls', {}).get('spotify', 'N/A')}")
                        print(f"   Playable: {track_info.get('playable', 'Unknown')}")
                    else:
                        print(f"❌ Failed to parse track {i+1}")
            
            if tracks:
                print(f"\n🎵 Successfully parsed {len(tracks)} tracks!")
                
                # Test export functionality
                scraper.export_to_text(tracks, "test_tracks.txt")
                scraper.export_to_csv(tracks, "test_tracks.csv")
                
                print("💾 Exported test results to:")
                print("   - test_tracks.txt")
                print("   - test_tracks.csv")
            else:
                print("❌ No tracks could be parsed")
        else:
            print("❌ No tracks found in response structure")
    else:
        print("❌ Invalid response structure")


def test_search_term_extraction():
    """Test extracting information about the search term used."""
    print("\n🔍 Testing Search Term Extraction")
    print("-" * 40)
    
    try:
        with open('../utilities/example-response.json', 'r', encoding='utf-8') as f:
            response_data = json.load(f)
        
        # The search term should be "Paradisio – Bailando" based on your example
        print("🎯 This response appears to be for search: 'Paradisio – Bailando'")
        
        # Check if we can find evidence of this in the results
        if 'data' in response_data and 'searchV2' in response_data['data']:
            search_results = response_data['data']['searchV2']
            
            # Count different result types
            albums_count = len(search_results.get('albumsV2', {}).get('items', []))
            tracks_count = len(search_results.get('tracksV2', {}).get('items', []))
            artists_count = len(search_results.get('artists', {}).get('items', []))
            
            print(f"📊 Search Results Summary:")
            print(f"   Albums: {albums_count}")
            print(f"   Tracks: {tracks_count}")
            print(f"   Artists: {artists_count}")
            
            # Check if Paradisio appears in artist results
            if 'artists' in search_results and 'items' in search_results['artists']:
                for artist in search_results['artists']['items'][:3]:
                    if 'data' in artist and 'profile' in artist['data']:
                        name = artist['data']['profile'].get('name', 'Unknown')
                        verified = artist['data']['profile'].get('verified', False)
                        print(f"   🎤 Artist found: {name} {'✓' if verified else ''}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def show_raw_structure_sample():
    """Show a sample of the raw JSON structure for debugging."""
    print("\n📁 Raw Structure Sample")
    print("-" * 40)
    
    try:
        with open('../utilities/example-response.json', 'r', encoding='utf-8') as f:
            response_data = json.load(f)
        
        # Show the top-level structure
        print("🔍 Top-level keys:")
        for key in response_data.keys():
            print(f"   - {key}")
        
        if 'data' in response_data:
            print("\n🔍 data keys:")
            for key in response_data['data'].keys():
                print(f"   - {key}")
            
            if 'searchV2' in response_data['data']:
                print("\n🔍 searchV2 keys:")
                for key in response_data['data']['searchV2'].keys():
                    print(f"   - {key}")
                
                # Show structure of first track item
                tracks = response_data['data']['searchV2'].get('tracksV2', {}).get('items', [])
                if tracks and tracks[0].get('item', {}).get('data'):
                    track_data = tracks[0]['item']['data']
                    print("\n🔍 First track data keys:")
                    for key in sorted(track_data.keys()):
                        value_type = type(track_data[key]).__name__
                        if isinstance(track_data[key], dict):
                            sub_keys = list(track_data[key].keys())[:3]
                            print(f"   - {key} ({value_type}): {sub_keys}...")
                        elif isinstance(track_data[key], list):
                            list_len = len(track_data[key])
                            print(f"   - {key} ({value_type}): [{list_len} items]")
                        else:
                            value_str = str(track_data[key])[:50]
                            print(f"   - {key} ({value_type}): {value_str}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🧪 Spotify Response Parsing Test")
    print("=" * 50)
    
    # Change to the correct directory
    os.chdir(os.path.dirname(__file__))
    
    try:
        test_response_parsing()
        test_search_term_extraction()
        show_raw_structure_sample()
        
        print(f"\n✅ Testing completed! Check the generated files:")
        print(f"   - test_tracks.txt")
        print(f"   - test_tracks.csv")
        
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()