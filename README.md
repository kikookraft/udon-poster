# Nappollen Udon Poster

nappollen.udon-poster

![Udon Posters Screenshot](./preview.png)

## Description

A package for managing dynamic poster displays in VRChat worlds using Udon Sharp. This system allows you to display and update posters dynamically by loading images from external sources, with support for texture atlases and automated content management.

## Requirements

- Unity 2022.3 or later
- VRChat SDK3 (Udon)
- UdonSharp

### For the server-side features:
- [PHP 8.4](https://www.php.net/downloads.php?version=8.4) or later
- [Python 3.13](https://www.python.org/downloads/release/python-3130/) or later

## Installation

### Via VRChat Package Manager (VPM)

Check the VPM repository for the latest version:  
[https://nappollen.github.io/vpm/](https://nappollen.github.io/vpm/)

Add the package using [VRChat Creator Companion](https://vcc.docs.vrchat.com/):  
[https://nappollen.github.io/vpm.json](https://nappollen.github.io/vpm.json)

1. Open VRChat Creator Companion
2. Go to `Settings > Packages`
3. Add the repository URL above
4. Install "Nappollen Udon Poster" from the available packages

### Via Unity Package Manager (UPM)

1. Open the Package Manager window
2. Click the "+" button and select "Add package from git URL..."
3. Enter: `https://github.com/nappollen/udon-poster.git`

### Via manifest.json

Add the following line to your `Packages/manifest.json`:

```json
"nappollen.udon-poster": "https://github.com/nappollen/udon-poster.git"
```


## Setup Guide

### 1. Basic Setup

1. **Add PosterManager to Scene**:  
> The PosterManager is responsible for managing multiple poster displays and handling the loading of metadata and atlases. It should be added to your scene to function properly.
   - Drag `Assets/Prefab/Manager.prefab` into your scene
   - Configure the `metaUrl` to point to your metadata JSON
   - Set up `atlasUrls` array with your texture atlas URLs

2. **Configure Individual Posters**:  
> A Poster component represents an individual poster display in your scene. You can have multiple Poster instances, and they will be managed by the PosterManager. The order of posters in the array should match the metadata indices to ensure correct mapping.
   - Add `Assets/Prefab/Poster.prefab` instances to your scene
   - Assign them to the `posters` array in PosterManager
   - Optionally: Set up click interactions and animations

### 2. Server Setup (Optional)

If you want to use the dynamic generation features:

1. **Go to the `Generator/` folder**:
   - This contains Python scripts for generating metadata and atlases.

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Input Images**:
   - Place your images in `Generator/input_images/`
   - Run `make_metadata.py` to generate metadata
   - You can add additional properties like titles and redirect URLs in the metadata JSON. If you change the order of metadata, it changes the index of the posters, so be careful with that.
   - Run `generate_posters.py` to create atlases. If you have many images, it is possible it may take a long time to generate the atlases, so be patient.

4. **Deploy Web Server**:
    - Production with own PHP server:
        - Copy the `api.php` file to your web server
        - Ensure PHP is available for the API

    - Production with static hosting:
        - Use the `generate_static.py` script to generate static files that can be hosted on platforms like GitHub Pages. This will create a `static_output/` folder with the necessary files. You can then upload this folder to your hosting platform and update the URLs in your Unity setup accordingly.
        
    - Local Testing:
        - Use the `start_server.bat` or `start_server.sh` script to run a local server for testing purposes. This will serve the metadata and atlas images from your local machine. You need to run the script in the folder where your `output_atlases` are located.

    - Update URLs in your Unity setup


## License

See [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG](CHANGELOG.md) file for details.

---

<sub>This package was created with [Nappollen's Packager](https://github.com/nappollen/packager)</sub>

