"""
Utilities for CI/CD
"""

import os
import sys


def check_images_exist(images_folder: str = "images") -> bool:
    """
    Checks if images folder exists and contains files
    
    Args:
        images_folder: Path to images folder
        
    Returns:
        True if images exist, False otherwise
    """
    if os.path.isdir(images_folder):
        files = os.listdir(images_folder)
        if files:
            print(f"✅ Images folder found with {len(files)} files")
            return True
    
    print("⚠️ No images found in 'images/' folder")
    return False


def display_deployment_info(deployment_url: str):
    """
    Displays deployment information
    
    Args:
        deployment_url: GitHub Pages deployment URL
    """
    print("🎉 Deployment successful!")
    print(f"📍 Base URL: {deployment_url}")
    print(f"📄 Atlas JSON: {deployment_url}atlas.json")
    print("")
    print("Use this URL in your VRChat world!")
