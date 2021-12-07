import sys
# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
# fmt: on


@Gtk.Template(filename="main_window.ui")
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "main_window"

    main_stack = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def on_calibrate_mode_toggled(self, toggle):
        if toggle.get_active():
            self.main_stack.set_visible_child_name("calibrate")
        else:
            self.main_stack.set_visible_child_name("convert")


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            application_id="cc.combo.MuscleMemory", flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title="MuscleMemory")
        self.window.show()


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)
