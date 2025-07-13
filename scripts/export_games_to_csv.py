#!/usr/bin/env python3
"""
Export all YAML files from the games directory to a CSV file.

This script reads all YAML files in the games/ directory and exports them to a CSV file
with all game data flattened into columns.
"""

import csv
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml


def flatten_list(items: List[Any]) -> str:
    """Convert a list to a semicolon-separated string."""
    if not items:
        return ""
    return "; ".join(str(item) for item in items)


def flatten_dict(d: Dict[str, Any]) -> str:
    """Convert a dictionary to a semicolon-separated key=value string."""
    if not d:
        return ""
    return "; ".join(f"{k}={v}" for k, v in d.items())


def extract_video_info(video_data: Dict[str, Any]) -> Dict[str, str]:
    """Extract video information into separate fields."""
    result = {}
    if not video_data:
        return result
    
    for platform in ['youtube', 'vimeo', 'moddb', 'indiedb']:
        if platform in video_data:
            result[f'video_{platform}'] = str(video_data[platform])
        else:
            result[f'video_{platform}'] = ""
    
    return result


def process_game_data(game: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single game entry and flatten it for CSV export."""
    processed = {}
    
    # Basic fields
    processed['name'] = game.get('name', '')
    processed['type'] = game.get('type', '')
    processed['status'] = game.get('status', '')
    processed['development'] = game.get('development', '')
    processed['content'] = game.get('content', '')
    processed['repo'] = game.get('repo', '')
    processed['url'] = game.get('url', '')
    processed['feed'] = game.get('feed', '')
    processed['info'] = game.get('info', '')
    processed['added'] = game.get('added', '')
    processed['updated'] = game.get('updated', '')
    
    # List fields
    processed['originals'] = flatten_list(game.get('originals', []))
    processed['langs'] = flatten_list(game.get('langs', []))
    processed['frameworks'] = flatten_list(game.get('frameworks', []))
    processed['licenses'] = flatten_list(game.get('licenses', []))
    processed['images'] = flatten_list(game.get('images', []))
    processed['multiplayer'] = flatten_list(game.get('multiplayer', []))
    
    # Video information
    video_info = extract_video_info(game.get('video', {}))
    processed.update(video_info)
    
    return processed


def get_all_field_names(games_data: List[Dict[str, Any]]) -> List[str]:
    """Get all possible field names from the games data."""
    field_names = set()
    
    for game in games_data:
        processed = process_game_data(game)
        field_names.update(processed.keys())
    
    # Sort fields in a logical order
    ordered_fields = [
        'name', 'type', 'status', 'development', 'content',
        'originals', 'repo', 'url', 'feed', 'info',
        'langs', 'frameworks', 'licenses', 'multiplayer',
        'images', 'video_youtube', 'video_vimeo', 'video_moddb', 'video_indiedb',
        'added', 'updated'
    ]
    
    # Add any additional fields that weren't in the ordered list
    additional_fields = sorted(field_names - set(ordered_fields))
    return ordered_fields + additional_fields


def load_games_from_yaml_files(games_dir: Path) -> List[Dict[str, Any]]:
    """Load all games from YAML files in the games directory."""
    all_games = []
    
    # Get all YAML files in the games directory
    yaml_files = sorted(games_dir.glob("*.yaml"))
    
    for yaml_file in yaml_files:
        print(f"Processing {yaml_file.name}...")
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                games = yaml.safe_load(f)
                if games:
                    all_games.extend(games)
        except Exception as e:
            print(f"Error processing {yaml_file.name}: {e}")
            continue
    
    return all_games


def export_to_csv(games_data: List[Dict[str, Any]], output_file: Path):
    """Export games data to CSV file."""
    if not games_data:
        print("No games data to export.")
        return
    
    # Get all field names
    field_names = get_all_field_names(games_data)
    
    # Process all games
    processed_games = [process_game_data(game) for game in games_data]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(processed_games)
    
    print(f"Exported {len(processed_games)} games to {output_file}")
    print(f"Fields: {', '.join(field_names)}")


def main():
    """Main function."""
    # Get the project root directory (parent of scripts/)
    project_root = Path(__file__).parent.parent
    games_dir = project_root / "games"
    output_file = project_root / "games_export.csv"
    
    # Check if games directory exists
    if not games_dir.exists():
        print(f"Games directory not found: {games_dir}")
        sys.exit(1)
    
    # Load all games from YAML files
    print("Loading games from YAML files...")
    games_data = load_games_from_yaml_files(games_dir)
    
    if not games_data:
        print("No games found in YAML files.")
        sys.exit(1)
    
    print(f"Loaded {len(games_data)} games from YAML files.")
    
    # Export to CSV
    print("Exporting to CSV...")
    export_to_csv(games_data, output_file)
    
    print(f"Export complete! CSV file saved to: {output_file}")


if __name__ == "__main__":
    main() 