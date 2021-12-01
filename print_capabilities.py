import evdev
import sys

dev = evdev.InputDevice(sys.argv[1])
print(dev)
print(dev.capabilities(verbose=True))
