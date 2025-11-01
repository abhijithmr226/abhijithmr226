"""
Rubik's Cube Solver using Kociemba Algorithm
"""
import kociemba

class CubeSolver:
    """
    Wrapper class for Kociemba solver
    """
    
    @staticmethod
    def validate_cube_string(cube_string):
        """
        Validate the cube string format
        Expected format: 54 characters representing the cube state
        Each face: U (Up/White), R (Right/Red), F (Front/Green), 
                   D (Down/Yellow), L (Left/Orange), B (Back/Blue)
        """
        if len(cube_string) != 54:
            return False, "Cube string must be exactly 54 characters"
        
        # Check if all characters are valid face colors
        valid_chars = set('URFDLB')
        if not all(c in valid_chars for c in cube_string):
            return False, "Invalid characters in cube string. Use only: U, R, F, D, L, B"
        
        # Check if each color appears exactly 9 times
        color_counts = {}
        for char in cube_string:
            color_counts[char] = color_counts.get(char, 0) + 1
        
        for color, count in color_counts.items():
            if count != 9:
                return False, f"Color {color} appears {count} times, expected 9"
        
        return True, "Valid cube string"
    
    @staticmethod
    def solve(cube_string):
        """
        Solve the Rubik's cube using Kociemba algorithm
        
        Args:
            cube_string: 54-character string representing cube state
            
        Returns:
            dict: Solution with moves and status
        """
        try:
            # Validate cube string
            is_valid, message = CubeSolver.validate_cube_string(cube_string)
            if not is_valid:
                return {
                    'success': False,
                    'error': message
                }
            
            # Solve the cube
            solution = kociemba.solve(cube_string)
            
            # Parse solution into individual moves
            moves = solution.split()
            
            return {
                'success': True,
                'solution': solution,
                'moves': moves,
                'move_count': len(moves)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Solver error: {str(e)}"
            }
    
    @staticmethod
    def get_solved_state():
        """
        Return the solved cube state string
        """
        # Each face has 9 stickers of the same color
        return "U" * 9 + "R" * 9 + "F" * 9 + "D" * 9 + "L" * 9 + "B" * 9
