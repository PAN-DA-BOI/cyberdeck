from machine import Pin, ADC
import time

# Initialize ADC pins for the joystick
joystick_x = ADC(Pin(26))
joystick_y = ADC(Pin(27))

# Initialize GPIO pins for the buttons
button1 = Pin(14, Pin.IN, Pin.PULL_UP)
button2 = Pin(15, Pin.IN, Pin.PULL_UP)
button3 = Pin(16, Pin.IN, Pin.PULL_UP)

# Function to read and print joystick values
def read_joystick():
    x_value = joystick_x.read_u16()
    y_value = joystick_y.read_u16()
    print(f"X: {x_value}, Y: {y_value}")

# Function to read and print button states
def read_buttons():
    button1_state = "pressed" if not button1.value() else "not pressed"
    button2_state = "pressed" if not button2.value() else "not pressed"
    button3_state = "pressed" if not button3.value() else "not pressed"
    print(f"Button 1: {button1_state}, Button 2: {button2_state}, Button 3: {button3_state}")

# Main loop
while True:
    read_joystick()
    read_buttons()
    time.sleep(0.1)  # Delay to reduce the output rate
