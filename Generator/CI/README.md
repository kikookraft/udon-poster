# CI Scripts for GitHub Actions

This folder contains the scripts used by the GitHub Actions workflow to generate and deploy atlases.

## Files

### `generate_atlas_ci.py`
Main script to generate atlases in CI/CD context.

**Commands:**
- `python generate_atlas_ci.py generate --input ../images --output output_atlases`
  - Generates atlases from source images (images/ folder at repository root)
- `python generate_atlas_ci.py static --output output_atlases --static-output output_static`
  - Generates static version for GitHub Pages

### `create_index.py`
Script to create home page and empty atlas.

**Commands:**
- `python create_index.py create-index --output output_static`
  - Creates index.html page for GitHub Pages
- `python create_index.py empty-atlas --output output_static`
  - Creates empty atlas (fallback when no images are found)

### `check_images.sh`
Bash script to check for source images.

**Usage:**
```bash
./check_images.sh
```

Returns:
- `images_exist=true` if images are found
- `images_exist=false` otherwise

### `ci_utils.py`
Utility functions for CI/CD.

**Functions:**
- `check_images_exist(images_folder)`: Checks for images presence
- `display_deployment_info(deployment_url)`: Displays deployment info

## Usage in GitHub Actions

These scripts are used by the `.github/workflows/generate-atlas.yml` workflow.

The workflow:
1. Checks for images with `check_images.sh`
2. Generates atlases with `generate_atlas_ci.py generate`
3. Creates static version with `generate_atlas_ci.py static`
4. Creates index.html with `create_index.py create-index`
5. Deploys to GitHub Pages

## Folder Structure

```
/                                # Repository root
├── images/                      # Source images folder
│   └── README.md
├── Generator/
│   ├── CI/                      # CI scripts (this folder)
│   │   ├── generate_atlas_ci.py
│   │   ├── create_index.py
│   │   ├── check_images.sh
│   │   ├── ci_utils.py
│   │   └── README.md
│   ├── generate_posters.py      # Main atlas generator
│   ├── generate_static.py       # Static version generator
│   └── requirements.txt         # Python dependencies
└── .github/
    └── workflows/
        └── generate-atlas.yml   # GitHub Actions workflow
```
