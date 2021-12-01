import evdev
import sys

device = evdev.InputDevice(sys.argv[1])
print(device)

x = 0

for event in device.read_loop():
    if event.type != evdev.ecodes.EV_REL:
        continue
    if event.code != evdev.ecodes.REL_X:
        continue

    x += event.value
    print(x)
