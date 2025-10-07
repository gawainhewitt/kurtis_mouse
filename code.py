import time
import board
import usb_hid
from analogio import AnalogIn
from adafruit_hid.mouse import Mouse

# Initialize the mouse
mouse = Mouse(usb_hid.devices)

# Define analog input pins
x_pin = AnalogIn(board.GP26)
y_pin = AnalogIn(board.GP27)

# Calibrated center values from your joystick
CENTER_X = 33300
CENTER_Y = 33400

# Deadzone to prevent drift - smaller number for smaller zone, larger number for bigger zone
DEADZONE = 200

# Sensitivity multiplier (bigger number for faster/ smaller number for slower movement)
SENSITIVITY = 0.0005

print("Joystick Mouse Controller Started!")
print("Device rotated 180° - all directions inverted")
print(f"Center: X={CENTER_X}, Y={CENTER_Y}")
print("Move the joystick to control the mouse\n")

def calculate_movement(value, center):
    """Calculate mouse movement from joystick position"""
    diff = value - center
    
    # Apply deadzone
    if abs(diff) < DEADZONE:
        return 0
    
    # Remove deadzone from calculation
    if diff > 0:
        diff = diff - DEADZONE
    else:
        diff = diff + DEADZONE
    
    # Calculate movement with sensitivity
    movement = int(diff * SENSITIVITY)
    
    # Limit maximum movement per update
    return max(-127, min(127, movement))

while True:
    # Read joystick positions
    x_value = x_pin.value
    y_value = y_pin.value
    
    # Calculate mouse movements (INVERTED for 180° rotation)
    x_move = -calculate_movement(x_value, CENTER_X)  # Invert X
    y_move = -calculate_movement(y_value, CENTER_Y)  # Invert Y
    
    # Move the mouse if there's any movement
    if x_move != 0 or y_move != 0:
        mouse.move(x=x_move, y=y_move)
        print(f"Raw: X={x_value:5d} Y={y_value:5d} | Move: X={x_move:+4d} Y={y_move:+4d}")
    
    time.sleep(0.01)