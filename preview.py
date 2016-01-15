#! /usr/env/python

import signal

from gi import require_version

require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

class PreviewUi(Gtk.Window):
    """GTk main app window"""

    sizes = [16, 22, 24, 32, 48, 96]

    def __init__(self):
        super(PreviewUi, self).__init__()

        self.iconKey = "firefox"

        self.set_title("Icon Preview")
        self.set_wmclass("icon-preview", "Icon Preview")
        self.set_default_size(195, 188)

        # needs a desktop file for moar awesome
        Gdk.set_program_class("gnome-settings-theme")
        self.set_icon_name("gnome-settings-theme")

        self.connect("destroy", self.stop)

        self.create_layout()

        self.show_all()

    def bind_signals(self):
        signal.signal(signal.SIGINT, self.signal_stop_received)  # 9
        signal.signal(signal.SIGTERM, self.signal_stop_received)  # 15

    def signal_stop_received(self, *args):
        self.stop()

    def start(self):
        self.bind_signals()

        Gtk.main()

    def stop(self, *args):
        Gtk.main_quit()

    def create_icon_set_box(self, icons, bg):

        ev_box = Gtk.EventBox()
        ev_box.override_background_color(Gtk.StateType.NORMAL, bg)

        btn_box = Gtk.HBox()
        ev_box.add(btn_box)

        for pixbuf in icons:
            image = Gtk.Image.new_from_pixbuf(pixbuf)

            btn_box.add(image)

        return ev_box

    def create_icon_pixbufs(self, icon_key):
        icon_theme = Gtk.IconTheme.get_default()

        self.icons = []
        for size in self.sizes:

            try:
                pixbuf = icon_theme.load_icon(icon_key, size,
                                          Gtk.IconLookupFlags.FORCE_SIZE)
            except GObject.GError:
                raise KeyError

            self.icons.append(pixbuf)

    def key_changed(self, entry):
        self.iconKey = entry.get_text()
        self.reload_icons()

    def create_layout(self):
        self.main_window = Gtk.VBox()

        # make the icon name box
        key_label = Gtk.Label("Icon:")
        self.main_window.add(key_label)

        icon_key_input = Gtk.Entry()
        icon_key_input.set_text(self.iconKey)
        icon_key_input.connect('changed', self.key_changed)
        self.main_window.add(icon_key_input)

        self.icon_box = Gtk.VBox()
#        self.icon_box.set_reallocate_redraws(True)

        self.main_window.add(self.icon_box)

        self.reload_icons()

        self.add(self.main_window)

    def reload_icons(self):
        try:
            self.create_icon_pixbufs(self.iconKey)
        except KeyError:
            # unknown icon key
            return

        bgs = [
            Gdk.RGBA(0, 0, 0, 0), # transparent, so system default
            Gdk.RGBA(0, 0, 0, 1),
            Gdk.RGBA(.5, .5, .5, 1),
            Gdk.RGBA(1, 1, 1, 1)
        ]

        for child in self.icon_box.get_children():
            self.icon_box.remove(child)

        for bg in bgs:
            btn_box = self.create_icon_set_box(self.icons, bg)
            self.icon_box.add(btn_box)

        self.icon_box.show_all()

def main():
    gui = PreviewUi()
    gui.start()

if __name__ == "__main__":
    main()
