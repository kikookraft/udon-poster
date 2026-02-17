#!/bin/bash
# Script to check for source images
# Used by GitHub Actions workflow

check_images() {
    if [ -d "images" ] && [ "$(ls -A images 2>/dev/null)" ]; then
        echo "images_exist=true"
        echo "✅ Images folder found with $(ls -1 images | wc -l) files"
        return 0
    else
        echo "images_exist=false"
        echo "⚠️ No images found in 'images/' folder"
        return 1
    fi
}

# Run check
check_images
