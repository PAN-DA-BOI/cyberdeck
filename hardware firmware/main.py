import board
import keypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

ROW_PINS = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
COL_PINS = (
    board.GP5, board.GP6, board.GP7, board.GP8, board.GP9,
    board.GP10, board.GP11, board.GP12, board.GP13, board.GP14,
    board.GP15, board.GP16, board.GP17, board.GP18
)

KEYCODES = (
    Keycode.GRAVE_ACCENT, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE,
    Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO,
    Keycode.MINUS, Keycode.EQUALS, Keycode.BACKSPACE,
    Keycode.TAB, Keycode.Q, Keycode.W, Keycode.E, Keycode.R,
    Keycode.T, Keycode.Y, Keycode.U, Keycode.I, Keycode.O,
    Keycode.P, Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.BACKSLASH,
    Keycode.CAPS_LOCK, Keycode.A, Keycode.S, Keycode.D, Keycode.F,
    Keycode.G, Keycode.H, Keycode.J, Keycode.K, Keycode.L,
    Keycode.SEMICOLON, Keycode.QUOTE, Keycode.ENTER, Keycode.ENTER,
    Keycode.LEFT_SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V,
    Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD,
    Keycode.FORWARD_SLASH, Keycode.RIGHT_SHIFT, Keycode.UP_ARROW, Keycode.UP_ARROW,
    Keycode.RIGHT_ARROW, Keycode.DOWN_ARROW, Keycode.LEFT_ARROW,
    Keycode.RIGHT_CONTROL, Keycode.F, Keycode.F, Keycode.SPACE,
    Keycode.F, Keycode.F, Keycode.F, Keycode.BACKSLASH, Keycode.LEFT_ALT,
    Keycode.PAUSE, Keycode.LEFT_CONTROL,
)

keys = keypad.KeyMatrix(ROW_PINS, COL_PINS)

SPECIAL_ROW_PINS = (board.GP26, board.GP22)
SPECIAL_COL_PINS = (board.GP20, board.GP21)

SPECIAL_KEYCODES = (
    Keycode.F13, Keycode.F14,  
    Keycode.F15, Keycode.F16,
)

special_keys = keypad.KeyMatrix(SPECIAL_ROW_PINS, SPECIAL_COL_PINS)

kbd = Keyboard(usb_hid.devices)

while True:
    event = keys.events.get()
    if event:
        key_number = event.key_number
        if event.pressed:
            kbd.press(KEYCODES[key_number])
        if event.released:
            kbd.release(KEYCODES[key_number])

    special_event = special_keys.events.get()
    if special_event:
        special_key_number = special_event.key_number
        if special_event.pressed:
            kbd.press(SPECIAL_KEYCODES[special_key_number])
        if special_event.released:
            kbd.release(SPECIAL_KEYCODES[special_key_number])
