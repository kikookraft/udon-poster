#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate a static version of atlases
Copies images with index renaming and generates JSON equivalent to /atlas API
"""

import json
import os
import shutil
from pathlib import Path


def compress_atlas_data(data):
    """
    Compresses JSON data (replaces string keys with indexes)
    Equivalent to PHP compressAtlasData function
    """
    compressed_data = {
        'version': data.get('version', 1),
        'mapping': [],
        'atlases': []
    }
    
    # Add custom metadata if it exists
    if 'metadata' in data and data['metadata']:
        compressed_data['metadata'] = data['metadata']
    
    # Create a mapping from image names to indexes based on metadata order
    image_name_to_index = {}
    image_index = 0

    # Use metadata order to determine indexes
    for image_name, metadata in data['images_metadata'].items():
        image_name_to_index[image_name] = image_index
        compressed_data['mapping'].append(metadata)
        image_index += 1

    # Compress atlases
    for atlas in data['atlases']:
        compressed_atlas = {
            'scale': atlas['scale'],
            'width': atlas['width'],
            'height': atlas['height'],
            'sha': atlas.get('sha', ''),
            'uv': {}
        }

        # Replace string keys with numeric indexes
        for image_name, uv in atlas['uv'].items():
            index = image_name_to_index[image_name]
            compressed_atlas['uv'][str(index)] = uv

        compressed_data['atlases'].append(compressed_atlas)
    
    return compressed_data


def copy_and_rename_images(atlas_folder, output_static_folder, atlas_data):
    """
    Copies atlas images by renaming them with their index
    """
    images_folder = output_static_folder / 'atlas'
    images_folder.mkdir(exist_ok=True)
    
    copied_files = []
    
    for index, atlas in enumerate(atlas_data['atlases']):
        if 'file' in atlas:
            source_file = atlas_folder / atlas['file']
            if source_file.exists():
                # Get original file extension
                extension = source_file.suffix
                # New name with index
                new_filename = f"{index}{extension}"
                destination_file = images_folder / new_filename
                
                # Copy file
                shutil.copy2(source_file, destination_file)
                copied_files.append({
                    'original': atlas['file'],
                    'new': new_filename,
                    'index': index
                })
                print(f"Copied: {atlas['file']} -> {new_filename}")
            else:
                print(f"Warning: File not found: {source_file}")
    
    return copied_files


def generate_static_version(input_path=None, output_path=None, progress_callback=None):
    """
    Main function to generate static version
    
    Args:
        input_path: Input atlases folder (default: 'output_atlases')
        output_path: Output folder (default: 'output_static')
        progress_callback: Progress callback function (step, total, message)
        
    Returns:
        dict: Generation result or None on error
    """
    
    def report_progress(step, total, message):
        """Helper to call callback if it exists"""
        if progress_callback:
            progress_callback(step, total, message)
    report_progress(1, 5, "Initializing static generation")
    
    # Determine input folder
    if not input_path:
        # Use default folder
        script_dir = Path(__file__).parent
        atlas_folder = script_dir / 'output_atlases'
        print(f"Using default folder: {atlas_folder}")
    else:
        atlas_folder = Path(input_path)
    
    # Check input folder exists
    if not atlas_folder.exists():
        print(f"Error: Input folder {atlas_folder} does not exist")
        return None
    
    json_file = atlas_folder / 'manifest.json'
    if not json_file.exists():
        print(f"Error: File {json_file} does not exist")
        print("Make sure the folder contains the manifest.json file")
        return None
    
    # Determine output folder
    if not output_path:
        # Use default folder
        output_static_folder = Path('output_static')
        print(f"Using default output folder: {output_static_folder}")
    else:
        output_static_folder = Path(output_path)
    output_static_folder.mkdir(exist_ok=True)
    print(f"Output folder: {output_static_folder}")
    
    report_progress(2, 5, "Loading atlas manifest")
    
    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            atlas_data = json.load(f)
        print(f"JSON data loaded from: {json_file}")
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    
    report_progress(3, 5, "Compressing JSON data")
    
    # Compress data (as done by PHP API)
    compressed_data = compress_atlas_data(atlas_data)
    
    # Save compressed JSON (equivalent to /atlas response)
    atlas_json_file = output_static_folder / 'atlas.json'
    try:
        with open(atlas_json_file, 'w', encoding='utf-8') as f:
            json.dump(compressed_data, f, indent=2, ensure_ascii=False)
        print(f"Compressed JSON saved: {atlas_json_file}")
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return None
    
    report_progress(4, 5, "Copying and renaming atlas images")
    
    # Copy and rename images
    copied_files = copy_and_rename_images(atlas_folder, output_static_folder, atlas_data)
    
    report_progress(5, 5, "Static generation completed successfully")
    
    print(f"\n✅ Static version generated successfully in: {output_static_folder}")
    print(f"📁 Generated files:")
    print(f"   - atlas.json (equivalent to /atlas API)")
    print(f"   - atlas/ (images renamed by index)")
    print(f"\n📊 Statistics:")
    print(f"   - {len(copied_files)} images copied")
    print(f"   - {len(compressed_data['atlases'])} atlases")
    print(f"   - {len(compressed_data['mapping'])} images in mapping")
    
    return {
        'output_folder': str(output_static_folder),
        'atlas_json': str(atlas_json_file),
        'copied_files': copied_files,
        'compressed_data': compressed_data
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generates a static version of atlases for GitHub Pages')
    parser.add_argument('--input', default=None,
                       help='Input atlases folder (default: output_atlases)')
    parser.add_argument('--output', default=None,
                       help='Output folder (default: output_static)')
    
    args = parser.parse_args()
    generate_static_version(args.input, args.output)
