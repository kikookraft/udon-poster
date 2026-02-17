# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-02-17

### Added
- Example scene (`Assets/Example.unity`) with sample poster setup and configurations
- Fast load feature: when `fastload: true` is set in atlas metadata, loads only the first low-resolution atlas, then skips directly to scale ×1 for faster initial display
- Poster grouping system with `key` field
  - Each poster can be assigned a `key` to define its group
  - Images with matching `key` in manifest are assigned to corresponding poster groups
  - Images with null/empty `key` are assigned to default group (posters with null/empty `key`)
- Smart image assignment logic
  - Images are assigned to the first available poster in their group
  - Multiple posters can share the same group key
  - Images without matching poster group are automatically ignored
  - Excess images (more images than posters in a group) are automatically ignored
- New CI/CD Python scripts in `Generator/CI/` folder:
  - `generate_atlas_ci.py`: Unified script for CI/CD atlas generation and static deployment
  - `ci_utils.py`: Utilities for CI/CD operations (image detection, deployment info)
- Progress callback system for atlas generation with visual progress bars
- GitHub Actions output support (groups, summaries, notices, outputs)
- Configuration support from manifest.json for atlas generation:
  - `max_atlas_size`: Maximum atlas texture size
  - `padding`: Padding between images in atlas
  - `max_image_size`: Maximum individual image size
- New `Public/` folder with default web assets:
  - `index.html`: Interactive HTML viewer
  - `app.js`: JavaScript application logic
  - `styles.css`: Styling
  - `commit.svg`: GitHub commit icon

### Changed
- **BREAKING**: GitHub Actions workflow refactored with reusable `workflow_call` support
  - New inputs: `input`, `pages`, `summary`, `archive`, `public`
  - New outputs: `page-url`, `num-atlases`, `num-images`
  - Separate jobs: `generate`, `archive`, `pages`, `summary`
- Refactored `PosterManager.OnStringLoadSuccess()` to use new group-based assignment
- Added `AssignImagesToPostersByKey()` method for group-based image distribution
- GitHub Actions workflow now uses separate checkouts for generator and repository
- Atlas generation now supports progress callbacks for better visibility
- CI/CD metadata injection enhanced with more GitHub context:
  - Workflow name and run number
  - GitHub actor (user who triggered the workflow)
  - Full commit and repository URLs
- Public assets handling improved:
  - Default assets from generator's `Public/` folder
  - Custom override support via `public` input parameter
- Workflow summary now consolidated in single step with statistics table

### Fixed
- Input folder path handling in GitHub Actions (supports custom paths via `input` parameter)
- Asset copying logic with proper fallback to defaults
- Manifest.json parameter extraction for atlas generation configuration

## [1.0.2] - 2026-02-16

### Added
- Dynamic HTML viewer (index.html) that fetches and displays atlas.json data
  - Responsive gallery with image cards
  - Real-time statistics display
  - API endpoints documentation
  - Modern gradient UI with backdrop blur effects
- GitHub Pages deployment workflow integration
  - Automatic atlas generation from source images
  - Static version generation for deployment
  - CI/CD metadata injection (commit SHA, workflow info, repository links)
- SHA256 hash generation for cache optimization
  - Image file hashing for integrity verification
  - Atlas file hashing for cache-busting
- Version tracking system (version: 1) in manifest and atlas files
- Missing file detection with `_comment` error annotations
- Command-line argument support (argparse) for all Python scripts
  - make_metadata.py
  - generate_posters.py
  - generate_static.py

### Changed
- Converting package to use template created with `nappollen.packager`
- **BREAKING**: Renamed `metadata.json` to `manifest.json`
- **BREAKING**: New manifest.json structure:
  - `version`: Version number for format compatibility
  - `images`: Image metadata (title, url, sha)
  - `metadata`: Custom metadata object
- **BREAKING**: Changed deployment branch from `images` to `public`
- New repository structure:
  - `public/images/`: Source images and manifest.json
  - `public/public/`: Static assets (index.html, etc.)
- Atlas.json now includes:
  - `base_url`: GitHub Pages base URL
  - `metadata.ci`: CI/CD information (commit, workflow, repository)
  - SHA hashes for all images and atlases
- Image insertion order is now preserved (no automatic sorting)
- Workflow improvements:
  - Separate checkouts for main and public branches
  - Automatic asset copying from public/public/
  - Enhanced error detection and reporting

### Fixed
- Workflow path filtering for proper triggering
- Python script imports refactored for better modularity

### Technical Details
- All Python scripts now support both CLI and module import usage
- Compressed atlas data includes custom metadata passthrough
- GitHub Actions environment variables integration
- Automatic migration support for legacy manifest structure

## [1.0.1] - 2025-08-05

### Added
- Add static support for github pages (for trust URLs)
- Auto-detection of dirty state in the poster manager

### Changed
- The paths has changed with extensions of requests (.json, .png).
- Changed interface for poster manager to use a more consistent.

## [1.0.0] - 2025-08-05

### Added
- Dynamic poster display system for VRChat worlds using Udon Sharp
- Texture atlas support for efficient image management
- Web API integration for remote content loading
- Automated content management tools
- Python scripts for poster generation and atlas creation
- PHP API for serving poster data
- Unity Editor integration with custom UI
- Poster animation system (Display, Loading, Error states)
- Material and shader support for poster rendering
- Comprehensive documentation and setup guides

### Features
- **PosterManager**: Core system for managing multiple poster displays
- **Poster Component**: Individual poster display with state management
- **Atlas Generation**: Python tools for creating optimized texture atlases
- **Web API**: PHP backend for serving poster metadata and images
- **Editor Tools**: Custom Unity Editor interface for easy setup
- **Animation System**: Smooth transitions between poster states
- **VRChat Integration**: Full compatibility with VRC SDK3 and Udon Sharp

### Technical Details
- Unity 2022.3+ compatibility
- VRChat Worlds SDK 3.8.2+ support
- TextMeshPro integration for UI elements
- Modular architecture for easy customization
- Performance optimized for VRChat world limits

### Documentation
- Complete setup and installation guide
- API documentation for web integration
- Examples and best practices
- Troubleshooting guide

## [Unreleased]

### Planned
Nothing yet, but future updates will focus on:
- User feedback and feature requests
- Performance enhancements
- Compatibility with future VRChat SDK updates

