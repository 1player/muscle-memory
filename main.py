import evdev
from evdev import ecodes
import select
import time


class Application:
    alt_pressed = False
    recording = False
    recorded_x_distance = 0

    def __init__(self, mouse_device):
        self.mouse_device = mouse_device

    def handle_mouse_event(self, event):
        if self.recording and event.code == ecodes.REL_X:
            self.recorded_x_distance += event.value

    def handle_keyboard_event(self, event):
        key_event = evdev.categorize(event)

        if key_event.keycode == 'KEY_LEFTALT' or key_event.keycode == 'KEY_RIGHTALT':
            self.alt_pressed = key_event.keystate == 1 or key_event.keystate == 2
            return

        if self.alt_pressed and key_event.keystate == 1:
            if key_event.keycode == 'KEY_SLASH':
                self.toggle_recording()
            elif key_event.keycode == 'KEY_BACKSPACE':
                self.replay_recording()

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            print("Recording")
            self.recorded_x_distance = 0
        else:
            print("x distance =", self.recorded_x_distance)

    def replay_recording(self):
        print("Replaying")

        ui = evdev.UInput.from_device(self.mouse_device)
        i = 0
        while i < self.recorded_x_distance:
            ui.write(ecodes.EV_REL, ecodes.REL_X, 1)
            ui.syn()
            time.sleep(0.0002)
            i += 1


def supports_event_type(device, event_type):
    return event_type in device.capabilities()


def is_keyboard(device):
    return ecodes.EV_KEY in device.capabilities()


def is_mouse(device):
    rel_caps = device.capabilities().get(ecodes.EV_REL, [])
    return ecodes.REL_X in rel_caps and ecodes.REL_Y in rel_caps


def find_mice(devices):
    return [device for device in devices if is_mouse(device)]


def find_keyboards(devices):
    return [device for device in devices if is_keyboard(device)]


device_paths = [evdev.InputDevice(path) for path in evdev.list_devices()]
mice = find_mice(device_paths)
keyboards = find_keyboards(device_paths)

if len(mice) != 1:
    raise Exception("Mouse not found")

print("Mouse found: ", mice)
print("Keyboards found: ", keyboards)

listen_to = {dev.fd: dev for dev in mice + keyboards}
app = Application(mice[0])

while True:
    r, w, x = select.select(listen_to, [], [])
    for fd in r:
        for event in listen_to[fd].read():
            if event.type == ecodes.EV_REL:
                app.handle_mouse_event(event)
            if event.type == ecodes.EV_KEY:
                app.handle_keyboard_event(event)
