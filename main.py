# === CHRONO + 2 AFFICHAGES DE 0 A 19 ===

from machine import Pin
import time
import neopixel

#Segments:
# -- A --
#|       |
#F       B
#|       |
# -- G --
#|       |
#E       C
#|       |
# -- D --

# === CONFIGURATION ===
LEDS_PER_SEGMENT = 9
SEGMENTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
SEGMENTS_PER_DIGIT = len(SEGMENTS)
LEDS_PER_DIGIT = SEGMENTS_PER_DIGIT * LEDS_PER_SEGMENT

# Affichage 1 et 2 : 2 chiffres (1 partiel + 1 complet) = 81 LEDs chacun
OFFSET_DISPLAY_1 = 0
OFFSET_DISPLAY_2 = OFFSET_DISPLAY_1 + 81

# Chrono : 5 chiffres complets + 2 LED pour les 2 points => 5*63 + 2 = 317
OFFSET_CHRONO = OFFSET_DISPLAY_2 + 81
CHRONO_DIGITS = 5
COLON_LEDS = [OFFSET_CHRONO + 3 * LEDS_PER_DIGIT, OFFSET_CHRONO + 3 * LEDS_PER_DIGIT + 1]  # après 3e chiffre

TOTAL_LEDS = OFFSET_CHRONO + CHRONO_DIGITS * LEDS_PER_DIGIT + 2
np = neopixel.NeoPixel(Pin(1, Pin.OUT), TOTAL_LEDS)

# === SEGMENT MAPPING ===
def get_segment_mapping(offset):
    segment_map = {}
    for idx, seg in enumerate(SEGMENTS):
        start = offset + idx * LEDS_PER_SEGMENT
        segment_map[seg] = [start + i for i in range(LEDS_PER_SEGMENT)]
    return segment_map

DIGIT_SEGMENTS = {
    0: ['A', 'B', 'C', 'D', 'E', 'F'],
    1: ['B', 'C'],
    2: ['A', 'B', 'G', 'E', 'D'],
    3: ['A', 'B', 'C', 'D', 'G'],
    4: ['F', 'G', 'B', 'C'],
    5: ['A', 'F', 'G', 'C', 'D'],
    6: ['A', 'F', 'E', 'D', 'C', 'G'],
    7: ['A', 'B', 'C'],
    8: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    9: ['A', 'B', 'C', 'D', 'F', 'G']
}

# === AFFICHAGE DE CHIFFRE ===
def clear_digit(offset):
    for i in range(LEDS_PER_DIGIT):
        np[offset + i] = (0, 0, 0)

def show_digit(value, offset, color):
    segments = get_segment_mapping(offset)
    clear_digit(offset)
    for seg in DIGIT_SEGMENTS.get(value, []):
        for i in segments[seg]:
            np[i] = color

# === AFFICHAGE CHIFFRE DOUBLE ===
def show_number(value, offset, color, left_segments=['B', 'C']):
    value = max(0, min(19, value))
    tens = value // 10
    units = value % 10
    if tens > 0:
        segs = get_segment_mapping(offset)
        for s in segs:
            for i in segs[s]:
                np[i] = (0, 0, 0)
        for seg in left_segments:
            for i in segs[seg]:
                np[i] = color
    else:
        for i in range(LEDS_PER_DIGIT):
            np[offset + i] = (0, 0, 0)
    show_digit(units, offset + LEDS_PER_DIGIT, color)

# === AFFICHAGE TEMPS CHRONO ===
def show_time(minutes, seconds, color, colon=True):
    digits = [minutes // 100, (minutes // 10) % 10, minutes % 10, seconds // 10, seconds % 10]
    for i, val in enumerate(digits):
        show_digit(val, OFFSET_CHRONO + i * LEDS_PER_DIGIT, color)
    for idx in COLON_LEDS:
        np[idx] = color if colon else (0, 0, 0)
    np.write()

# === BOUTONS ===
btn1_inc = Pin(2, Pin.IN, Pin.PULL_DOWN)
btn1_dec = Pin(3, Pin.IN, Pin.PULL_DOWN)
btn1_col = Pin(4, Pin.IN, Pin.PULL_DOWN)

btn2_inc = Pin(5, Pin.IN, Pin.PULL_DOWN)
btn2_dec = Pin(6, Pin.IN, Pin.PULL_DOWN)
btn2_col = Pin(7, Pin.IN, Pin.PULL_DOWN)

btn_preset = Pin(20, Pin.IN, Pin.PULL_DOWN)
btn_start = Pin(21, Pin.IN, Pin.PULL_DOWN)

# === ETATS ===
val1 = 0
val2 = 0
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]
color1_idx = 0
color2_idx = 2
chrono_color = (0, 150, 255)

presets = [(0, 45), (45, 90), (90, 105), (105, 120)]
preset_idx = 0
chrono_running = False
chrono_start_ms = 0
elapsed_sec = 0
colon_on = True
last_blink = time.ticks_ms()

# === LOOP ===
while True:
    now = time.ticks_ms()

    # GESTION AFFICHAGE 1
    if btn1_inc.value():
        val1 = (val1 + 1) % 20
        time.sleep(0.2)
    if btn1_dec.value():
        val1 = (val1 - 1) % 20
        time.sleep(0.2)
    if btn1_col.value():
        color1_idx = (color1_idx + 1) % len(colors)
        time.sleep(0.2)

    # GESTION AFFICHAGE 2
    if btn2_inc.value():
        val2 = (val2 + 1) % 20
        time.sleep(0.2)
    if btn2_dec.value():
        val2 = (val2 - 1) % 20
        time.sleep(0.2)
    if btn2_col.value():
        color2_idx = (color2_idx + 1) % len(colors)
        time.sleep(0.2)

    # AFFICHAGES LED
    show_number(val1, OFFSET_DISPLAY_1, colors[color1_idx])
    show_number(val2, OFFSET_DISPLAY_2, colors[color2_idx])

    # GESTION PRESET CHRONO
    if btn_preset.value():
        preset_idx = (preset_idx + 1) % len(presets)
        chrono_running = False
        elapsed_sec = 0
        colon_on = True
        start_min = presets[preset_idx][0]
        show_time(start_min, 0, chrono_color, colon_on)
        time.sleep(0.3)

    # DEMARRAGE CHRONO
    if btn_start.value() and not chrono_running:
        chrono_running = True
        chrono_start_ms = now
        time.sleep(0.3)

    # CHRONO EN COURS
    if chrono_running:
        elapsed_sec = time.ticks_diff(now, chrono_start_ms) // 1000
        start_m = presets[preset_idx][0] * 60
        end_m = presets[preset_idx][1] * 60
        current = start_m + elapsed_sec
        if current >= end_m:
            current = end_m
            chrono_running = False
        minutes = current // 60
        seconds = current % 60
        show_time(minutes, seconds, chrono_color, colon_on)

    # CLIGNOTEMENT DES :
    if time.ticks_diff(now, last_blink) >= 500:
        colon_on = not colon_on
        last_blink = now
        if not chrono_running:
            show_time(presets[preset_idx][0], 0, chrono_color, colon_on)
