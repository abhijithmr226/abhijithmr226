"""
Flask Backend for Rubik's Cube Solver
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import CubeSolver
from scanner import ColorScanner

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route('/')
def index():
    """
    Root endpoint
    """
    return jsonify({
        'message': 'Rubik\'s Cube Solver API',
        'version': '1.0.0',
        'endpoints': {
            '/api/solve': 'POST - Solve a Rubik\'s cube',
            '/api/detect-color': 'POST - Detect color from RGB values',
            '/api/process-image': 'POST - Process camera image',
            '/api/test': 'GET - Test the solver with a scrambled cube'
        }
    })

@app.route('/api/solve', methods=['POST'])
def solve_cube():
    """
    Solve a Rubik's cube
    
    Expected JSON:
    {
        "cube": "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'cube' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing cube data. Please provide a "cube" field with 54-character string.'
            }), 400
        
        cube_string = data['cube']
        
        # Solve the cube
        result = CubeSolver.solve(cube_string)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/detect-color', methods=['POST'])
def detect_color():
    """
    Detect Rubik's cube color from RGB values
    
    Expected JSON:
    {
        "r": 255,
        "g": 0,
        "b": 0
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'r' not in data or 'g' not in data or 'b' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing RGB values. Please provide r, g, b fields.'
            }), 400
        
        r = int(data['r'])
        g = int(data['g'])
        b = int(data['b'])
        
        # Detect color
        color_code = ColorScanner.detect_color_from_rgb(r, g, b)
        color_name = ColorScanner.COLOR_RANGES[color_code]['name']
        
        return jsonify({
            'success': True,
            'color_code': color_code,
            'color_name': color_name
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Color detection error: {str(e)}'
        }), 500

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """
    Process camera image for color detection
    
    Expected JSON:
    {
        "image": "base64_encoded_image_data"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing image data'
            }), 400
        
        image_data = data['image']
        
        # Process image
        result = ColorScanner.process_image_data(image_data)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Image processing error: {str(e)}'
        }), 500

@app.route('/api/detect-colors-grid', methods=['POST'])
def detect_colors_grid():
    """
    Detect colors from a grid of RGB values
    
    Expected JSON:
    {
        "colors": [[r, g, b], [r, g, b], ...]  // 54 RGB values
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'colors' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing colors data'
            }), 400
        
        colors_rgb = data['colors']
        
        if len(colors_rgb) != 54:
            return jsonify({
                'success': False,
                'error': f'Expected 54 colors, got {len(colors_rgb)}'
            }), 400
        
        # Detect colors
        cube_string = ColorScanner.detect_colors_from_grid(colors_rgb)
        
        return jsonify({
            'success': True,
            'cube_string': cube_string
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Grid detection error: {str(e)}'
        }), 500

@app.route('/api/test', methods=['GET'])
def test_solver():
    """
    Test the solver with a known scrambled cube
    """
    try:
        # A scrambled cube state (solvable)
        scrambled_cube = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"
        
        result = CubeSolver.solve(scrambled_cube)
        
        return jsonify({
            'test': 'Solver test',
            'input': scrambled_cube,
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🧩 Rubik's Cube Solver API Starting...")
    print("📡 Server running on http://localhost:5000")
    print("🔗 API Endpoints:")
    print("   - POST /api/solve")
    print("   - POST /api/detect-color")
    print("   - POST /api/process-image")
    print("   - POST /api/detect-colors-grid")
    print("   - GET  /api/test")
    app.run(debug=True, host='0.0.0.0', port=5000)
