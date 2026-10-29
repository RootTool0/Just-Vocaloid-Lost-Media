import os
from pathlib import Path
import urllib.parse

TARGET_DIR = "."

def convert_path_to_github_url(artist: str, song: str, filename: str) -> str:
    base_url = "https://github.com/RootTool0/Just-Vocaloid-Lost-Media/raw/refs/heads/main/"
    full_path = Path(artist) / song / filename
    
    return base_url + urllib.parse.quote(full_path.as_posix())

def TEMPLATE_SONG_README(artist, song, files):
    table_rows = []
    file_list = [f for f in files if f != "README.md"]
    
    for index, filename in enumerate(file_list, start=1):
        table_rows.append(f"| {index} | [{filename}]({convert_path_to_github_url(artist, song, filename)}) |")
    
    table_content = "\n".join(table_rows)
    
    cover_file = next((f for f in files if Path(f).stem.lower() == "cover"), None)
    print(files)
    
    main_content = []
    
    main_content.append(f"# {artist} / {song}\n")
    
    main_content.append(f'<img src="{cover_file}" alt="Cover Image" height="300">\n')
    
    main_content.append("| № | File |")
    main_content.append("| :--- | :--- |")
    
    main_content.append("\n".join(table_rows))
    
    main_content.append("\n###### [<- Back](../../README.md)\n")
    
    return "\n".join(main_content)

def TEMPLATE_MAIN_README(archive_data):
    grouped_data = {}
    for item in archive_data:
        artist = item['artist']
        if artist not in grouped_data:
            grouped_data[artist] = []
        grouped_data[artist].append(item)
    
    main_content = []
    main_content.append("# [Generated] Just-Vocaloid-Lost-Media\n")
    
    for artist, songs in grouped_data.items():
        main_content.append(f"## {artist}\n")
        main_content.append("| № | Song | Cover |")
        main_content.append("| :--- | :--- | :--: |")
        
        table_rows = []
        for index, item in enumerate(songs, start=1):
            rel_path = item['path'].replace(os.sep, '/')
            cover_file = next((f for f in os.listdir(item['path']) if Path(f).stem.lower() == "cover"), None)
            cover_cell = f'<img src="{rel_path}/{cover_file}" width="160" height="90" alt="Cover">' if cover_file else "**- no image -**"
            
            table_rows.append(f"| {index} | [**{item['song']}**]({rel_path}/README.md) | {cover_cell} |")
        
        main_content.append("\n".join(table_rows))
        main_content.append("\n")
    
    return "\n".join(main_content)

def generate_archive_documentation(root_dir):
    root_path = Path(root_dir)
    archive_db = []

    for artist_dir in root_path.iterdir():
        if not artist_dir.is_dir() or artist_dir.name.startswith('.'):
            continue
        
        for song_dir in artist_dir.iterdir():
            if not song_dir.is_dir() or song_dir.name.startswith('.'):
                continue
                
            artist_name = artist_dir.name
            song_name = song_dir.name
            
            all_files = [f.name for f in song_dir.iterdir() if f.is_file()]
            
            song_readme_content = TEMPLATE_SONG_README(artist_name, song_name, all_files)
            song_readme_path = song_dir / "README.md"
            song_readme_path.write_text(song_readme_content, encoding="utf-8")
            
            relative_path = song_dir.relative_to(root_path)
            
            archive_db.append({
                'artist': artist_name,
                'song': song_name,
                'path': str(relative_path),
                'files_count': len(all_files)
            })
            
            print(f"Processing: {artist_name} -> {song_name}")
    
    main_readme_content = TEMPLATE_MAIN_README(archive_db)
    main_readme_path = root_path / "GeneratedREADME.md"
    main_readme_path.write_text(main_readme_content, encoding="utf-8")
    
    print(f"\nReady! Main README.md created: {main_readme_path.absolute()}")

generate_archive_documentation(TARGET_DIR)
