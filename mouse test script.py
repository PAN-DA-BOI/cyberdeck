from machine import Pin, ADC
import time

# Initialize ADC pins for the joystick
joystick_x = ADC(Pin(26))
joystick_y = ADC(Pin(27))

# Function to read and print joystick values
def read_joystick():
    x_value = joystick_x.read_u16()
    y_value = joystick_y.read_u16()

    # Print the joystick values
    print(f"X: {x_value}, Y: {y_value}")

# Main loop
while True:
    read_joystick()
    time.sleep(0.1)  # Delay to reduce the output rate
