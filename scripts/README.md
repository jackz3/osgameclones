# Scripts

This directory contains utility scripts for the OSGC project.

## export_games_to_csv.py

Exports all YAML files from the `games/` directory to a CSV file.

### Usage

```bash
python3 scripts/export_games_to_csv.py
```

### Output

The script creates a `games_export.csv` file in the project root with the following columns:

- `name` - Game name
- `type` - Game type (remake, clone, official, similar, tool)
- `status` - Playability status (playable, semi-playable, unplayable, N/A)
- `development` - Development status (complete, very active, active, sporadic, halted)
- `content` - Content type (commercial, free, open, swappable)
- `originals` - Original games this clones (semicolon-separated)
- `repo` - Source code repository URL
- `url` - Game's main website URL
- `feed` - RSS/Atom feed URL
- `info` - Additional information
- `langs` - Programming languages (semicolon-separated)
- `frameworks` - Frameworks/engines used (semicolon-separated)
- `licenses` - License information (semicolon-separated)
- `multiplayer` - Multiplayer features (semicolon-separated)
- `images` - Image URLs (semicolon-separated)
- `video_youtube` - YouTube video ID
- `video_vimeo` - Vimeo video ID
- `video_moddb` - ModDB video ID
- `video_indiedb` - IndieDB video ID
- `added` - Date when game was first added
- `updated` - Date when game was last updated

### Features

- Handles all YAML files in the `games/` directory
- Flattens nested data structures for CSV format
- Separates video information by platform
- Converts lists to semicolon-separated strings
- Provides progress feedback during processing
- Handles missing fields gracefully

### Requirements

- Python 3.6+
- PyYAML library (included in project dependencies) 