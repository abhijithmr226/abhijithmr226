"""
Color detection and scanning utilities for Rubik's Cube
"""
import cv2
import numpy as np
from PIL import Image
import io
import base64

class ColorScanner:
    """
    Handles color detection from camera images
    """
    
    # Define color ranges in HSV for Rubik's cube colors
    COLOR_RANGES = {
        'U': {  # White (Up)
            'name': 'White',
            'lower': np.array([0, 0, 200]),
            'upper': np.array([180, 30, 255])
        },
        'R': {  # Red (Right)
            'name': 'Red',
            'lower': np.array([0, 100, 100]),
            'upper': np.array([10, 255, 255])
        },
        'F': {  # Green (Front)
            'name': 'Green',
            'lower': np.array([40, 50, 50]),
            'upper': np.array([80, 255, 255])
        },
        'D': {  # Yellow (Down)
            'name': 'Yellow',
            'lower': np.array([20, 100, 100]),
            'upper': np.array([30, 255, 255])
        },
        'L': {  # Orange (Left)
            'name': 'Orange',
            'lower': np.array([10, 100, 100]),
            'upper': np.array([20, 255, 255])
        },
        'B': {  # Blue (Back)
            'name': 'Blue',
            'lower': np.array([100, 50, 50]),
            'upper': np.array([130, 255, 255])
        }
    }
    
    @staticmethod
    def detect_color_from_rgb(r, g, b):
        """
        Detect Rubik's cube color from RGB values
        
        Args:
            r, g, b: RGB color values (0-255)
            
        Returns:
            str: Color code (U, R, F, D, L, B)
        """
        # Convert RGB to HSV
        rgb_pixel = np.uint8([[[b, g, r]]])  # OpenCV uses BGR
        hsv_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2HSV)[0][0]
        
        # Find the best matching color
        best_match = None
        min_distance = float('inf')
        
        for color_code, color_info in ColorScanner.COLOR_RANGES.items():
            lower = color_info['lower']
            upper = color_info['upper']
            
            # Check if HSV values are within range
            if (lower[0] <= hsv_pixel[0] <= upper[0] and
                lower[1] <= hsv_pixel[1] <= upper[1] and
                lower[2] <= hsv_pixel[2] <= upper[2]):
                
                # Calculate distance to center of range
                center = (lower + upper) / 2
                distance = np.linalg.norm(hsv_pixel - center)
                
                if distance < min_distance:
                    min_distance = distance
                    best_match = color_code
        
        # If no match found, use simple RGB heuristics
        if best_match is None:
            best_match = ColorScanner._simple_color_detection(r, g, b)
        
        return best_match
    
    @staticmethod
    def _simple_color_detection(r, g, b):
        """
        Simple color detection fallback using RGB values
        """
        # Normalize values
        total = r + g + b
        if total == 0:
            return 'U'  # Default to white for black
        
        r_norm = r / total
        g_norm = g / total
        b_norm = b / total
        
        # White: high values across all channels
        if r > 200 and g > 200 and b > 200:
            return 'U'
        
        # Yellow: high red and green, low blue
        if r > 180 and g > 180 and b < 100:
            return 'D'
        
        # Red: high red, low others
        if r_norm > 0.45 and r > g and r > b:
            return 'R'
        
        # Orange: high red and medium green
        if r > 180 and 100 < g < 180 and b < 100:
            return 'L'
        
        # Green: high green
        if g_norm > 0.4 and g > r and g > b:
            return 'F'
        
        # Blue: high blue
        if b_norm > 0.4 and b > r and b > g:
            return 'B'
        
        # Default to white
        return 'U'
    
    @staticmethod
    def process_image_data(image_data):
        """
        Process base64 image data and detect colors
        
        Args:
            image_data: Base64 encoded image string
            
        Returns:
            dict: Detected colors and processed image
        """
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img_array
            
            return {
                'success': True,
                'message': 'Image processed successfully',
                'dimensions': {
                    'width': img_array.shape[1],
                    'height': img_array.shape[0]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Image processing error: {str(e)}"
            }
    
    @staticmethod
    def detect_colors_from_grid(colors_rgb):
        """
        Detect cube colors from a grid of RGB values
        
        Args:
            colors_rgb: List of RGB tuples [(r,g,b), ...]
            
        Returns:
            str: Cube string representation
        """
        cube_string = ""
        
        for rgb in colors_rgb:
            r, g, b = rgb
            color_code = ColorScanner.detect_color_from_rgb(r, g, b)
            cube_string += color_code
        
        return cube_string
