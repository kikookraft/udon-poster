@echo off
echo Starting Atlas API server...
echo.
echo Available routes:
echo - GET /atlas.json              : Complete JSON data
echo - GET /atlas/{index}.png       : Atlas image by index
echo.
echo Server started on http://localhost:8000
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
php -S localhost:8000 api.php
