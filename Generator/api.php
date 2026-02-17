<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Configuration
$atlas_folder = __DIR__ . '/output_atlases';
$json_file = $atlas_folder . '/atlas_data.json';

// Function to load JSON data
function loadAtlasData($json_file) {
    if (!file_exists($json_file)) {
        http_response_code(404);
        echo json_encode(['error' => 'Atlas data not found']);
        exit;
    }
    
    $json_content = file_get_contents($json_file);
    $data = json_decode($json_content, true);
    
    if ($data === null) {
        http_response_code(500);
        echo json_encode(['error' => 'Invalid JSON data']);
        exit;
    }

    return $data;
}

// Function to compress JSON data (replace string keys with indexes)
function compressAtlasData($data) {
    $compressed_data = [
        'mapping' => [],
        'atlases' => []
    ];
    
    // Create a mapping from image names to indexes based on metadata order
    $image_name_to_index = [];
    $image_index = 0;

    // Use metadata order to determine indexes
    foreach ($data['metadata'] as $image_name => $metadata) {
        $image_name_to_index[$image_name] = $image_index;
        $compressed_data['mapping'][$image_index] = $metadata;
        $image_index++;
    }

    // Compress atlases
    foreach ($data['atlases'] as $atlas) {
        $compressed_atlas = [
            'scale' => $atlas['scale'],
            'width' => $atlas['width'],
            'height' => $atlas['height'],
            'uv' => (object)[] // Force to be an object/dictionary
        ];

        // Replace string keys with numeric indexes
        foreach ($atlas['uv'] as $image_name => $uv) {
            $index = $image_name_to_index[$image_name];
            $compressed_atlas['uv']->$index = $uv;
        }

        $compressed_data['atlases'][] = $compressed_atlas;
    }
    
    return $compressed_data;
}

// Function to get MIME type based on extension
function getMimeType($file_path) {
    $extension = strtolower(pathinfo($file_path, PATHINFO_EXTENSION));
    
    $mime_types = [
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'gif' => 'image/gif',
        'bmp' => 'image/bmp',
        'webp' => 'image/webp',
        'tiff' => 'image/tiff',
        'tif' => 'image/tiff',
        'svg' => 'image/svg+xml'
    ];
    
    return isset($mime_types[$extension]) ? $mime_types[$extension] : 'application/octet-stream';
}

// Function to serve an image
function serveImage($file_path) {
    if (!file_exists($file_path)) {
        http_response_code(404);
        echo json_encode(['error' => 'Image not found']);
        exit;
    }
    
    $mime_type = getMimeType($file_path);
    header('Content-Type: ' . $mime_type);
    header('Content-Length: ' . filesize($file_path));
    header('Cache-Control: public, max-age=86400'); // Cache 1 day
    
    readfile($file_path);
    exit;
}

// Simple router
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);

// Route: GET /atlas - Returns complete compressed JSON file
if ($path === '/atlas.json') {
    $data = loadAtlasData($json_file);
    $compressed_data = compressAtlasData($data);
    echo json_encode($compressed_data, JSON_PRETTY_PRINT);
    exit;
}

// Route: GET /atlas/{index} - Returns the atlas image at the given index
if (preg_match('/^\/atlas\/(\d+).png$/', $path, $matches)) {
    $requested_index = intval($matches[1]);
    $data = loadAtlasData($json_file);
    
    $atlas = $data['atlases'];
    
    if (!isset($atlas[$requested_index])) {
        http_response_code(404);
        echo json_encode(['error' => "Atlas with index $requested_index not found"]);
        exit;
    }
    
    $found_atlas = $atlas[$requested_index];
    
    if ($found_atlas === null) {
        http_response_code(404);
        echo json_encode(['error' => "Atlas containing image with index $requested_index not found"]);
        exit;
    }
    
    // Serve the atlas image
    $image_path = $atlas_folder . '/' . $found_atlas['file'];
    serveImage($image_path);
}

// Default route - API documentation
http_response_code(404);
echo json_encode([
    'error' => 'Route not found',
    'available_routes' => [
        'GET /atlas.json' => 'Returns complete atlas JSON file',
        'GET /atlas/{index}.png' => 'Returns the atlas image at the given index'
    ],
    'examples' => [
        '/atlas.json' => 'Complete JSON data',
        '/atlas/0.png' => 'First atlas (index 0)',
        '/atlas/1.png' => 'Second atlas (index 1)'
    ]
], JSON_PRETTY_PRINT);
?>
