import board
import displayio
import terminalio
import adafruit_ssd1306
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.modules.media_keys import MediaKeys
from adafruit_display_text import label

keyboard = KMKKeyboard()
encoders = EncoderHandler()

# Setup I2C OLED
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address = 0x3C) # 0x3C (hex for 60) is the default I2C address for most SSD1306 OLED displays
WIDTH = 128
HEIGHT = 32
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Create label
comment_text = "Testing!"
comment = label.Label(terminalio.FONT, text = comment_text, color = 0xFFFFFF)

# Add macro extension
macros = Macros()
keyboard.modules.append(macros)
keyboard.modules.append(encoders)
keyboard.modules.append(MediaKeys())

# Define pins
PINS = [board.D7, board.D8, board.D9, board.D10, board.D4]
encoders.pins = ((board.D3, board.D0, board.GND),) # <- COMMA = tuple with 1 encoder

# Specify to kmk that the keyboard has no matrix
keyboard.matrix = KeysScanner(
    pins = PINS,
    value_when_pressed = False, # Trailing comma
)

# Define buttons corresponding to pins
# For keycodes: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
# For macros: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md
keyboard.keymap = [ # 2-D array: [1][5]
    [
        KC.MACRO(Press(KC.LCTRL), Tap(KC.Z), Release(KC.LCTRL)), # CTRL + Z
        KC.MACRO(Press(KC.LCTRL), Press(KC.LSHIFT), Tap(KC.Z), Release(KC.LSHIFT), Release(KC.LCTRL)), # CTRL + Shift + Z
        KC.MACRO(Press(KC.LCTRL), Press(KC.LSHIFT), Tap(KC.C), Release(KC.LSHIFT), Release(KC.LCTRL)), # CTRL + Shift + C
        KC.MACRO(Press(KC.LCTRL), Tap(KC.D), Release(KC.LCTRL)), # CTRL + D
        KC.MACRO(Press(KC.LCTRL), Press(KC.LSHIFT), Tap(KC.D), Release(KC.LSHIFT), Release(KC.LCTRL)), # CTRL + Shift + D
    ]
]

# ((A, B), C)
encoders.map = [((KC.BRIGHTNESS_UP, KC.BRIGHTNESS_DOWN), (Press(KC.LGUI), Tap(KC.F8), Release(KC.LGUI)))] # C: Win + F8

# Add to display group
main_group = displayio.Group()
main_group.append(comment)
display.show(main_group)

# Animation loop (slide from right to left)
while True: # Run forever
    # Adjust 6 for font width (assume ~6 pixels per character)
    # Move left by 1 pixel every time
    # range(start, stop, step)
    for x in range(WIDTH, -len(comment_text)*6, -1): # int x = WIDTH; x > -comment_text.length()*6; x--
        comment.x = x
        comment.y = 10 # Adjust vertical position
        display.show(main_group)
        time.sleep(0.05) # Speed of slide

    # Reset to right again
    time.sleep(0.5)

# Start kmk
if __name__ == '__main__':
    keyboard.go()