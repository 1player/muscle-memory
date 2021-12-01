import evdev
from evdev import ecodes as e
import sys

cap = {
    e.EV_REL: [
        e.REL_X,
        e.REL_Y,
    ]
}

mouse = evdev.InputDevice('/dev/input/event3')
ui = evdev.UInput.from_device(mouse)
#ui = evdev.UInput(cap)
print(ui)
print(ui.capabilities(verbose=True))
ui.write(e.EV_REL, e.REL_X, 1)
ui.syn()
