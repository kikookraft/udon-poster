#!/bin/bash

echo "Starting Atlas API server..."
echo ""
echo "Available routes:"
echo "- GET /atlas.json               : Complete JSON data"
echo "- GET /atlas/{index}.png        : Atlas image by index"
echo ""
echo "Server started on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Start PHP server
php -S localhost:8000 api.php